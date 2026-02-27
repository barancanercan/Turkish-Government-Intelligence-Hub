"""
Multi-Model Comparison Streamlit App
Compare answers from 5 different Ollama models
"""

import streamlit as st
from pathlib import Path
import sys
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from langchain_ollama import OllamaLLM

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODELS = {
    "qwen2.5:7b": "Qwen 2.5 (7B) - Genel amaçlı, hızlı",
    "mistral": "Mistral (7B) - Avrupa odaklı, iyi performans",
    "gemma3": "Gemma 3 (3B) - Google, kompakt",
    "llama3.2:1b": "Llama 3.2 (1B) - Meta, minimal",
    "phi3": "Phi-3 (3B) - Microsoft, verimli",
}

st.set_page_config(
    page_title="MİZAN-AI | Model Karşılaştırma", page_icon="🔬", layout="wide", initial_sidebar_state="expanded"
)

st.markdown(
    """
<style>
    .stApp { background-color: #0e1117; color: #fafafa; }
    h1, h2, h3, h4, h5, h6, p, label { color: #fafafa !important; }
    .stTextInput > div > div > input { background-color: #262730; color: #fafafa; }
    .stButton > button { background-color: #4c78a8; color: #fafafa; }
    [data-testid="stSidebar"] { background-color: #0e1117; border-right: 1px solid #3a3f4b; }
    .model-card { 
        background-color: #1e2130; 
        border-radius: 10px; 
        padding: 20px; 
        margin: 10px 0;
        border: 1px solid #3a3f4b;
    }
    .model-title { font-size: 18px; font-weight: bold; color: #4c78a8; }
    .model-answer { font-size: 14px; color: #fafafa; line-height: 1.6; }
    .model-time { font-size: 12px; color: #888; }
</style>
""",
    unsafe_allow_html=True,
)

st.title("🔬 MİZAN-AI | 5'li Model Karşılaştırma")
st.markdown("Aynı soruyu 5 farklı LLM modeline sorun ve sonuçları karşılaştırın.")

query = st.text_input("🔍 Sorunuz:", placeholder="Örn: Mansur Yavaş kimdir?")

col1, col2 = st.columns([3, 1])
with col1:
    selected_models = st.multiselect(
        "Modelleri seçin:",
        options=list(MODELS.keys()),
        default=list(MODELS.keys())[:3],
        format_func=lambda x: MODELS[x],
    )
with col2:
    temperature = st.slider("Sıcaklık", 0.1, 1.0, 0.3)


def ask_model(model_name: str, query: str, temperature: float) -> dict:
    """Ask a single model and return result."""
    import time

    start = time.time()
    try:
        llm = OllamaLLM(model=model_name, temperature=temperature, base_url="http://localhost:11434")
        answer = llm.invoke(query)
        elapsed = time.time() - start
        return {
            "model": model_name,
            "display_name": MODELS.get(model_name, model_name),
            "answer": answer if isinstance(answer, str) else str(answer),
            "time": elapsed,
            "error": None,
        }
    except Exception as e:
        elapsed = time.time() - start
        return {
            "model": model_name,
            "display_name": MODELS.get(model_name, model_name),
            "answer": None,
            "time": elapsed,
            "error": str(e),
        }


if query and selected_models:
    st.divider()
    st.markdown(f"### 📊 Sonuçlar ({len(selected_models)} model)")

    results = []
    progress_bar = st.progress(0)

    for i, model in enumerate(selected_models):
        with st.spinner(f"{MODELS[model]} soruluyor..."):
            result = ask_model(model, query, temperature)
            results.append(result)
        progress_bar.progress((i + 1) / len(selected_models))

    progress_bar.empty()

    for idx, r in enumerate(results):
        with st.container():
            st.markdown(
                f"""
            <div class="model-card">
                <div class="model-title">🤖 {r["display_name"]}</div>
                <div class="model-time">⏱️ {r["time"]:.2f}s</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            if r["error"]:
                st.error(f"Hata: {r['error']}")
            else:
                st.markdown(f"<div class='model-answer'>{r['answer']}</div>", unsafe_allow_html=True)

            st.divider()

elif query and not selected_models:
    st.warning("Lütfen en az bir model seçin.")
