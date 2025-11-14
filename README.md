# 🗳️ Politika Asistanı | Turkish Politics AI Assistant

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-🦜-green.svg)](https://langchain.com/)
[![Gemini](https://img.shields.io/badge/Gemini-API-orange.svg)](https://ai.google.dev/)
[![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)]()

**Türkiye'nin İlk Konuşan Parti Platformu**

[Demo](#-demo) • [Özellikler](#-özellikler) • [Mimari](#-teknik-mimari) • [Kurulum](#-kurulum) • [Roadmap](#-roadmap)

</div>

---

## 📖 Proje Hakkında

**Politika Asistanı**, vatandaşların siyasi partilerin politikalarını anlamasını ve karşılaştırmasını sağlayan yapay zeka destekli bir platformdur. Her siyasi parti, kendi AI temsilcisi aracılığıyla vatandaşlarla konuşur.

### 💡 Motivasyon

- 🗳️ **Seçmen Bilgilenme Sorunu**: Vatandaşlar partilerin politikalarını anlamakta zorlanıyor
- 📚 **Erişilebilirlik**: 400+ sayfalık parti programlarını okumak pratik değil
- 🤝 **Karşılaştırma Zorluğu**: Partilerin aynı konudaki görüşlerini yan yana görmek zor
- 🇹🇷 **Türkçe AI Açığı**: Türk siyasetine özel, konuşma dilinde çalışan AI yok

### 🎯 Çözüm

Konuşma tabanlı AI asistanları ile parti politikalarını erişilebilir kılmak. Her parti, kendi resmi dokümanları ile beslenen bir AI temsilcisine sahip.

---

## ✨ Özellikler

### 🤖 Multi-Agent Sistem
- **Her Parti Bir Agent**: AKP, CHP, MHP, İYİ Parti AI temsilcileri
- **Parti Tüzükleri & Programlar**: RAG sistemi ile beslenmiş knowledge base
- **Konuşma Tabanlı**: Doğal dilde soru-cevap

### 💬 Kullanım Senaryoları

```
Kullanıcı: "CHP'nin ekonomi politikası nedir?"
AI: [CHP parti programından ilgili bölümleri analiz ederek cevap verir]

Kullanıcı: "AKP ve CHP'nin eğitim politikalarını karşılaştır"
AI: [Her iki partinin politikalarını yan yana sunar]

Kullanıcı: "Hangi partiler LGBT haklarını destekliyor?"
AI: [İlgili parti programlarından bilgi sentezler]
```

### 🎨 Planlanan Özellikler (v1.0)
- ✅ Multi-party RAG system
- ✅ Turkish language optimization
- ⏳ Streamlit UI
- ⏳ Comparative analysis mode
- ⏳ Source citation & transparency
- ⏳ Conversation memory
- ⏳ Policy timeline tracking

---

## 🏗️ Teknik Mimari

### Tech Stack

```
┌─────────────────────────────────────────────────┐
│                  FRONTEND                        │
│         Streamlit (MVP) / React (v2.0)          │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│              ORCHESTRATION LAYER                 │
│    LangGraph (Multi-Agent Coordination)         │
│    - Party Agent Router                          │
│    - Comparison Agent                            │
│    - Citation Agent                              │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│                 RAG PIPELINE                     │
│    LangChain + Gemini 1.5 Flash                 │
│    - Document Loaders                            │
│    - Text Splitters (Turkish-optimized)         │
│    - Prompt Templates                            │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│              VECTOR DATABASE                     │
│    Chroma (MVP) / Pinecone (Production)         │
│    - Turkish Embeddings (BGE-M3)                │
│    - Per-party collections                       │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│                DATA SOURCES                      │
│    - Parti Tüzükleri (PDF)                      │
│    - Seçim Beyannameleri                         │
│    - Parti Programları                           │
│    - Resmi Açıklamalar (gelecekte)              │
└─────────────────────────────────────────────────┘
```

### Core Technologies

| Component | Technology | Why? |
|-----------|-----------|------|
| **LLM** | Gemini 1.5 Flash | Turkish language support, fast, cost-effective |
| **Embeddings** | BGE-M3 Turkish | Best Turkish semantic understanding |
| **Vector DB** | Chroma → Pinecone | Easy prototyping → Production scale |
| **Framework** | LangChain | Industry standard RAG framework |
| **Orchestration** | LangGraph | Multi-agent coordination |
| **Frontend** | Streamlit → React | Rapid MVP → Production UI |
| **Deployment** | Docker + AWS | Scalable, production-ready |

---

## 🚀 Kurulum

### Prerequisites

```bash
Python 3.10+
Git
Gemini API Key
```

### Installation

```bash
# 1. Clone repository
git clone https://github.com/barancanercan/Turkish-Government-Intelligence-Hub.git
cd Turkish-Government-Intelligence-Hub

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 5. Run MVP
python main.py
```

### Environment Variables

```bash
# .env
GEMINI_API_KEY=your_gemini_api_key_here
# PINECONE_API_KEY=your_pinecone_key  # For production
```

---

## 📂 Proje Yapısı

```
Turkish-Government-Intelligence-Hub/
├── data/
│   ├── chp.pdf                 # CHP Parti Tüzüğü
│   ├── akp.pdf                 # AKP Parti Tüzüğü (gelecek)
│   └── ...
├── src/
│   ├── agents/                 # Multi-agent logic (gelecek)
│   ├── rag/                    # RAG pipeline (gelecek)
│   └── utils/                  # Helper functions
├── chroma_db/                  # Vector database (local)
├── main.py                     # Current MVP
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🎯 Roadmap

### Phase 1: MVP (Current - Week 1-2) ✅
- [x] Single party RAG system (CHP)
- [x] Basic Q&A functionality
- [x] Turkish embedding model integration
- [x] Chroma vector database
- [ ] Streamlit UI

### Phase 2: Multi-Party System (Week 3-4)
- [ ] Add 3+ party agents (AKP, MHP, İYİ Parti)
- [ ] LangGraph multi-agent orchestration
- [ ] Comparative analysis feature
- [ ] Source citation system

### Phase 3: Advanced Features (Week 5-6)
- [ ] Conversation memory
- [ ] Advanced prompt engineering
- [ ] LoRA fine-tuning for party-specific language
- [ ] Performance optimization (<800ms latency)

### Phase 4: Production (Week 7-8)
- [ ] Migrate to Pinecone
- [ ] FastAPI backend
- [ ] React frontend
- [ ] Docker containerization
- [ ] AWS deployment
- [ ] Monitoring & logging

### Future Vision
- [ ] Real-time policy updates
- [ ] Integration with official party APIs
- [ ] Mobile app
- [ ] Multilingual support (English, Kurdish)
- [ ] Election prediction analytics

---

## 📊 Demo

> 🚧 **Demo coming soon!** Streamlit UI in development.

### Current CLI Demo

```bash
$ python main.py

============================================================
CHP Parti Tüzüğü - Soru-Cevap Sistemi
============================================================

Sorunuz: Parti genel başkanı nasıl seçilir?

Aranıyor: 'Parti genel başkanı nasıl seçilir?'
Benzerlik hesaplanıyor...
✅ En benzer 3 bölüm bulundu
Gemini'ye gönderiliyor...

============================================================
Cevap:
============================================================
Parti Genel Başkanı, Kurultay tarafından gizli oyla ve...
```

---

## 🤝 Katkıda Bulunma

Bu proje açık kaynak değildir, ancak feedback'lere açıktır. Öneriniz varsa issue açabilirsiniz.

---

## 📜 License

Bu proje özel lisans altındadır. Ticari kullanım için izin gereklidir.

---

## 👨‍💻 Geliştirici

**Baran Can Ercan**  
Senior Data Scientist | AI/ML Engineer

- 🌐 [LinkedIn](https://www.linkedin.com/in/barancanercan)
- 📝 [Medium](https://barancanercan.medium.com)
- 📧 barancanercan@gmail.com
- 💼 [GitHub](https://github.com/barancanercan)

---

## 🙏 Acknowledgments

- **Turkish NLP Community** - Turkish embedding models
- **LangChain** - RAG framework
- **Google Gemini Team** - API access
- **Ankara Metropolitan Municipality** - Domain expertise in public sector AI

---

## ⚖️ Disclaimer

Bu proje, siyasi partilerin resmi görüşlerini temsil etmez. AI yanıtları, parti dokümanlarına dayansa da hata içerebilir. Resmi bilgi için partilerin web sitelerini ziyaret edin.

---

<div align="center">

**Türkiye'de Siyasi Katılımı Artıran AI Platformu**

⭐ Star this repo if you find it useful!

</div>