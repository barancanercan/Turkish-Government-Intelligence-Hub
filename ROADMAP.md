# MIZAN-AI Master Roadmap

**Tarih:** 27 Subat 2026
**Versiyon:** 2.0
**Hedef:** Production-Ready Multi-Agent T-RAG Platform

---

## EXECUTIVE SUMMARY

3 mimari analiz raporunun (llm.md, backend.md, frontend.md) sentezi sonucu belirlenen oncelikli aksiyonlar.

### Kritik Bulgular

| Alan | Mevcut | Hedef | Oncelik |
|------|--------|-------|---------|
| LLM Reasoning | Yok | CoT + ReAct | KRITIK |
| Streaming | Yok | SSE/WebSocket | KRITIK |
| Cache | In-Memory | Redis | YUKSEK |
| Auth | Temel | Production-grade | YUKSEK |
| Monitoring | Yok | Prometheus + Grafana | ORTA |

---

## FAZ 1: KRITIK DUZELTMELER (1-2 Hafta)

### 1.1 LLM Reasoning Katmani

**Sorun:** "CHP genel baskani kimdir?" sorusuna "nasil secilir" cevabi veriyor.

**Cozum:** Chain-of-Thought prompting

```python
# src/core/reasoning.py

REASONING_PROMPT = """
Adim adim dusun:

1. SORU ANALIZI: Kullanici ne soruyor?
   - "kimdir" = isim/kisi bilgisi isteniyor
   - "nedir" = tanim/aciklama isteniyor
   - "nasil" = surec/yontem isteniyor

2. BAGLAM KONTROLU: Verilen baglamda bu bilgi var mi?

3. YANIT OLUSTURMA: Sadece sorulan seyi yanitle.

SORU: {question}
BAGLAM: {context}

DUSUNCE SURECI:
"""
```

**Dosyalar:**
- src/core/reasoning.py (YENi)
- src/config.py (prompt guncelleme)
- src/api/services/query_service.py (reasoning entegrasyonu)

### 1.2 Streaming Responses

**Sorun:** Kullanici yanit gelene kadar bekliyor, UX kotu.

**Cozum:** Server-Sent Events (SSE)

```typescript
// web/app/api/chat/stream/route.ts
export async function POST(req: Request) {
  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      // Backend'den streaming al
      // Her chunk'i client'a gonder
    }
  });
  return new Response(stream, {
    headers: { 'Content-Type': 'text/event-stream' }
  });
}
```

**Dosyalar:**
- web/app/api/chat/stream/route.ts (YENi)
- web/app/chat/page.tsx (streaming UI)
- src/api/routers/query.py (streaming endpoint)

### 1.3 Context Grading

**Sorun:** Alakasiz belgeler getiriliyor (ZP belgesi CHP sorusuna geliyor).

**Cozum:** Retrieval sonrasi grading

```python
# src/agents/grader.py

class ContextGrader:
    def grade(self, question: str, document: str) -> float:
        prompt = f"""
        Soru: {question}
        Belge: {document}

        Bu belge soruya cevap vermek icin UYGUN mu?
        Puan (0-1):
        """
        # LLM ile skorla, <0.5 ise at
```

---

## FAZ 2: ALTYAPI IYILESTIRMELERI (2-3 Hafta)

### 2.1 Redis Cache

```yaml
# docker-compose.yml
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

```python
# src/core/redis_cache.py
import redis

class RedisCache:
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379)

    def cache_query(self, query_hash: str, response: dict, ttl: int = 3600):
        self.client.setex(query_hash, ttl, json.dumps(response))
```

### 2.2 PostgreSQL User DB

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    tier VARCHAR(20) DEFAULT 'free'
);

CREATE TABLE chat_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    messages JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 2.3 Prometheus Metrics

```python
# src/api/middleware/metrics.py
from prometheus_client import Counter, Histogram

QUERY_COUNT = Counter('mizan_queries_total', 'Total queries', ['party', 'type'])
QUERY_LATENCY = Histogram('mizan_query_latency_seconds', 'Query latency')
```

---

## FAZ 3: FRONTEND MODERNIZASYONU (2 Hafta)

### 3.1 Zustand State Management

```typescript
// web/lib/store.ts
import { create } from 'zustand';

interface ChatStore {
  chats: Chat[];
  currentChatId: string | null;
  addMessage: (message: Message) => void;
  // ...
}

export const useChatStore = create<ChatStore>((set) => ({
  chats: [],
  currentChatId: null,
  addMessage: (message) => set((state) => ({
    // immutable update
  })),
}));
```

### 3.2 Markdown Rendering

```typescript
// web/components/MarkdownRenderer.tsx
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';

export function MarkdownRenderer({ content }: { content: string }) {
  return (
    <ReactMarkdown
      components={{
        code({ node, inline, className, children, ...props }) {
          const match = /language-(\w+)/.exec(className || '');
          return !inline && match ? (
            <SyntaxHighlighter language={match[1]}>
              {String(children)}
            </SyntaxHighlighter>
          ) : (
            <code className={className} {...props}>{children}</code>
          );
        },
      }}
    >
      {content}
    </ReactMarkdown>
  );
}
```

### 3.3 Typing Indicator

```typescript
// web/components/TypingIndicator.tsx
export function TypingIndicator() {
  return (
    <div className="flex gap-1 p-3 bg-gray-800 rounded-lg w-fit">
      <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
      <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
      <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
    </div>
  );
}
```

---

## FAZ 4: ADVANCED LLM FEATURES (3-4 Hafta)

### 4.1 ReAct Loop

```python
# src/agents/react_agent.py

class ReActAgent:
    def run(self, question: str) -> str:
        thoughts = []
        for i in range(MAX_ITERATIONS):
            # THINK
            thought = self.think(question, thoughts)
            thoughts.append(thought)

            # ACT
            action = self.decide_action(thought)
            if action == "FINISH":
                return self.final_answer(thoughts)

            # OBSERVE
            observation = self.execute_action(action)
            thoughts.append(f"Observation: {observation}")

        return self.final_answer(thoughts)
```

### 4.2 Query Decomposition

```python
# src/agents/decomposer.py

class QueryDecomposer:
    def decompose(self, complex_query: str) -> List[str]:
        prompt = f"""
        Karmasik soru: {complex_query}

        Bu soruyu basit alt sorulara ayir:
        1. ...
        2. ...
        """
        # Her alt soruyu ayri RAG ile cevapla
        # Sonuclari birlestir
```

### 4.3 Hallucination Detection

```python
# src/agents/hallucination_checker.py

class HallucinationChecker:
    def check(self, answer: str, sources: List[str]) -> float:
        prompt = f"""
        YANIT: {answer}
        KAYNAKLAR: {sources}

        Yanittaki her iddia kaynaklarda destekleniyor mu?
        Desteklenmeyen iddialar:
        """
        # Hallucination skoru hesapla
```

---

## TIMELINE

```
Hafta 1-2:  FAZ 1 (Reasoning + Streaming + Grading)
Hafta 3-4:  FAZ 2 (Redis + PostgreSQL + Metrics)
Hafta 5-6:  FAZ 3 (Zustand + Markdown + UI)
Hafta 7-10: FAZ 4 (ReAct + Decomposition + Hallucination)
```

---

## ONCELIK SIRASI (Top 10)

| # | Gorev | Dosya | Etki | Sure |
|---|-------|-------|------|------|
| 1 | CoT Prompting | src/config.py | %30 kalite | 2 saat |
| 2 | Context Grading | src/agents/grader.py | %40 relevance | 4 saat |
| 3 | Streaming SSE | web/app/api/chat/stream/ | UX | 6 saat |
| 4 | Redis Cache | docker-compose.yml + src/core/ | %50 hiz | 4 saat |
| 5 | Markdown Rendering | web/components/ | UX | 2 saat |
| 6 | Typing Indicator | web/components/ | UX | 1 saat |
| 7 | PostgreSQL Users | docker-compose.yml + src/api/ | Persistence | 6 saat |
| 8 | Zustand State | web/lib/store.ts | Maintainability | 4 saat |
| 9 | ReAct Loop | src/agents/react_agent.py | %60 kalite | 2 hafta |
| 10 | Prometheus | src/api/middleware/ | Observability | 3 saat |

---

## HEMEN YAPILACAKLAR

```bash
# 1. CoT Prompt guncelle (src/config.py)
# 2. Server yeniden baslat
uvicorn src.api.main:app --reload

# 3. Frontend baslat
cd web && npm run dev

# 4. Test et
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"question": "CHP genel baskani kimdir?"}'
```

---

**Rapor:** llm.md, backend.md, frontend.md
**Hazirlayan:** Claude AI
**Tarih:** 27 Subat 2026
