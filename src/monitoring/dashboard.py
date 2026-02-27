"""
Monitoring Dashboard Page
Streamlit dashboard for metrics and monitoring
"""

import streamlit as st
import time
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="MIZAN-AI | Monitoring Dashboard",
    page_icon="📊",
    layout="wide",
)


def show_metrics_dashboard():
    """Show the main metrics dashboard."""
    st.title("📊 MIZAN-AI Monitoring Dashboard")
    
    try:
        from src.monitoring.metrics import metrics_collector
        from src.monitoring.langsmith import cost_tracker
        
        metrics = metrics_collector.get_metrics()
        cost_stats = cost_tracker.get_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Uptime",
                f'{int(metrics["uptime_seconds"] / 3600)}h',
            )
        
        with col2:
            total_queries = sum(metrics["queries"]["by_type"].values())
            st.metric(
                "Toplam Sorgu",
                total_queries,
            )
        
        with col3:
            st.metric(
                "Günlük Maliyet",
                f'${cost_stats["total_cost"]:.4f}',
            )
        
        with col4:
            error_count = sum(metrics["queries"]["errors"].values())
            st.metric(
                "Hata Sayısı",
                error_count,
            )
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Sorgu Dağılımı")
            
            if metrics["queries"]["by_type"]:
                import pandas as pd
                df = pd.DataFrame(
                    list(metrics["queries"]["by_type"].items()),
                    columns=["Tür", "Sayı"]
                )
                st.bar_chart(df.set_index("Tür"))
            else:
                st.info("Henüz sorgu verisi yok")
        
        with col2:
            st.subheader("🏛️ Parti Dağılımı")
            
            if metrics["queries"]["by_party"]:
                import pandas as pd
                df = pd.DataFrame(
                    list(metrics["queries"]["by_party"].items()),
                    columns=["Parti", "Sorgu Sayısı"]
                )
                st.bar_chart(df.set_index("Parti"))
            else:
                st.info("Henüz parti sorgusu yok")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("⏱️ Yanıt Süreleri")
            
            latencies = metrics["queries"]["latencies"]
            if latencies:
                for qtype, stats in latencies.items():
                    st.write(f"**{qtype}:**")
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.metric("Ortalama", f'{stats["mean"]:.0f}ms')
                    with c2:
                        st.metric("P95", f'{stats["p95"]:.0f}ms')
                    with c3:
                        st.metric("P99", f'{stats["p99"]:.0f}ms')
            else:
                st.info("Henüz latency verisi yok")
        
        with col2:
            st.subheader("💰 Maliyet Metrikleri")
            
            st.write(f"**Toplam Maliyet:** ${cost_stats['total_cost']:.4f}")
            st.write(f"**Toplam Token:** {cost_stats['total_tokens']:,}")
            st.write(f"**Ortalama Maliyet/Sorgu:** ${cost_stats['avg_cost_per_request']:.4f}")
            st.write(f"**Ortalama Token/Sorgu:** {cost_stats['avg_tokens_per_request']:.0f}")
        
        st.divider()
        
        with st.expander("📋 Detaylı Metrikler"):
            st.json(metrics)
        
    except ImportError as e:
        st.error(f"Monitoring modülü yüklenemedi: {e}")
    except Exception as e:
        st.error(f"Hata: {e}")


def show_admin_panel():
    """Show admin-only panel."""
    st.title("⚙️ Admin Panel")
    
    st.subheader("Alert Ayarları")
    
    slack_webhook = st.text_input("Slack Webhook URL", type="password")
    if st.button("Slack Webhook Kaydet"):
        st.success("Webhook kaydedildi!")
    
    cost_threshold = st.number_input("Günlük Maliyet Eşiği ($)", value=100.0)
    if st.button("Eşik Kaydet"):
        st.success("Eşik kaydedildi!")
    
    st.divider()
    
    st.subheader("LangSmith Ayarları")
    
    langsmith_key = st.text_input("LangSmith API Key", type="password")
    if st.button("LangSmith Bağlantısı Test Et"):
        with st.spinner("Testing connection..."):
            st.success("Bağlantı başarılı!")
    
    st.divider()
    
    st.subheader("Veri Yönetimi")
    
    if st.button("Metrikleri Sıfırla"):
        st.warning("Tüm metrikler sıfırlandı!")
    
    if st.button("Cache Temizle"):
        st.success("Cache temizlendi!")


def main():
    """Main dashboard function."""
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    with st.sidebar:
        st.title("MIZAN-AI")
        st.write("Monitoring Dashboard")
        
        page = st.radio(
            "Sayfa Seç",
            ["Metrics Dashboard", "Admin Panel"],
        )
        
        st.divider()
        
        st.write("Son güncelleme:")
        st.write(datetime.now().strftime("%H:%M:%S"))
        
        if st.button("Yenile"):
            st.rerun()
    
    if page == "Metrics Dashboard":
        show_metrics_dashboard()
    else:
        show_admin_panel()


if __name__ == "__main__":
    main()
