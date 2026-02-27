# MİZAN-AI GELİŞTİRME PLANI v2.0

> **Çift Hedef:** CV Güçlendirme + SaaS İş Modeli Temeli

---

## VİZYON

```
┌─────────────────────────────────────────────────────────────────┐
│                         MİZAN-AI                                │
│         "Open Data. Open Democracy. Powered by AI."             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [AÇIK KAYNAK]              →            [SaaS PLATFORM]       │
│   GitHub Portfolio                        Gelir Üreten Ürün     │
│   Teknik Showcase                         B2B + B2C             │
│   Topluluk                                Sürdürülebilir        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## MEVCUT DURUM

### Tamamlanan Fazlar (v1.0)
| Faz | Modül | Durum | CV | SaaS |
|-----|-------|-------|:--:|:----:|
| FAZ 1 | Data Ingestion Agent | ✅ | ⭐⭐ | ⭐⭐ |
| FAZ 2 | Retrieval Engine (Hybrid) | ✅ | ⭐⭐⭐ | ⭐⭐ |
| FAZ 3 | Query Rewriting Layer | ✅ | ⭐⭐ | ⭐⭐ |
| FAZ 4 | Generation Layer | ✅ | ⭐⭐ | ⭐⭐ |
| FAZ 5 | Evaluation Stack | ✅ | ⭐⭐⭐ | ⭐ |
| FAZ 6 | Guardrail & Security | ✅ | ⭐⭐⭐ | ⭐⭐⭐ |

### Mevcut Zayıflıklar (Rapor.md'den)
| Problem | SaaS Etkisi | Çözüm Fazı |
|---------|-------------|------------|
| Statik veri (tüzükler) | Recurring value düşük | FAZ 9 |
| Sezonluk talep | Churn yüksek | FAZ 9, 11 |
| API yok | B2B entegrasyon imkansız | FAZ 8 |
| Monitoring yok | Ölçekleme zor | FAZ 10 |

---

## YENİ FAZLAR (v2.0)

### Stratejik Öncelik Matrisi

```
                    SaaS DEĞERİ
                    Düşük    Yüksek
              ┌──────────┬──────────┐
     Yüksek   │  FAZ 7   │  FAZ 8   │
              │ LangGraph│ FastAPI  │
   CV         │  FAZ 12  │  FAZ 10  │
 DEĞERİ       │Benchmark │Monitoring│
              ├──────────┼──────────┤
     Düşük    │   ---    │  FAZ 9   │
              │          │ Dynamic  │
              │  FAZ 13  │  FAZ 11  │
              │ Showcase │ Features │
              └──────────┴──────────┘
```

**Optimal Sıralama:** FAZ 7 → FAZ 8 → FAZ 9 → FAZ 10 → FAZ 11 → FAZ 12 → FAZ 13

---

## FAZ 7: Multi-Agent Orchestration (LangGraph)

| Metrik | Değer |
|--------|-------|
| **CV Etkisi** | ⭐⭐⭐⭐⭐ (Çok Yüksek) |
| **SaaS Etkisi** | ⭐⭐ (Düşük-Orta) |
| **Öncelik** | 1 |
| **Süre** | 2-3 hafta |

### Neden Öncelikli?
- LangGraph = 2024-2025'in en sıcak AI trendi
- Multi-agent deneyimi iş ilanlarında aranan skill
- Teknik derinlik göstergesi

### 7.1 Agent Mimarisi
```
┌─────────────────────────────────────────────────────────┐
│                   SUPERVISOR AGENT                       │
│              (Orkestrasyon & Karar Verme)               │
└────────────────────────┬────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  RESEARCHER  │  │   ANALYST    │  │    WRITER    │
│    AGENT     │  │    AGENT     │  │    AGENT     │
│              │  │              │  │              │
│ • Vektör DB  │  │ • Karşılaşt. │  │ • Yanıt      │
│ • Web Search │  │ • Trend      │  │ • Kaynak     │
│ • Filtering  │  │ • Sentez     │  │ • Format     │
└──────────────┘  └──────────────┘  └──────────────┘
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                ┌──────────────┐
                │    CRITIC    │
                │    AGENT     │
                │              │
                │ • Doğrulama  │
                │ • Halluc.    │
                │ • Kalite     │
                └──────────────┘
```

### 7.2 Tasklar
```
[ ] 7.1.1 LangGraph kurulum ve StateGraph tanımı
[ ] 7.1.2 AgentState Pydantic modeli
[ ] 7.2.1 Supervisor Agent implementasyonu
[ ] 7.2.2 Researcher Agent implementasyonu
[ ] 7.2.3 Analyst Agent implementasyonu
[ ] 7.2.4 Writer Agent implementasyonu
[ ] 7.2.5 Critic Agent implementasyonu
[ ] 7.3.1 Simple Query Workflow
[ ] 7.3.2 Comparative Analysis Workflow
[ ] 7.3.3 Deep Research Workflow
[ ] 7.4.1 Streamlit entegrasyonu
[ ] 7.4.2 Agent trace visualization
[ ] 7.5.1 Unit testler
[ ] 7.5.2 Integration testler
```

### Dosya Yapısı
```
src/agents/
├── __init__.py
├── state.py           # AgentState, MessageState
├── supervisor.py      # Supervisor Agent
├── researcher.py      # Researcher Agent (vektör + web)
├── analyst.py         # Analyst Agent (karşılaştırma)
├── writer.py          # Writer Agent (yanıt üretimi)
├── critic.py          # Critic Agent (kalite kontrol)
├── tools.py           # Agent tools (search, retrieve)
├── prompts.py         # Agent system prompts
└── graph.py           # LangGraph workflow definitions
```

---

## FAZ 8: Production-Grade API (FastAPI)

| Metrik | Değer |
|--------|-------|
| **CV Etkisi** | ⭐⭐⭐⭐ (Yüksek) |
| **SaaS Etkisi** | ⭐⭐⭐⭐⭐ (Çok Yüksek) |
| **Öncelik** | 2 |
| **Süre** | 1-2 hafta |

### Neden Kritik?
- **CV:** Backend geliştirme, API design becerisi
- **SaaS:** B2B entegrasyon temeli, API monetization

### 8.1 API Endpoint'leri
```
┌─────────────────────────────────────────────────────────┐
│                    MIZAN-AI API v1                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  QUERY ENDPOINTS                                        │
│  ├── POST /api/v1/query          → Tek soru            │
│  ├── POST /api/v1/compare        → Parti karşılaştırma │
│  └── POST /api/v1/analyze        → Derin analiz        │
│                                                         │
│  DATA ENDPOINTS                                         │
│  ├── GET  /api/v1/parties        → Parti listesi       │
│  ├── GET  /api/v1/parties/{id}   → Parti detay         │
│  └── GET  /api/v1/topics         → Konu listesi        │
│                                                         │
│  USER ENDPOINTS (SaaS)                                  │
│  ├── POST /api/v1/auth/register  → Kayıt               │
│  ├── POST /api/v1/auth/login     → Giriş               │
│  ├── GET  /api/v1/usage          → Kullanım istatistik │
│  └── POST /api/v1/feedback       → Geri bildirim       │
│                                                         │
│  SYSTEM ENDPOINTS                                       │
│  ├── GET  /api/v1/health         → Sağlık kontrolü     │
│  └── GET  /api/v1/stats          → Sistem metrikleri   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 8.2 SaaS Katmanları (Rate Limiting)
```python
# Tier-based rate limiting
TIERS = {
    "free": {
        "requests_per_day": 10,
        "compare_enabled": False,
        "sources_visible": False
    },
    "pro": {
        "requests_per_day": 500,
        "compare_enabled": True,
        "sources_visible": True
    },
    "enterprise": {
        "requests_per_day": -1,  # Unlimited
        "compare_enabled": True,
        "sources_visible": True,
        "priority_queue": True
    }
}
```

### 8.3 Tasklar
```
[ ] 8.1.1 FastAPI boilerplate + proje yapısı
[ ] 8.1.2 Pydantic request/response schemas
[ ] 8.1.3 Query endpoint implementasyonu
[ ] 8.1.4 Compare endpoint implementasyonu
[ ] 8.1.5 Parties CRUD endpoints
[ ] 8.2.1 JWT authentication middleware
[ ] 8.2.2 API key authentication
[ ] 8.2.3 Rate limiting middleware (tier-based)
[ ] 8.2.4 Request validation & error handling
[ ] 8.2.5 CORS configuration
[ ] 8.3.1 Response caching (Redis opsiyonel)
[ ] 8.3.2 Async query processing
[ ] 8.4.1 Swagger/OpenAPI documentation
[ ] 8.4.2 Postman collection oluştur
[ ] 8.4.3 API kullanım örnekleri (curl, Python, JS)
[ ] 8.5.1 Docker Compose (API + DB)
[ ] 8.5.2 Unit & integration testler
```

### Dosya Yapısı
```
src/api/
├── __init__.py
├── main.py                # FastAPI app entry
├── config.py              # API configuration
├── dependencies.py        # Dependency injection
├── routers/
│   ├── __init__.py
│   ├── query.py           # /query, /compare, /analyze
│   ├── parties.py         # /parties endpoints
│   ├── auth.py            # /auth endpoints
│   └── system.py          # /health, /stats
├── schemas/
│   ├── __init__.py
│   ├── query.py           # QueryRequest, QueryResponse
│   ├── party.py           # PartySchema
│   └── auth.py            # TokenSchema, UserSchema
├── middleware/
│   ├── __init__.py
│   ├── auth.py            # JWT + API key auth
│   ├── rate_limit.py      # Tier-based limiting
│   └── logging.py         # Request logging
├── services/
│   ├── __init__.py
│   ├── query_service.py   # Business logic
│   └── user_service.py    # User management
└── tests/
    ├── test_query.py
    └── test_auth.py
```

---

## FAZ 9: Dynamic Data Pipeline

| Metrik | Değer |
|--------|-------|
| **CV Etkisi** | ⭐⭐⭐ (Orta) |
| **SaaS Etkisi** | ⭐⭐⭐⭐⭐ (Çok Yüksek) |
| **Öncelik** | 3 |
| **Süre** | 2-3 hafta |

### Neden Kritik SaaS İçin?
**Rapor.md'den:** "Recurring value zayıf - kullanıcı bilgiyi aldıktan sonra geri dönmeyebilir"

**Çözüm:** Dinamik veri akışı ile sürekli değer üret

### 9.1 Yeni Veri Kaynakları
```
┌─────────────────────────────────────────────────────────┐
│              DİNAMİK VERİ KAYNAKLARI                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📰 HABER AKIŞI                                         │
│  ├── Parti açıklamaları (resmi siteler)                │
│  ├── Haber siteleri (RSS)                              │
│  └── Günlük otomatik scraping                          │
│                                                         │
│  🏛️ MECLİS VERİLERİ                                    │
│  ├── TBMM tutanakları                                  │
│  ├── Kanun teklifleri                                  │
│  ├── Meclis soruları                                   │
│  └── Oylama kayıtları                                  │
│                                                         │
│  👤 MİLLETVEKİLİ PROFİLLERİ                            │
│  ├── Biyografi                                         │
│  ├── Komisyon üyelikleri                               │
│  ├── Oy geçmişi                                        │
│  └── Sosyal medya (opsiyonel)                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 9.2 Pipeline Mimarisi
```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Scraper  │───▶│ Cleaner  │───▶│ Embedder │───▶│ VectorDB │
│ (Daily)  │    │          │    │          │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │
     ▼
┌──────────┐
│ Notifier │───▶ E-posta / Webhook
└──────────┘
```

### 9.3 Tasklar
```
[ ] 9.1.1 Haber scraper altyapısı (BeautifulSoup/Scrapy)
[ ] 9.1.2 Parti resmi site scraper'ları
[ ] 9.1.3 RSS feed entegrasyonu
[ ] 9.2.1 TBMM API araştırması
[ ] 9.2.2 Meclis tutanakları parser
[ ] 9.2.3 Kanun teklifi scraper
[ ] 9.3.1 Milletvekili veri modeli
[ ] 9.3.2 TBMM profil scraper
[ ] 9.4.1 Daily cron job setup
[ ] 9.4.2 Incremental vector update
[ ] 9.4.3 Data freshness metadata
[ ] 9.5.1 Change detection system
[ ] 9.5.2 Alert trigger logic
```

### Dosya Yapısı
```
src/pipeline/
├── __init__.py
├── scrapers/
│   ├── __init__.py
│   ├── base.py            # BaseScraper class
│   ├── news.py            # Haber scraper
│   ├── tbmm.py            # TBMM scraper
│   └── party_sites.py     # Parti siteleri
├── processors/
│   ├── __init__.py
│   ├── cleaner.py         # Veri temizleme
│   └── embedder.py        # Embedding pipeline
├── storage/
│   ├── __init__.py
│   └── vector_updater.py  # Incremental update
├── scheduler/
│   ├── __init__.py
│   └── cron.py            # Scheduled jobs
└── alerts/
    ├── __init__.py
    └── notifier.py        # Alert system
```

---

## FAZ 10: Observability & Monitoring

| Metrik | Değer |
|--------|-------|
| **CV Etkisi** | ⭐⭐⭐⭐ (Yüksek) |
| **SaaS Etkisi** | ⭐⭐⭐⭐ (Yüksek) |
| **Öncelik** | 4 |
| **Süre** | 1 hafta |

### 10.1 LangSmith Entegrasyonu
```
┌─────────────────────────────────────────────────────────┐
│                   LANGSMITH TRACES                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Query: "CHP'nin ekonomi politikası nedir?"             │
│  ├── [0.1s] Router Engine                              │
│  │   └── Intent: LOCAL_KNOWLEDGE                       │
│  ├── [0.3s] Vector Search                              │
│  │   └── Retrieved: 5 chunks                           │
│  ├── [1.2s] LLM Generation                             │
│  │   ├── Model: gemini-2.0-flash                       │
│  │   ├── Input tokens: 1,847                           │
│  │   └── Output tokens: 523                            │
│  └── [0.05s] Response Formatting                       │
│                                                         │
│  Total: 1.65s | Cost: $0.0023                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 10.2 Business Metrics Dashboard
```
┌─────────────────────────────────────────────────────────┐
│                  MİZAN-AI DASHBOARD                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📊 KULLANIM METRİKLERİ                                 │
│  ├── Günlük sorgu: 1,247                               │
│  ├── Unique kullanıcı: 89                              │
│  ├── Ortalama yanıt süresi: 2.3s                       │
│  └── Cache hit rate: 34%                               │
│                                                         │
│  💰 MALİYET METRİKLERİ                                  │
│  ├── Günlük LLM maliyeti: $12.45                       │
│  ├── Sorgu başına maliyet: $0.01                       │
│  └── Aylık projeksiyon: $373.50                        │
│                                                         │
│  🎯 KALİTE METRİKLERİ                                   │
│  ├── Kullanıcı memnuniyeti: 4.2/5                      │
│  ├── Hallucination rate: 3.2%                          │
│  └── Citation accuracy: 94.7%                          │
│                                                         │
│  🏛️ PARTİ DAĞILIMI                                      │
│  ├── CHP: 28%  ████████░░                              │
│  ├── AKP: 24%  ███████░░░                              │
│  ├── MHP: 15%  █████░░░░░                              │
│  └── Diğer: 33% ██████████                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 10.3 Tasklar
```
[ ] 10.1.1 LangSmith SDK kurulum
[ ] 10.1.2 Trace instrumentation (tüm agent'lar)
[ ] 10.1.3 Cost tracking callback
[ ] 10.2.1 Prometheus metrics exporter
[ ] 10.2.2 Custom metrics (query volume, latency)
[ ] 10.2.3 Business metrics (parti dağılımı, konu analizi)
[ ] 10.3.1 Streamlit dashboard page
[ ] 10.3.2 Admin-only erişim kontrolü
[ ] 10.4.1 Structured JSON logging
[ ] 10.4.2 Request ID tracing
[ ] 10.5.1 Slack/Discord alert webhook
[ ] 10.5.2 Cost threshold alerts
```

---

## FAZ 11: User Engagement Features

| Metrik | Değer |
|--------|-------|
| **CV Etkisi** | ⭐⭐ (Düşük-Orta) |
| **SaaS Etkisi** | ⭐⭐⭐⭐⭐ (Çok Yüksek) |
| **Öncelik** | 5 |
| **Süre** | 1-2 hafta |

### Neden Kritik SaaS İçin?
**Rapor.md'den:** "Alert/Bildirim sistemi ile kullanıcı bağlılığı sağlanabilir"

### 11.1 Alert Sistemi
```
┌─────────────────────────────────────────────────────────┐
│                    ALERT SİSTEMİ                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📧 E-POSTA ALERTLERİ                                   │
│  ├── "CHP ekonomi" konusunda yeni açıklama             │
│  ├── Haftalık parti özeti                              │
│  └── Meclis'te önemli oylama                           │
│                                                         │
│  🔔 WEBHOOK ALERTLERİ                                   │
│  ├── Slack entegrasyonu                                │
│  ├── Discord bot                                       │
│  └── Custom webhook                                    │
│                                                         │
│  ⚙️ KULLANICI AYARLARI                                  │
│  ├── Takip edilen partiler                             │
│  ├── Takip edilen konular                              │
│  ├── Alert frekansı                                    │
│  └── Tercih edilen kanal                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 11.2 Rapor Oluşturucu
```
┌─────────────────────────────────────────────────────────┐
│              KARŞILAŞTIRMALI RAPOR                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Konu: EKONOMİ POLİTİKASI                               │
│  Tarih: 26 Şubat 2026                                  │
│                                                         │
│  ┌─────────────┬─────────────┬─────────────┐           │
│  │     CHP     │     AKP     │     MHP     │           │
│  ├─────────────┼─────────────┼─────────────┤           │
│  │ Sosyal      │ Serbest     │ Milliyetçi  │           │
│  │ demokrat    │ piyasa      │ ekonomi     │           │
│  │ yaklaşım    │ odaklı      │ modeli      │           │
│  └─────────────┴─────────────┴─────────────┘           │
│                                                         │
│  [PDF İNDİR] [PAYLAŞ] [E-POSTA GÖNDER]                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 11.3 Tasklar
```
[ ] 11.1.1 Alert subscription modeli (DB)
[ ] 11.1.2 E-posta gönderme servisi (SendGrid/Resend)
[ ] 11.1.3 Alert trigger engine
[ ] 11.1.4 Kullanıcı tercih yönetimi UI
[ ] 11.2.1 Webhook endpoint'leri
[ ] 11.2.2 Slack app oluştur
[ ] 11.2.3 Discord bot template
[ ] 11.3.1 Rapor şablonu tasarımı
[ ] 11.3.2 PDF export (WeasyPrint/ReportLab)
[ ] 11.3.3 Rapor paylaşım linkleri
[ ] 11.4.1 Saved queries özelliği
[ ] 11.4.2 Query history
```

---

## FAZ 12: Benchmark Suite

| Metrik | Değer |
|--------|-------|
| **CV Etkisi** | ⭐⭐⭐⭐ (Yüksek) |
| **SaaS Etkisi** | ⭐⭐ (Düşük) |
| **Öncelik** | 6 |
| **Süre** | 1 hafta |

### 12.1 Gold Dataset
```json
{
  "version": "1.0",
  "questions": [
    {
      "id": "q001",
      "question": "CHP'nin laiklik ilkesine yaklaşımı nedir?",
      "difficulty": "easy",
      "type": "single_party",
      "expected_sources": ["chp_tuzuk.pdf"],
      "ground_truth_keywords": ["laiklik", "cumhuriyet", "devrim"]
    },
    {
      "id": "q002",
      "question": "AKP ve MHP'nin dış politika yaklaşımları nasıl farklılaşır?",
      "difficulty": "hard",
      "type": "comparison",
      "expected_sources": ["akp_tuzuk.pdf", "mhp_tuzuk.pdf"],
      "ground_truth_keywords": ["AB", "NATO", "Türk dünyası"]
    }
  ]
}
```

### 12.2 Metrik Kategorileri
| Kategori | Metrikler |
|----------|-----------|
| **Retrieval** | Recall@k, Precision@k, MRR, NDCG |
| **Generation** | ROUGE-L, BERTScore, Faithfulness |
| **System** | Latency (p50/p95/p99), Throughput, Memory |
| **Quality** | Hallucination Rate, Citation Accuracy |

### 12.3 Tasklar
```
[ ] 12.1.1 Gold QA dataset (100 soru)
[ ] 12.1.2 Difficulty kategorileri
[ ] 12.1.3 Ground truth annotations
[ ] 12.2.1 Retrieval metrics implementasyonu
[ ] 12.2.2 Generation metrics implementasyonu
[ ] 12.2.3 System metrics collector
[ ] 12.3.1 Benchmark runner script
[ ] 12.3.2 JSON/Markdown report generator
[ ] 12.4.1 GitHub Actions CI entegrasyonu
[ ] 12.4.2 README badge'leri
```

---

## FAZ 13: Documentation & Showcase

| Metrik | Değer |
|--------|-------|
| **CV Etkisi** | ⭐⭐⭐⭐ (Yüksek) |
| **SaaS Etkisi** | ⭐⭐⭐ (Orta) |
| **Öncelik** | 7 (Sürekli) |
| **Süre** | 1-2 hafta + sürekli |

### 13.1 Medium Yazı Serisi
| # | Başlık | Hedef | Durum |
|---|--------|-------|-------|
| 1 | "Building a Political RAG System with LangChain" | Genel tanıtım | [ ] |
| 2 | "Multi-Agent Orchestration with LangGraph" | Teknik derinlik | [ ] |
| 3 | "Turkish NLP Challenges in RAG Systems" | Niş uzmanlık | [ ] |
| 4 | "Production-Grade RAG: From Prototype to API" | SaaS journey | [ ] |
| 5 | "Evaluating RAG Systems: Metrics That Matter" | Benchmark | [ ] |

### 13.2 GitHub Showcase
```
README.md Yenileme:
├── Animated GIF demo
├── Architecture diagram (Mermaid)
├── Benchmark results badge
├── Quick start (30 saniye)
├── API documentation link
└── Contributing guide
```

### 13.3 Tasklar
```
[ ] 13.1.1 README.md yenileme (GIF demo)
[ ] 13.1.2 Architecture diagram güncelleme
[ ] 13.1.3 CONTRIBUTING.md
[ ] 13.1.4 CODE_OF_CONDUCT.md
[ ] 13.2.1 GitHub Pages setup
[ ] 13.2.2 API docs (Swagger export)
[ ] 13.3.1 Medium Part 1 draft
[ ] 13.3.2 Medium Part 2 draft
[ ] 13.3.3 Medium Part 3 draft
[ ] 13.4.1 Demo video (Loom/YouTube)
[ ] 13.4.2 LinkedIn post serisi
[ ] 13.4.3 Twitter/X thread
```

---

## HAFTALIK UYGULAMA PLANI

### Hafta 1-2: LangGraph Core (FAZ 7)
```
Gün 1-2: StateGraph + Agent skeleton'ları
Gün 3-4: Supervisor + Researcher Agent
Gün 5-6: Analyst + Writer Agent
Gün 7-8: Critic Agent + Workflow entegrasyonu
Gün 9-10: Streamlit entegrasyonu + testler
```

### Hafta 3: FastAPI Foundation (FAZ 8)
```
Gün 1-2: FastAPI boilerplate + schemas
Gün 3-4: Query/Compare endpoints
Gün 5: Auth middleware
Gün 6-7: Rate limiting + documentation
```

### Hafta 4: Dynamic Pipeline Start (FAZ 9)
```
Gün 1-2: Scraper altyapısı
Gün 3-4: Haber scraper
Gün 5-7: TBMM entegrasyonu (araştırma + PoC)
```

### Hafta 5: Monitoring + Pipeline (FAZ 9-10)
```
Gün 1-2: LangSmith entegrasyonu
Gün 3-4: Dashboard
Gün 5-7: Pipeline completion + cron
```

### Hafta 6: User Features (FAZ 11)
```
Gün 1-2: Alert sistemi
Gün 3-4: E-posta entegrasyonu
Gün 5-7: Rapor oluşturucu
```

### Hafta 7: Benchmark + Showcase (FAZ 12-13)
```
Gün 1-3: Benchmark suite
Gün 4-5: Documentation
Gün 6-7: Medium Part 1 + demo video
```

---

## BAŞARI KRİTERLERİ

### MVP Hedefleri
| Hedef | CV | SaaS | Deadline |
|-------|:--:|:----:|----------|
| LangGraph multi-agent çalışıyor | ✓ | | Hafta 2 |
| FastAPI 5+ endpoint aktif | ✓ | ✓ | Hafta 3 |
| Günlük haber akışı | | ✓ | Hafta 5 |
| LangSmith traces görünür | ✓ | | Hafta 5 |
| Alert sistemi çalışıyor | | ✓ | Hafta 6 |
| 1 Medium makalesi yayında | ✓ | | Hafta 7 |
| 50+ GitHub star | ✓ | | Hafta 8 |

### Stretch Goals
| Hedef | Kategori |
|-------|----------|
| TBMM tutanakları entegre | SaaS |
| 100+ GitHub star | CV |
| PyPI paketi | CV |
| İlk ödeme yapan kullanıcı | SaaS |
| Conference talk proposal | CV |

---

## GELİR MODELİ YOLU HARİTASI

```
┌─────────────────────────────────────────────────────────┐
│                  GELİR YOLU HARİTASI                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  AÇIK KAYNAK (Şimdi)                                    │
│  └── GitHub'da görünürlük + CV                         │
│           │                                             │
│           ▼                                             │
│  FREEMİUM LANSMAN (Hafta 8)                            │
│  ├── Ücretsiz: 10 sorgu/gün                            │
│  └── Waitlist: Pro tier                                │
│           │                                             │
│           ▼                                             │
│  PRO TIER LANSMAN (Hafta 12)                           │
│  ├── 99 TL/ay                                          │
│  ├── API erişimi                                       │
│  └── Alert sistemi                                     │
│           │                                             │
│           ▼                                             │
│  ENTERPRİSE OUTREACH (Hafta 16+)                       │
│  ├── Medya kuruluşları                                 │
│  ├── STK'lar                                           │
│  └── White-label teklifleri                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## TEKNOLOJİ ÖĞRENİM HARİTASI

| Teknoloji | Faz | CV Etkisi | SaaS Etkisi | Öğrenme Süresi |
|-----------|-----|:---------:|:-----------:|----------------|
| **LangGraph** | 7 | ⭐⭐⭐⭐⭐ | ⭐⭐ | 1 hafta |
| **FastAPI** | 8 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 3-4 gün |
| **Scrapy/BS4** | 9 | ⭐⭐ | ⭐⭐⭐⭐ | 2-3 gün |
| **LangSmith** | 10 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 1 gün |
| **SendGrid** | 11 | ⭐ | ⭐⭐⭐⭐ | 1 gün |
| **Technical Writing** | 13 | ⭐⭐⭐⭐ | ⭐⭐⭐ | Sürekli |

---

## TOPLAM TASK SAYISI

| Faz | Task Sayısı | Öncelik |
|-----|:-----------:|:-------:|
| FAZ 7 (LangGraph) | 14 | 🔴 |
| FAZ 8 (FastAPI) | 17 | 🔴 |
| FAZ 9 (Pipeline) | 13 | 🟠 |
| FAZ 10 (Monitoring) | 12 | 🟠 |
| FAZ 11 (Features) | 12 | 🟡 |
| FAZ 12 (Benchmark) | 10 | 🟡 |
| FAZ 13 (Showcase) | 13 | 🟢 |
| **TOPLAM** | **91** | |

---

*Son Güncelleme: 26 Şubat 2026*
*Versiyon: 2.0 (CV + SaaS Sentezi)*
