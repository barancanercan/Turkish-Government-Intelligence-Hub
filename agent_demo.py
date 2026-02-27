"""
Streamlit Demo for LangGraph Multi-Agent System
Simple interface to test the agent workflow
"""

import streamlit as st
from pathlib import Path
import sys
import logging

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.agents.graph import AgentWorkflow
from src.core.llm_setup import create_llm_handler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="MİZAN-AI | LangGraph Agents", page_icon="🤖", layout="wide", initial_sidebar_state="expanded"
)

st.markdown(
    """
<style>
    /* Dark Theme */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #fafafa;
    }
    .stButton > button {
        background-color: #4c78a8;
        color: #fafafa;
    }
    .stButton > button:hover {
        background-color: #5a94c7;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #fafafa !important;
    }
    .stMarkdown {
        color: #fafafa;
    }
    .stExpander > details > summary {
        background-color: #262730;
        color: #fafafa;
    }
    div[data-testid="stExpander"] {
        background-color: #1e2130;
    }
    .stAlert {
        background-color: #262730;
    }
    .stSuccess {
        background-color: #0e4429;
        color: #39d353;
    }
    .stError {
        background-color: #da3633;
        color: #fafafa;
    }
    .stWarning {
        background-color: #9e6a03;
        color: #fafafa;
    }
    .stInfo {
        background-color: #1158c7;
        color: #fafafa;
    }
    .stSpinner {
        color: #4c78a8;
    }
    /* Sidebar dark */
    section[data-testid="stSidebar"] {
        background-color: #0e1117;
    }
    /* Input focus */
    input:focus, textarea:focus {
        border-color: #4c78a8 !important;
        box-shadow: 0 0 0 1px #4c78a8 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("🤖 MİZAN-AI | Multi-Agent System")
st.markdown("LangGraph tabanlı multi-agent RAG sistemi")

if "workflow" not in st.session_state:
    with st.spinner("Sistem başlatılıyor..."):
        try:
            llm_result = create_llm_handler("CHP")
            llm = llm_result[0] if isinstance(llm_result, tuple) else llm_result
            st.session_state.workflow = AgentWorkflow(llm)
            st.session_state.llm = llm
            st.success("Sistem hazır!")
        except Exception as e:
            st.error(f"Sistem başlatma hatası: {e}")
            st.session_state.workflow = None

query = st.text_input("Sorunuz:", placeholder="Örn: CHP'nin ekonomi politikası nedir?")

if query and st.session_state.workflow:
    with st.spinner("Agent'lar çalışıyor..."):
        result = st.session_state.workflow.query(query)

        st.divider()

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📝 Yanıt")
            st.write(result["answer"])

        with col2:
            st.subheader("📊 Bilgiler")
            st.write(f"**Sorgu Türü:** {result['query_type']}")
            st.write(f"**Kalite Puanı:** {result['quality_score']:.2f}")
            st.write(f"**Revizyon Gerekli:** {'Evet' if result['needs_revision'] else 'Hayır'}")

        if result.get("sources"):
            with st.expander("📚 Kaynaklar"):
                for src in result["sources"]:
                    st.write(f"- {src}")

        with st.expander("🔍 Adımlar"):
            for step in result["steps"]:
                st.write(f"- {step}")

elif query and not st.session_state.workflow:
    st.warning("Sistem başlatılamadı. Lütfen sayfayı yenileyin.")
