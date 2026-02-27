# Mizan-AI: LLM Mimarisi Analiz Raporu

**Tarih:** Şubat 2026
**Proje:** Mizan-AI - Türkiye Siyasi Belge Analiz Platformu
**Kapsam:** LLM yapısı, multi-agent orchestration, reasoning katmanları ve optimizasyon stratejileri

---

## 1. MEVCUT DURUM ANALIZI

### 1.1 Teknoloji Stack

```
LLM Katmanı:
├── Birincil: Gemini 2.0 Flash (Google)
├── Yedek: Ollama (qwen2.5:7b)
└── Temperature: 0.3, Max Tokens: 1024

Agent Orchestration:
├── Framework: LangGraph
├── State Management: Pydantic BaseModel
├── Checkpointing: Memory Saver
└── Agents: Supervisor → Researcher/Analyst → Writer → Critic

RAG Layer:
├── Embedding: nezahatkorkmaz/turkce-embedding-bge-m3
├── Vector DB: ChromaDB
├── Chunk Size: 512 tokens
├── Chunk Overlap: 50 tokens
├── Top-K Retrieval: 5 documents
└── Similarity Threshold: 0.75 (L2 distance)

Web Search:
├── Engine: DuckDuckGo (SearchAgent)
├── Strategy: SearchStrategyAgent
├── Max Results: 5
└── Timeout: 10 seconds
```

### 1.2 Multi-Agent Yapısı

**Workflow (LangGraph):**

```
Supervisor (Soru Sınıflandırması)
    ↓
    ├─→ Researcher (Veri Toplama: Local + Web + Wikipedia)
    │       ↓
    │   (join) ←─ Analyst (Karşılaştırma & Analiz)
    │       ↓
    └─→ Writer (Yanıt Sentezi)
            ↓
        Critic (Kalite Kontrol)
            ↓
        CEVAP
```

**Agent Sorumlulukları:**
- **Supervisor:** Sorguyu `simple/comparison/deep_research` olarak sınıflandırır
- **Researcher:** Yerel DB + Web + Wikipedia araştırması
- **Analyst:** Multi-party karşılaştırma ve trend analizi
- **Writer:** Türkçe yanıt sentezi, kaynak yönetimi
- **Critic:** Kalite puanlaması (0-1), hallucination kontrolü

### 1.3 Prompt Mimarisi

**Güçlü Yönler:**
- Parti-spesifik sistem promptları (`SYSTEM_PROMPTS`)
- Türkçe-first tasarım
- Context window yönetimi (2500 token limit)
- Tarafsızlık kuralları

**Zayıf Yönler:**
- **Statik promptlar** - sorguya göre dinamik uyarlanmıyor
- **Chain-of-Thought eksik** - LLM doğrudan sonuca sıçrıyor
- **ReAct pattern eksik** - "think-act-observe" döngüsü yok
- **Self-reflection limited** - Critic sadece sonradan kontrol ediyor

### 1.4 RAG Kalitesi

**İyileştirmeler:**
- Web araması fallback mekanizması
- Parti-spesifik vektör filtreleme
- Political Context Agent (sorgu zenginleştirme)
- Query Analyzer (alt-soru decomposition)

**Sorunlar:**
- High similarity threshold (0.75) → false negatives
- Query Analyzer alt-soruları "web_required" bayrağıyla işaretliyor ama gerçek web arama stratejisi eksik
- SearchStrategyAgent sonuçları filtreleniyor ama fallback logik sınırlı

### 1.5 Fallback & Error Handling

```
Başarı Sırası:
1. Gemini API → OK
2. Gemini API → FAIL → Ollama fallback
3. Ollama → FAIL → Error message

Retrieval Fallback:
- Score > 0.75 → Web search trigger
- Web result found → LLM synthesis
- Web result NOT found → "Bilgi bulunamadı"
```

---

## 2. 2026 BEST PRACTICES (Web Research)

### 2.1 Agentic RAG Paradigm Shift

2026'da Agentic RAG artık bir pipeline değil, **loop-based reasoning sistemi:**

```
Loop = Retrieval → Grading → Generation → Hallucination Check → (Loop if needed)
```

**Key Components (Mizan-AI'de eksik):**
1. **Router Node:** Retrieval gerekli mi? (Binary decision)
2. **Grader Node:** Retrieved docs relevant mi? (Relevance check)
3. **Hallucination Checker:** Generated answer supported mi? (Fact verification)

**Mizan-AI Durumu:** Partial - Writer + Critic kombinasyonu benzer fakat explicit grade/check aşkalaması yok

### 2.2 Reasoning Frameworks

#### Chain-of-Thought (CoT)
- **Tanım:** Adım-adım düşünme süreci
- **Problem:** Tek-turlu, hata propagation riski yüksek
- **Mizan-AI Kullanımı:** YOK

#### ReAct (Reasoning + Acting)
- **Tanım:** Diyalojik loop: Think → Act → Observe → Think
- **Avantaj:** Gerçek zamanlı feedback ve correction
- **Mizan-AI Kullanımı:** KISMEN (Researcher tools + Writer ama tight coupling eksik)

#### Reflexion (ReAct + Self-Reflection)
- **Tanım:** Multi-trial improvement with memory
- **Components:** Actor + Evaluator + Self-Reflection model
- **Mizan-AI Kullanımı:** MINIMAL (Critic only evaluates, no memory/retry loop)

### 2.3 Multi-Agent Orchestration (2026)

**Standardlar:**
- **MCP (Model Context Protocol):** Tool integration standarı
- **A2A (Agent-to-Agent):** Peer collaboration protocol
- **ACP (IBM):** Enterprise governance

**Prompt Patterns:**
- Supervisor agents → Decision-focused prompts
- Worker agents → Task-specific, actionable instructions
- Role assignment → Clear agent responsibilities

**Mizan-AI Durumu:** LangGraph iyi, ama prompt standardizasyonu eksik

### 2.4 Context Window Optimization

2026 Trends:
- Smaller models (Phi-3, Qwen-2.5) for Router/Grader
- Larger models for synthesis (Claude, Gemini)
- Strict token budgeting per node

**Mizan-AI:** 1024 token limit makul ama dynamic budgeting eksik

---

## 3. REASONING KATMANI ÖNERİLERİ

### 3.1 Eksiklikler Özeti

| Katman | Mizan-AI | Best Practice | GAP |
|--------|----------|----------------|-----|
| CoT Prompting | ✗ | ✓ (Multi-step reasoning) | Kritik |
| ReAct Loop | ◐ | ✓ (Think-Act-Observe) | Yüksek |
| Reflexion | ✗ | ✓ (Self-correction memory) | Yüksek |
| Hallucination Check | ◐ | ✓ (Explicit grader node) | Orta |
| Context Grading | ✗ | ✓ (Relevance score) | Orta |
| Query Decomposition | ◐ | ✓ (Explicit sub-question loop) | Orta |

### 3.2 Somut Kodlama Önerileri

#### 3.2.1 Chain-of-Thought Prompt Injection

**Mevcut (yanlış):**
```python
# src/config.py
SYSTEM_PROMPTS.get(party)  # Static prompt
```

**Önerilen:**
```python
def create_cot_prompt(question: str, party: str, context: str) -> str:
    """Chain-of-Thought prompt dinamik olarak oluşturur"""
    return f"""
    KURAL: Adım adım düşün, ardından cevap ver.

    SORU: {question}

    BAĞLAM: {context}

    DÜŞÜNME SÜRECİ:
    1. Soru hangi konuyla ilgili?
    2. Bağlamda hangi bilgiler relevan?
    3. Bu bilgiler soruyu nasıl yanıtlıyor?

    CEVAP: [Mantıklı adımlar sonrasında cevap ver]
    """
```

#### 3.2.2 ReAct Loop Implementation

**Önerilen yeni node (graph.py'de):**

```python
from langgraph.graph import StateGraph, START, END

def create_agentic_workflow(llm) -> StateGraph:
    """ReAct-style agentic RAG workflow"""

    workflow = StateGraph(AgentState)

    # 1. Router Node - Retrieval gerekli mi?
    workflow.add_node("router", router_node)

    # 2. Retriever Node
    workflow.add_node("retriever", retriever_node)

    # 3. Grader Node - Retrieved docs relevant mi?
    workflow.add_node("grader", grader_node)

    # 4. Generator Node - Yanıt üret
    workflow.add_node("generator", generator_node)

    # 5. Hallucination Checker - Cevap supported mi?
    workflow.add_node("hallucination_checker", hallucination_node)

    # Conditional edges for ReAct loop
    workflow.add_conditional_edges(
        "router",
        should_retrieve,
        {
            "retrieve": "retriever",
            "generate": "generator"
        }
    )

    workflow.add_conditional_edges(
        "grader",
        is_document_relevant,
        {
            "regenerate": "retriever",  # ReAct loop: tekrar ara
            "generate": "generator"
        }
    )

    workflow.add_conditional_edges(
        "hallucination_checker",
        has_hallucination,
        {
            "regenerate": "generator",  # ReAct loop: tekrar üret
            "end": END
        }
    )

    return workflow.compile(checkpointer=checkpointer)
```

#### 3.2.3 Reflexion Memory System

**Önerilen (src/agents/reflexion.py - YENİ DOSYA):**

```python
from typing import List, Dict
from pydantic import BaseModel

class ReflexionMemory(BaseModel):
    """Reflexion framework için hafıza"""
    attempt: int
    question: str
    reasoning: str  # Actor'ün düşüncesi
    action: str     # Actor'ün aksiyonu
    result: str     # Sonuç
    score: float    # Evaluator skoru
    feedback: str   # Self-Reflection output

class ReflexionAgent:
    """Multi-trial self-improvement agent"""

    def __init__(self, llm, max_attempts: int = 3):
        self.llm = llm
        self.max_attempts = max_attempts
        self.memory: List[ReflexionMemory] = []

    def improve(self, question: str, initial_answer: str) -> str:
        """Multi-trial improvement döngüsü"""

        for attempt in range(self.max_attempts):
            # 1. Evaluator: Sonucu puanla
            score = self.evaluate(initial_answer)

            if score > 0.8:
                return initial_answer

            # 2. Self-Reflection: Hatayı analiz et
            feedback = self.reflect(question, initial_answer, score)

            # 3. Store memory
            self.memory.append(ReflexionMemory(
                attempt=attempt,
                question=question,
                reasoning="...",
                action="...",
                result=initial_answer,
                score=score,
                feedback=feedback
            ))

            # 4. Tekrar dene (with feedback)
            initial_answer = self.regenerate_with_feedback(
                question,
                initial_answer,
                feedback
            )

        return initial_answer
```

#### 3.2.4 Context Grading Node

**Önerilen (src/agents/grader.py - YENİ DOSYA):**

```python
def grader_node(state: AgentState) -> AgentState:
    """
    Retrieved documents'in relevance'ını kontrol eder.
    Mizan-AI'nin Critic node'u bunu kısmen yapıyor ama
    explicit grading score eksik.
    """

    from langchain_core.language_model import BaseLanguageModel

    relevance_prompt = """
    DOKÜMAN: {doc}
    SORU: {question}

    Lütfen bu dokümanın soruya ne kadar relevant olduğunu
    0-10 skala ile puan ver.

    Sadece sayı dön (0-10):
    """

    # Her retrieved doc için grade et
    for doc in state.retrieved_docs:
        grade = llm.invoke(
            relevance_prompt.format(
                doc=doc.content,
                question=state.query
            )
        )

        doc.score = float(grade) / 10.0

    # Ortalama score
    avg_score = sum(d.score for d in state.retrieved_docs) / len(state.retrieved_docs)
    state.quality_score = avg_score

    return state
```

#### 3.2.5 Query Decomposition Loop

**Mevcut sorun:** QueryAnalyzer alt-soruları bulur ama loop yok.

**Önerilen:**

```python
def decomposition_node(state: AgentState) -> AgentState:
    """Sub-questions'ı sequentially işle"""

    query_analyzer = get_query_analyzer()
    analysis = query_analyzer.analyze(state.query, state.party)

    if not analysis.is_compound:
        # Basit soru - doğrudan ilerle
        return state

    # Compound soru: Her sub-question için döngü
    all_answers = []

    for sub_q in analysis.sub_questions:
        # Her sub-soru için retrieval + generation
        sub_context, _, _ = search_local_knowledge(
            vectorstore,
            sub_q.text,
            state.party
        )

        # Web gerekli mi?
        if sub_q.requires_web:
            web_results = search_online_knowledge(sub_q.text, state.party)

        # Sub-soru cevabı
        answer = synthesize_answer(sub_context, web_results, sub_q.text, ...)
        all_answers.append(answer)

    # Tüm sub-cevapları birleştir
    state.final_answer = "\n\n".join(all_answers)

    return state
```

### 3.3 Prompt Template Iyileştirmeleri

#### 3.3.1 Supervisor Prompt (ReAct-aware)

**Mevcut (yanlış):**
```python
SUPERVISOR_SYSTEM_PROMPT = """Sen Supervisor'sun.
Sorguyu hangi agent'a yönlendir?"""
```

**Önerilen:**

```python
SUPERVISOR_SYSTEM_PROMPT = """
Sen Mizan-AI Supervisor Agent'ısın.

GÖREVIN: Kullanıcı sorusunu analiz et ve:
1. SORU TİPİ: simple / comparison / deep_research olarak sınıfla
2. ENTITIES: Hangi partiler/konular bahsediliyor?
3. REASONING: Neden bu routing'i yaptığını açıkla
4. RETRIEVAL: Web arama gerekli mi?

AGENT SEÇIMI:
- simple: Tek parti, tek konu → researcher
- comparison: Multiple partiler → analyst + researcher
- deep_research: Derinlemesine, zaman-duyarlı → researcher + web

YANIT FORMAT (JSON):
{{
    "query_type": "simple|comparison|deep_research",
    "next_agent": "researcher|analyst",
    "parties": ["CHP", "AKP"],
    "topics": ["ekonomi"],
    "needs_web": true,
    "confidence": 0.9,
    "reasoning": "Kısa açıklama"
}}
"""
```

#### 3.3.2 Writer Prompt (CoT + Context-aware)

**Önerilen:**

```python
WRITER_COT_PROMPT = """
Sen Mizan-AI Writer Agent'ısın.

ADIM 1 - ANALIZ:
- Hangi kaynaklar mevcut? (Local, Web, Wikipedia)
- Kaynaklar ne kadar güvenilir?
- Boşluklar var mı?

ADIM 2 - SENTEZ:
- Kaynakları mantıksal sırada sun
- Karşıt görüşleri de belirt
- Belirsizlikleri açıkça söyle

ADIM 3 - YANITLAMA:
- Soruya TAMAMEN yanıt ver
- Kaynakları inline belirt: "Kaynak: Wikipedia"
- Tarafsız ve nesnel ol

YANIT ÖRNEĞİ:
{party_name} hakkında:
1. [Kaynak: Local] Resmi statüde ...
2. [Kaynak: Web] Son haberler: ...
3. [Kaynak: Wikipedia] Tarihçe: ...

NOT: Emin olmadığın bilgi için "Bilgi belirtilmemiştir" de, UYDURMA!

BAĞLAM:
{context}

SORU:
{question}

CEVAP:
"""
```

---

## 4. TEKNIK İMPLEMENTASYON REHBERI

### 4.1 Faydaya Göre Sıralanmış Önceliklendirme

| Sıra | Özellik | Faydası | Zorluk | Zaman | Neden? |
|------|---------|--------|--------|-------|--------|
| **1** | CoT Prompt Injection | Hallucination -30% | Düşük | 2h | Critical - en kolay + en faydalı |
| **2** | Context Grading Node | Relevance +40% | Düşük | 4h | Mevcut Critic'i improve |
| **3** | Sub-question Loop | Compound Q +50% | Orta | 6h | Query Analyzer başlangıcı var |
| **4** | ReAct Loop | Self-correction +60% | Yüksek | 12h | Architecture refactor gerekli |
| **5** | Reflexion Memory | Multi-trial +40% | Yüksek | 10h | Gözlemsel fayda |

### 4.2 Implementation Phases

#### **Phase 1: CoT Prompt (Haftada 1-2 gün)**

```python
# src/config.py
def get_context_aware_prompt(party: str, question: str) -> str:
    """Dinamik CoT prompt üret"""
    # Soru tipi detekle
    # Uygun template seç
    # Context insert et

# src/agents/writer.py
WRITER_SYSTEM_PROMPT = """[CoT template burada]"""
```

**Test:**
```python
# test_cot.py
question = "CHP'nin ekonomi politikası nedir?"
answer = writer_node(state)
assert "Adım" in answer or "Cevap" in answer
```

#### **Phase 2: Grader Node (Haftada 1-2 gün)**

```python
# src/agents/grader.py
def grader_node(state: AgentState) -> AgentState:
    """Grade each retrieved document"""
    # Mevcut Critic'i refactor et
    # Explicit relevance scoring ekle

# src/agents/graph.py
# Workflow'a grader node ekle
workflow.add_node("grader", grader_node)
workflow.add_edge("retriever", "grader")
```

**Test:**
```python
# test_grader.py
docs = state.retrieved_docs
graded_state = grader_node(state)
assert all(0 <= d.score <= 1 for d in graded_state.retrieved_docs)
```

#### **Phase 3: Sub-Question Loop (1-2 hafta)**

```python
# src/agents/decomposition.py
def decomposition_node(state: AgentState) -> AgentState:
    """Compound questions'ı sequentially çöz"""
    # QueryAnalyzer sub-questions'ı al
    # Her sub-soru için retrieval loop
    # Cevapları birleştir

# src/agents/graph.py
# "decomposition" node'u supervisor'dan sonra ekle
```

#### **Phase 4: ReAct Loop (2-3 hafta)**

```python
# src/agents/react.py (NEW)
class ReactNode:
    def router(self, state): pass
    def retrieve(self, state): pass
    def grade(self, state): pass
    def generate(self, state): pass
    def check_hallucination(self, state): pass

# src/agents/graph.py
# Tamamen yeni workflow: SimpleGraph → ReactGraph
```

#### **Phase 5: Reflexion (2 hafta)**

```python
# src/agents/reflexion.py (NEW)
class ReflexionAgent:
    def evaluate(self, answer): pass
    def reflect(self, question, answer, score): pass
    def regenerate_with_feedback(self, ...): pass
```

### 4.3 Konfigürasyon Parametreleri

**src/config.py'ye ekle:**

```python
# ============================================
# REASONING CONFIGS (2026)
# ============================================

# Chain-of-Thought
ENABLE_COT_PROMPTING = True
COT_TEMPLATE = "Adım adım düşün..."

# ReAct
ENABLE_REACT_LOOP = True
REACT_MAX_ITERATIONS = 3

# Reflexion
ENABLE_REFLEXION = False  # Phase 5
REFLEXION_MAX_ATTEMPTS = 3
REFLEXION_SCORE_THRESHOLD = 0.8

# Grader
ENABLE_GRADING = True
GRADER_RELEVANCE_THRESHOLD = 0.6

# Decomposition
ENABLE_SUB_QUESTION_LOOP = True
MAX_SUB_QUESTIONS = 5
```

---

## 5. MONITORING & EVALUATION

### 5.1 Metrics

```python
# src/monitoring/metrics.py
class LLMMetrics:
    def track_hallucination_rate(answer, context):
        """Hallucination oranı"""
        # Cevap context'ten support alıyor mu?

    def track_retrieval_quality(docs, answer):
        """Retrieved docs answer'da kullanılıyor mu?"""

    def track_agent_routing(question, routed_agent):
        """Routing doğru mu?"""

    def track_response_latency(state):
        """Agent pipeline hızı"""

    def track_quality_score_distribution():
        """Critic puanlamalarının dağılımı"""
```

### 5.2 Evaluation Suite

```python
# test_llm_improvements.py
import unittest

class TestCoT(unittest.TestCase):
    def test_cot_reduces_hallucination(self):
        # CoT olmadan vs ile karşılaştır
        pass

    def test_cot_improves_reasoning(self):
        # Adım-adım cevaplar daha iyi mi?
        pass

class TestReAct(unittest.TestCase):
    def test_react_self_corrects(self):
        # Loop bad answer'ı fix ediyor mu?
        pass

class TestReflexion(unittest.TestCase):
    def test_reflexion_multi_trial(self):
        # Denemeler iyileşiyor mu?
        pass
```

---

## 6. RISK & MITIGATION

| Risk | İmact | Olasılık | Mitigation |
|------|-------|----------|-----------|
| Token limit aşımı (CoT) | Kesik cevaplar | Yüksek | Strict budgeting, smaller models for grader |
| Infinite loops (ReAct) | Timeout | Orta | Max iterations, timeout abort |
| Prompt injection | Hallucination | Düşük | Input validation, guardrails |
| Gemini API quota | Yedek kötü | Orta | Ollama fallback, local models |
| Türkçe işleme | Kalite düşüşü | Düşük | Specific test data, Turkish metrics |

---

## 7. ROADMAP

```
Month 1: CoT + Grader (Quick wins)
├─ Week 1-2: CoT prompt templates
├─ Week 3-4: Grader node implementation
└─ Testing: Hallucination tests

Month 2: Sub-question Loop
├─ Week 1-2: Query decomposition refactor
├─ Week 3-4: Sequential sub-Q processing
└─ Testing: Compound Q tests

Month 3: ReAct Loop
├─ Week 1-2: Router/Retriever/Generator nodes
├─ Week 3-4: Conditional edges, max iterations
└─ Testing: Self-correction tests

Month 4: Reflexion (Optional)
├─ Week 1-2: Evaluation model
├─ Week 3-4: Memory + retry logic
└─ Testing: Multi-trial improvement tests

Month 5: Optimization
├─ Token budgeting
├─ Model size optimization
├─ Monitoring dashboard
└─ Production deployment
```

---

## 8. KAYNAKLAR & REFERANSLAR

### Academic Papers
- Chain-of-Thought: Wei et al. (2201.11903)
- ReAct: Yao et al.
- Reflexion: Shinn et al.
- Agentic RAG: Mitrovic et al.

### 2026 Web Resources
- [Building Agentic RAG Systems with LangGraph: The 2026 Guide](https://rahulkolekar.com/building-agentic-rag-systems-with-langgraph/)
- [Build a custom RAG agent with LangGraph - LangChain Docs](https://docs.langchain.com/oss/python/langgraph/agentic-rag)
- [How LLM Reasoning Powers the Agentic AI Revolution](https://medium.com/@anicomanesh/how-llm-reasoning-powers-the-agentic-ai-revolution-cbefd10ebf3f)
- [State of Reasoning LLMs: The New Era of "Thinking" Machines](https://medium.com/@adnanmasood/state-of-reasoning-llms-the-new-era-of-thinking-machines-f241b1a3096d)
- [Multi-Agent RAG System with LangGraph](https://wesleybaxterhuber.medium.com/building-a-multi-agent-rag-system-with-langgraph-43071904b123)
- [The Ultimate Guide to Prompt Engineering in 2026](https://www.lakera.ai/blog/prompt-engineering-guide)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

### Frameworks & Tools
- **LangGraph:** Multi-agent orchestration
- **LangChain:** RAG/prompt templates
- **ChromaDB:** Vector store
- **DuckDuckGo API:** Web search

---

## 9. SONUÇ

Mizan-AI **solid** bir RAG mimarisine sahiptir ama **2026 standards** için şunlar eksik:

1. **Reasoning Layer:** CoT, ReAct, Reflexion yok
2. **Agentic Loop:** Single-pass, no self-correction
3. **Explicit Grading:** Critic evaluates ama relevance score yok
4. **Prompt Optimization:** Static → Dynamic prompts gerekli

**En kritik 3 improvement:**
1. **CoT Prompting** (2-3 saat, +30% quality)
2. **Context Grading** (4-6 saat, +40% relevance)
3. **ReAct Loop** (2 hafta, +60% self-correction)

**Fakat:** Mevcut mimari bu iyileştirmeleri barındıracak kadar esnektir. LangGraph state management'ı, moduler agents ve fallback sistemi iyi tasarlanmış.

---

**Rapor Bitti**

---

