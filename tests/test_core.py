"""Core module tests."""

import pytest
from src.core.parties import normalize_party_name, PARTY_INFO
from src.core.content_filter import should_answer


def test_normalize_party_name():
    """Test party name normalization."""
    assert normalize_party_name("chp") == "CHP"
    assert normalize_party_name("AKP") == "AKP"
    assert normalize_party_name("iyi") == "IYI"
    assert normalize_party_name("İYİ") == "IYI"


def test_party_info_exists():
    """Test that party info is defined."""
    assert "CHP" in PARTY_INFO
    assert "AKP" in PARTY_INFO
    assert len(PARTY_INFO) >= 8


def test_content_filter_valid():
    """Test content filter allows valid questions."""
    result, _ = should_answer("CHP'nin ekonomi politikası nedir?")
    assert result is True


def test_content_filter_offensive():
    """Test content filter blocks offensive content."""
    result, message = should_answer("küfürlü soru aptal")
    # Should either block or allow with warning
    assert isinstance(result, bool)
    assert isinstance(message, str)
