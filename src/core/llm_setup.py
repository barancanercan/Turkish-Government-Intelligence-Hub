"""
mizan-ai - LLM Setup Utilities with Error Handling and Retry Logic
Gemini (Birincil) + Ollama (Yedek) Configuration with Resilience
"""

import os
import time
import logging
from typing import Any, Dict, Tuple, Optional
from functools import wraps

from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

from src import config
from src.core.parties import normalize_party_name

logger = logging.getLogger(__name__)


def retry_on_failure(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator for retrying functions with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception: Optional[Exception] = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries + 1} failed: {e}. Retrying in {current_delay}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"All {max_retries + 1} attempts failed for {func.__name__}")

            if last_exception is not None:
                raise last_exception
            else:
                raise LLMError("Unknown error in retry logic")

        return wrapper

    return decorator


class LLMError(Exception):
    """Base exception for LLM-related errors."""

    pass


class LLMConnectionError(LLMError):
    """Raised when LLM connection fails."""

    pass


class LLMTimeoutError(LLMError):
    """Raised when LLM operation times out."""

    pass


class LLMResponseError(LLMError):
    """Raised when LLM returns an invalid or empty response."""

    pass


class LLMManager:
    """
    LLM Manager with automatic failover and retry logic.
    """

    def __init__(self):
        self._gemini_chain = None
        self._ollama_chain = None
        self._current_llm_type = None
        self._initialized = False
        self._init_errors = {}

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    @retry_on_failure(max_retries=2, delay=1.0)
    def _test_gemini_connection(self, api_key: str) -> bool:
        """Test Gemini connection with retry logic."""
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            api_key=api_key,
            temperature=config.LLM_TEMPERATURE,
            max_tokens=10,
        )
        response = llm.invoke("test")
        response_str = str(response) if response else ""
        return bool(response_str and len(response_str.strip()) > 0)

    @retry_on_failure(max_retries=2, delay=0.5)
    def _test_ollama_connection(self, model: str, base_url: str) -> bool:
        """Test Ollama connection with retry logic."""
        llm = OllamaLLM(
            model=model,
            temperature=0.1,
            base_url=base_url,
            num_predict=10,
        )
        response = llm.invoke("test")
        return bool(response and len(response.strip()) > 0)

    def initialize(self, party: str = "CHP") -> Tuple[bool, str]:
        """
        Initialize LLM with automatic failover.

        Args:
            party: Target party code

        Returns:
            Tuple[bool, str]: (success, llm_type)
        """
        if self._initialized and self._current_llm_type is not None and self._current_llm_type != "none":
            return True, self._current_llm_type

        logger.info("Initializing LLM manager...")

        # Try Gemini first
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                if self._test_gemini_connection(api_key):
                    self._gemini_chain = self._create_gemini_chain(party)
                    self._current_llm_type = "gemini"
                    self._initialized = True
                    logger.info("✅ Gemini initialized successfully (Primary LLM)")
                    return True, "gemini"
            except Exception as e:
                logger.warning(f"⚠️ Gemini initialization failed: {e}")
                self._init_errors["gemini"] = str(e)

        # Fallback to Ollama
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model = os.getenv("OLLAMA_MODEL", config.LLM_MODEL)

        try:
            if self._test_ollama_connection(model, ollama_base_url):
                self._ollama_chain = self._create_ollama_chain(party, model, ollama_base_url)
                self._current_llm_type = "ollama"
                self._initialized = True
                logger.info("✅ Ollama initialized successfully (Fallback LLM)")
                return True, "ollama"
        except Exception as e:
            logger.warning(f"⚠️ Ollama initialization failed: {e}")
            self._init_errors["ollama"] = str(e)

        # No LLM available
        self._current_llm_type = "none"
        self._initialized = True
        logger.error("❌ No LLM available!")
        return False, "none"

    def _create_gemini_chain(self, party: str) -> Any:
        """Create Gemini chain."""
        normalized_party = normalize_party_name(party)

        prompt_template_str = config.SYSTEM_PROMPTS.get(normalized_party)
        if not prompt_template_str:
            prompt_template_str = config.SYSTEM_PROMPTS.get(party)
        if not prompt_template_str:
            prompt_template_str = "Soruyu yanıtla: {question}"

        prompt_template = PromptTemplate.from_template(prompt_template_str)

        api_key = os.getenv("GEMINI_API_KEY")
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            api_key=api_key,
            temperature=config.LLM_TEMPERATURE,
        )

        return prompt_template | llm | StrOutputParser()

    def _create_ollama_chain(self, party: str, model: str, base_url: str) -> Any:
        """Create Ollama chain."""
        normalized_party = normalize_party_name(party)

        prompt_template_str = config.SYSTEM_PROMPTS.get(normalized_party)
        if not prompt_template_str:
            prompt_template_str = config.SYSTEM_PROMPTS.get(party)
        if not prompt_template_str:
            prompt_template_str = "Soruyu yanıtla: {question}"

        prompt_template = PromptTemplate.from_template(prompt_template_str)

        llm = OllamaLLM(
            model=model,
            temperature=config.LLM_TEMPERATURE,
            base_url=base_url,
            repeat_penalty=1.2,
            num_predict=512,
        )

        return prompt_template | llm | StrOutputParser()

    @retry_on_failure(max_retries=2, delay=1.0)
    def invoke(self, prompt: str, party: str = "CHP") -> str:
        """
        Invoke LLM with automatic failover and retry.

        Args:
            prompt: Input prompt
            party: Target party code

        Returns:
            str: LLM response

        Raises:
            LLMError: If all LLM attempts fail
        """
        # Ensure initialization
        if not self._initialized:
            self.initialize(party)

        # Try current LLM first
        if self._current_llm_type == "gemini" and self._gemini_chain:
            try:
                response = self._gemini_chain.invoke({"question": prompt})
                if response and response.strip():
                    return response
                raise LLMResponseError("Empty response from Gemini")
            except Exception as e:
                logger.warning(f"Gemini invoke failed: {e}")
                self._init_errors["gemini"] = str(e)

        # Fallback to Ollama
        if self._current_llm_type == "ollama" and self._ollama_chain:
            try:
                response = self._ollama_chain.invoke({"question": prompt})
                if response and response.strip():
                    return response
                raise LLMResponseError("Empty response from Ollama")
            except Exception as e:
                logger.warning(f"Ollama invoke failed: {e}")
                self._init_errors["ollama"] = str(e)

        # Try fallback LLM if current one failed
        if self._current_llm_type != "none":
            # Try the other LLM as fallback
            if self._current_llm_type == "gemini":
                # Reinitialize with Ollama
                self._initialized = False
                self.initialize(party)
                if self._current_llm_type == "ollama" and self._ollama_chain:
                    return self._ollama_chain.invoke({"question": prompt})
            else:
                # Reinitialize with Gemini
                self._initialized = False
                self.initialize(party)
                if self._current_llm_type == "gemini" and self._gemini_chain:
                    return self._gemini_chain.invoke({"question": prompt})

        raise LLMConnectionError("No LLM available")

    def get_status(self) -> Dict[str, Any]:
        """Get LLM status."""
        return {
            "initialized": self._initialized,
            "current_llm": self._current_llm_type,
            "errors": self._init_errors,
        }

    def reset(self):
        """Reset LLM manager."""
        self._gemini_chain = None
        self._ollama_chain = None
        self._current_llm_type = None
        self._initialized = False
        self._init_errors = {}


# Global LLM manager instance
llm_manager = LLMManager()


def get_ollama_model(model_type: str = "main") -> OllamaLLM:
    """
    Get Ollama LLM by model type.

    Args:
        model_type: "main" (main brain) or "fast" (quick tasks)

    Returns:
        OllamaLLM: Configured Ollama model
    """
    model_name = config.LLM_MODELS.get(model_type, config.LLM_MODELS["main"])
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    logger.info(f"Using model: {model_name} ({model_type})")

    return OllamaLLM(
        model=model_name,
        temperature=config.LLM_TEMPERATURE,
        base_url=ollama_base_url,
        repeat_penalty=1.2,
        num_predict=512,
    )


def setup_gemini_chain(party: str) -> Tuple[Any, str]:
    """
    Create chain for Gemini LLM (Primary).

    Args:
        party: Target party code.

    Returns:
        Tuple[Any, str]: (handler, llm_type)
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.warning("⚠️ GEMINI_API_KEY not set")
        return (None, "none")

    normalized_party = normalize_party_name(party)

    prompt_template_str = config.SYSTEM_PROMPTS.get(normalized_party)
    if not prompt_template_str:
        prompt_template_str = config.SYSTEM_PROMPTS.get(party)
    if not prompt_template_str:
        prompt_template_str = "Soruyu yanıtla: {question}"

    prompt_template = PromptTemplate.from_template(prompt_template_str)

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            api_key=api_key,
            temperature=config.LLM_TEMPERATURE,
        )
        llm.invoke("test")

        chain = prompt_template | llm | StrOutputParser()
        logger.info("✅ Gemini connected (Primary LLM)")
        return (chain, "gemini")
    except Exception as e:
        logger.warning(f"⚠️ Gemini connection failed: {e}")
        return (None, "none")


def setup_ollama_chain(party: str) -> Tuple[Any, str]:
    """
    Create chain for Ollama LLM (Fallback).

    Args:
        party: Target party code.

    Returns:
        Tuple[Any, str]: (handler, llm_type)
    """
    normalized_party = normalize_party_name(party)

    prompt_template_str = config.SYSTEM_PROMPTS.get(normalized_party)
    if not prompt_template_str:
        prompt_template_str = config.SYSTEM_PROMPTS.get(party)
    if not prompt_template_str:
        prompt_template_str = "Soruyu yanıtla: {question}"

    prompt_template = PromptTemplate.from_template(prompt_template_str)

    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", config.LLM_MODEL)

    llm = OllamaLLM(
        model=model,
        temperature=config.LLM_TEMPERATURE,
        base_url=ollama_base_url,
    )

    try:
        llm.invoke("test")
    except Exception as e:
        logger.warning(f"⚠️ Ollama test connection failed: {e}")

    chain = prompt_template | llm | StrOutputParser()
    logger.info("✅ Ollama connected (Fallback LLM)")
    return (chain, "ollama")


def create_llm_handler(party: str) -> Tuple[Any, str]:
    """
    Create LLM handler.

    Tries Gemini first, falls back to Ollama if needed.

    Args:
        party: Target party code

    Returns:
        Tuple[Any, str]: (handler, llm_type)
    """
    # Try Gemini first
    try:
        handler, llm_type = setup_gemini_chain(party)
        if handler is not None:
            return (handler, llm_type)
    except Exception as e:
        logger.warning(f"⚠️ Gemini failed, trying Ollama: {e}")

    # Fallback: Ollama
    try:
        handler, llm_type = setup_ollama_chain(party)
        if handler is not None:
            return (handler, llm_type)
    except Exception as e:
        logger.error(f"❌ Ollama also failed: {e}")

    logger.error("❌ No LLM available!")
    return (None, "none")


def get_llm_display_name(llm_type: str) -> str:
    """
    Get user-friendly name for LLM type.

    Args:
        llm_type: LLM type

    Returns:
        str: Display name
    """
    display_names = {
        "gemini": "Gemini 1.5 Flash (Primary)",
        "ollama": "Qwen 2.5 7B (Ollama)",
        "none": "No LLM",
    }
    return display_names.get(llm_type, "Unknown")


@retry_on_failure(max_retries=2, delay=0.5)
def check_llm_health(llm_type: str, timeout: float = 5.0) -> bool:
    """
    Check LLM health with retry logic.

    Args:
        llm_type: "gemini" or "ollama"
        timeout: Timeout in seconds

    Returns:
        bool: True if healthy, False otherwise
    """
    try:
        if llm_type == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key:
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    api_key=api_key,
                    temperature=0.1,
                )
                llm.invoke("test", max_tokens=5)
                return True
        elif llm_type == "ollama":
            ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            model = os.getenv("OLLAMA_MODEL", config.LLM_MODEL)
            llm = OllamaLLM(model=model, base_url=ollama_base_url, num_predict=5)
            llm.invoke("test")
            return True
    except Exception:
        pass

    return False


def check_llm_status() -> Dict[str, Any]:
    """
    Check LLM statuses.

    Returns:
        Dict: Status information
    """
    status = {
        "gemini": {"available": False, "error": None},
        "ollama": {"available": False, "error": None},
    }

    # Gemini check
    try:
        if check_llm_health("gemini"):
            status["gemini"]["available"] = True
    except Exception as e:
        status["gemini"]["error"] = str(e)

    # Ollama check
    try:
        if check_llm_health("ollama"):
            status["ollama"]["available"] = True
    except Exception as e:
        status["ollama"]["error"] = str(e)

    return status
