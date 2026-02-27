# MIZAN-AI Backend Mimarisi Analiz Raporu

**Son Güncelleme:** 27 Şubat 2026
**Versiyon:** 1.0.0
**Proje:** MIZAN-AI - Türk Siyasi Belge Analiz Sistemi

---

## İçindekiler

1. [Mevcut Durum Analizi](#mevcut-durum-analizi)
2. [Sistem Mimarisi](#sistem-mimarisi)
3. [API Tasarımı](#api-tasarımı)
4. [Veritabanı ve Cache Stratejileri](#veritabanı-ve-cache-stratejileri)
5. [Güvenlik Analizi](#güvenlik-analizi)
6. [Performans Analizi](#performans-analizi)
7. [Scalability Önerileri](#scalability-önerileri)
8. [Somut Kod Önerileri](#somut-kod-önerileri)
9. [Öncelik Sıralaması ve Eylem Planı](#öncelik-sıralaması-ve-eylem-planı)

---

## 1. Mevcut Durum Analizi

### 1.1 Proje Yapısı

```
mizan-ai/
├── src/
│   ├── app.py (Streamlit UI - Frontend)
│   ├── api/
│   │   ├── main.py (FastAPI App)
│   │   ├── config.py (API Config)
│   │   ├── middleware/
│   │   │   ├── auth.py (JWT/API Key Auth)
│   │   │   └── rate_limit.py (Rate Limiting)
│   │   ├── routers/
│   │   │   ├── query.py (Query, Compare, Analyze)
│   │   │   ├── parties.py (Party Endpoints)
│   │   │   ├── auth.py (User Management)
│   │   │   └── system.py (Health, Stats)
│   │   ├── services/
│   │   │   └── query_service.py (Business Logic)
│   │   └── schemas/ (Pydantic Models)
│   ├── core/
│   │   ├── cache.py (LRU Cache, Vectorstore)
│   │   ├── llm_setup.py (Gemini + Ollama Fallback)
│   │   ├── search_agent.py (Web Search)
│   │   ├── search_strategy_agent.py
│   │   └── duckduckgo_search.py
│   ├── agents/ (LangGraph Multi-Agent)
│   ├── benchmark/
│   └── config.py (Global Config)
├── docker-compose.yml
├── requirements.txt
└── data/ (Party PDFs)
```

### 1.2 Teknoloji Stack

| Katman | Teknoloji | Versiyon |
|--------|-----------|---------|
| **API Framework** | FastAPI | - |
| **ASGI Server** | (Uvicorn/Gunicorn) | - |
| **Vector DB** | ChromaDB | 0.5.23+ |
| **Embeddings** | Sentence Transformers | 3.3.1 |
| **LLM (Primary)** | Google Gemini 2.0 Flash | - |
| **LLM (Fallback)** | Ollama (Qwen 2.5) | - |
| **Web Search** | DuckDuckGo | 4.0.0+ |
| **Auth** | JWT + API Key | python-jose |
| **Cache** | Redis (Planned) | In-Memory LRU |
| **UI** | Streamlit | 1.31.0 |
| **Container** | Docker + Docker Compose | 3.8 |

### 1.3 Mevcut Özellikler

✅ **İmplemente Edilen:**
- FastAPI REST API (v1.0)
- JWT Token-based Authentication
- API Key Validation
- Basic Rate Limiting (In-Memory)
- Multi-party Query Support
- Comparison & Analysis Endpoints
- Web Search Integration (DuckDuckGo)
- Dual LLM Setup (Gemini + Ollama Fallback)
- ChromaDB Vector Storage (Unified)
- System Health & Stats Endpoints
- CORS Middleware
- Error Handling

⚠️ **Kısmi/Eksik Özellikler:**
- Redis Integration (Tasarlandı, implement edilmedi)
- Persistent User Database (In-Memory Dict)
- WebSocket Support (Streaming untuk)
- Request Logging & Monitoring
- API Rate Limiting (Client-level detailing)
- Database Query Optimization
- Async/Await Consistency
- Production-grade Error Handling

---

## 2. Sistem Mimarisi

### 2.1 Mimari Diyagram

```
┌─────────────────────────────────────────────────────────┐
│                     Clients                              │
│  (Streamlit UI / Web Frontend / Mobile / Third-Party)   │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
     ┌──────┐  ┌──────┐  ┌──────┐
     │HTTP  │  │WS    │  │gRPC? │
     │REST  │  │Proto │  │      │
     └──┬───┘  └──┬───┘  └──────┘
        │         │
        └────┬────┘
             ▼
    ┌────────────────────────────────────┐
    │      FastAPI Application           │
    │                                    │
    │  ┌──────────────────────────────┐ │
    │  │    CORS Middleware           │ │
    │  │    Rate Limit Middleware     │ │
    │  │    Auth Middleware           │ │
    │  └──────────────────────────────┘ │
    │                                    │
    │  ┌──────────────────────────────┐ │
    │  │    Routers                   │ │
    │  │  ├── /api/v1/query           │ │
    │  │  ├── /api/v1/compare         │ │
    │  │  ├── /api/v1/analyze         │ │
    │  │  ├── /api/v1/parties         │ │
    │  │  ├── /api/v1/auth            │ │
    │  │  └── /api/v1/health          │ │
    │  └──────────────────────────────┘ │
    │                                    │
    │  ┌──────────────────────────────┐ │
    │  │    Services                  │ │
    │  │  ├── QueryService            │ │
    │  │  ├── AuthService             │ │
    │  │  └── SearchService           │ │
    │  └──────────────────────────────┘ │
    └────┬───────────────────────────┬──┘
         │                           │
         ▼                           ▼
    ┌─────────────┐         ┌──────────────────┐
    │  ChromaDB   │         │   LLM Chain      │
    │ Vector DB   │         │                  │
    │ (Unified)   │         │ ├── Gemini 2.0   │
    │             │         │ └── Ollama       │
    │ Collections │         │    (Fallback)    │
    │ ├── Parties │         │                  │
    │ ├── Metadata│         └──────────────────┘
    │ └── Embeddings
    └─────────────┘         ┌──────────────────┐
                            │  Search Agent    │
                            │ ├── DuckDuckGo   │
                            │ ├── Strategy     │
                            │ └── Filtering    │
                            └──────────────────┘
         │                           │
         └─────────────┬─────────────┘
                       ▼
    ┌──────────────────────────────────┐
    │    Cache Layer (Redis/In-Mem)    │
    │  ├── Embedding Cache             │
    │  ├── Query Results Cache         │
    │  ├── Rate Limit Counters         │
    │  └── User Sessions               │
    └──────────────────────────────────┘
```

### 2.2 İstek Akışı (Request Flow)

```
1. Client Request
   │
   ├─→ [CORS Middleware Check]
   │   └─→ ✗ → 403 Forbidden
   │   └─→ ✓ → Continue
   │
   ├─→ [Rate Limit Middleware]
   │   └─→ ✗ → 429 Too Many Requests
   │   └─→ ✓ → Continue
   │
   ├─→ [Auth Check]
   │   ├─→ JWT Token Validate
   │   ├─→ API Key Validate
   │   └─→ ✗ → 401 Unauthorized
   │   └─→ ✓ → Continue
   │
   ├─→ [Router Dispatch]
   │   ├─→ POST /api/v1/query
   │   ├─→ POST /api/v1/compare
   │   └─→ POST /api/v1/analyze
   │
   ├─→ [Service Layer]
   │   ├─→ Validate Input (Pydantic)
   │   ├─→ Check Cache
   │   ├─→ Execute Business Logic
   │   └─→ Log Request
   │
   ├─→ [Vector Search]
   │   ├─→ Load Vectorstore (Cache)
   │   ├─→ Similarity Search
   │   └─→ Retrieve Documents
   │
   ├─→ [LLM Chain]
   │   ├─→ Create Context from Docs
   │   ├─→ Apply System Prompt
   │   ├─→ Generate Response
   │   └─→ Parse Output
   │
   ├─→ [Web Search (if needed)]
   │   ├─→ Create Search Query
   │   ├─→ DuckDuckGo Search
   │   └─→ Filter & Format Results
   │
   └─→ Response
       └─→ QueryResponse (JSON)
```

### 2.3 Component Sorumlulukları

| Component | Sorumluluk | Status |
|-----------|-----------|--------|
| **FastAPI Main** | App lifecycle, routing | ✅ Good |
| **Auth Middleware** | Token/API Key validation | ⚠️ Basic |
| **Rate Limit Middleware** | Request throttling | ⚠️ In-Memory Only |
| **Query Router** | Endpoint definitions | ✅ Good |
| **Query Service** | Business logic | ⚠️ Needs Refactor |
| **ChromaDB Manager** | Vector storage/retrieval | ✅ Good |
| **LLM Setup** | Model initialization | ✅ Good |
| **Search Agent** | Web search orchestration | ✅ Good |
| **Cache Layer** | Response/data caching | ⚠️ In-Memory LRU |

---

## 3. API Tasarımı

### 3.1 Endpoint Analizi

#### 3.1.1 Query Endpoint
```
POST /api/v1/query

Request:
{
  "question": "Genel başkan nasıl seçilir?",
  "party": "CHP",
  "top_k": 5,
  "stream": false
}

Response:
{
  "answer": "...",
  "sources": ["statute.pdf"],
  "citations": ["..."],
  "query_type": "simple",
  "latency_ms": 245.3
}
```

**Sorunlar:**
- ❌ Streaming desteği placeholder
- ❌ Metadata filtering eksik (page numbers, confidence scores)
- ❌ Pagination yok
- ⚠️ Error responses inconsistent

#### 3.1.2 Compare Endpoint
```
POST /api/v1/compare

Request:
{
  "question": "Gençlik yapıları nasıl?",
  "parties": ["CHP", "AKP"],
  "top_k": 5
}

Response:
{
  "comparison": "...",
  "party_positions": { "CHP": "...", "AKP": "..." },
  "sources": [],
  "latency_ms": 450.2
}
```

**Sorunlar:**
- ⚠️ Paralel istekler yapılmıyor (sequential)
- ❌ Difference highlighting yok
- ❌ Confidence scores yok

#### 3.1.3 Analyze Endpoint
```
POST /api/v1/analyze

Request:
{
  "question": "...",
  "parties": ["CHP"],
  "include_web": true
}

Response:
{
  "analysis": "...",
  "key_findings": [],
  "sources": [],
  "web_results": [],
  "latency_ms": 600.5
}
```

**Sorunlar:**
- ❌ Key findings extraction not implemented
- ❌ Web results integration weak

#### 3.1.4 Auth Endpoints
```
POST /api/v1/auth/register
POST /api/v1/auth/login
GET /api/v1/usage
POST /api/v1/feedback
```

**Sorunlar:**
- ⚠️ User database in-memory (ephemeral)
- ❌ Password stored as plaintext
- ❌ Email verification yok
- ❌ Rate limiting per user yok

#### 3.1.5 Party Endpoints
```
GET /api/v1/parties
GET /api/v1/parties/{code}
```

**Status:** Eksik/Boş router

#### 3.1.6 System Endpoints
```
GET /api/v1/health
GET /api/v1/stats
```

**Sorunlar:**
- ⚠️ Stats hardcoded/mocked
- ❌ Detailed component health yok
- ❌ Monitoring metrics eksik

### 3.2 Şema Tasarımı

**Pydantic Models:**
```python
✅ QueryRequest/Response
✅ CompareRequest/Response
✅ AnalyzeRequest/Response
✅ PartyInfo/PartyListResponse
✅ TokenRequest/Response
✅ UserCreate/UserResponse
✅ UsageResponse
✅ HealthResponse
✅ StatsResponse
```

**Eksikler:**
- ❌ Error response schemas
- ❌ Pagination schemas
- ❌ Sorting/Filter schemas
- ❌ Webhook event schemas

### 3.3 Versioning Stratejisi

**Mevcut:** `/api/v1/`

**Öneriler:**
- ✅ API versioning yapılmış
- ⚠️ Backward compatibility plan yok
- ❌ Deprecation headers yok
- ⚠️ Version migration docs yok

---

## 4. Veritabanı ve Cache Stratejileri

### 4.1 Vector Database (ChromaDB)

#### 4.1.1 Mevcut Setup
```python
# src/core/cache.py
@lru_cache(maxsize=1)
def get_cached_embeddings():
    # Turkish BGE-M3 Embeddings
    return utils.load_embeddings()

def get_vectorstore():
    # Unified DB - tüm partiler
    return utils.load_vectorstore(
        config.UNIFIED_VECTOR_DB,
        embeddings
    )
```

**Özellikleri:**
- ✅ Unified collection (tüm partiler bir DB'de)
- ✅ Metadata filtering (party, source)
- ⚠️ LRU cache (Python in-memory)
- ✅ Turkish embeddings (BGE-M3)

#### 4.1.2 Şema
```
Collection: "turkish_parties"
├── Documents
│   ├── page_content (text)
│   ├── metadata
│   │   ├── party (string) - "CHP", "AKP", etc.
│   │   ├── source (string) - PDF filename
│   │   ├── page (int) - page number
│   │   └── chunk_id (string)
│   └── embeddings (vector, 768-dim)
```

**Sorunlar:**
- ⚠️ Query performance düşebilir (large scale)
- ❌ Indexing strategy yok
- ❌ Compression/optimization yok
- ❌ Backup strategy yok

#### 4.1.3 Önerileri

**Optimize edilmiş setup:**
```python
# Multi-Index approach
class VectorStoreManager:
    def __init__(self):
        # Primary index: similarity search
        self.index_semantic = ChromaDB(...)

        # Secondary index: BM25 (keyword search)
        self.index_bm25 = BM25Retriever(...)

        # Metadata index
        self.index_meta = MetadataIndex(...)

    def hybrid_search(query, party=None, top_k=5):
        # Semantic + keyword hybrid
        semantic_results = self.index_semantic.search(query, k=top_k)
        keyword_results = self.index_bm25.search(query, k=top_k)

        # Rerank & merge
        merged = self._merge_results(semantic_results, keyword_results)
        return merged[:top_k]

    def search_with_filters(query, party=None, page=None):
        # Metadata filtering + search
        filtered_docs = self.index_meta.filter(party=party, page=page)
        return self.index_semantic.search(
            query,
            k=5,
            where={"party": party} if party else None
        )
```

### 4.2 Caching Stratejisi

#### 4.2.1 Mevcut State

| Cache Layer | Tip | Impl. | TTL | Capacity |
|------------|-----|-------|-----|----------|
| Embeddings | LRU | ✅ | None | 1 item |
| Query Results | ❌ | None | - | - |
| User Sessions | ❌ | None | - | - |
| Rate Limits | In-Mem Dict | ⚠️ | 1 min | Unlimited |
| Search Cache | ❌ | None | - | - |

#### 4.2.2 Önerilen Multi-Layer Cache

```
┌─────────────────────────────────────────┐
│        Client (Browser Cache)           │  ← HTTP Cache headers
├─────────────────────────────────────────┤
│          L1: In-Memory (Fast)           │
│  - Embeddings (LRU, 100 items)          │
│  - Recent queries (100 items, 5 min)    │
├─────────────────────────────────────────┤
│        L2: Redis (Distributed)          │
│  - Query results (24 hours)             │
│  - User sessions (7 days)               │
│  - Rate limit counters (1 day)          │
│  - Search results (12 hours)            │
├─────────────────────────────────────────┤
│       L3: Database (Persistent)         │
│  - Vector DB (permanent)                │
│  - User DB (permanent)                  │
│  - Audit logs (permanent)               │
└─────────────────────────────────────────┘
```

#### 4.2.3 Redis Integration (TODO)

```python
# src/core/redis_cache.py
from redis import Redis
from functools import wraps
import json
import hashlib

class RedisCache:
    def __init__(self, redis_url="redis://localhost:6379"):
        self.redis = Redis.from_url(redis_url, decode_responses=True)

    def get_key(self, query, party):
        """Unique cache key generation"""
        key_str = f"{query}:{party}"
        return f"query:{hashlib.md5(key_str.encode()).hexdigest()}"

    def cache_query_result(self, query, party, result, ttl=86400):
        """Cache query result in Redis (24h TTL)"""
        key = self.get_key(query, party)
        self.redis.setex(
            key,
            ttl,
            json.dumps(result, ensure_ascii=False)
        )

    def get_cached_result(self, query, party):
        """Retrieve cached result"""
        key = self.get_key(query, party)
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)
        return None

    def invalidate_party(self, party):
        """Invalidate all queries for a party"""
        pattern = f"query:*:{party}:*"
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)

# Usage in QueryService
redis_cache = RedisCache()

async def process_query(question, party, top_k):
    # Check cache first
    cached = redis_cache.get_cached_result(question, party)
    if cached:
        return cached

    # Process and cache
    result = await _process_query_uncached(question, party, top_k)
    redis_cache.cache_query_result(question, party, result)
    return result
```

#### 4.2.4 Cache Invalidation Strategy

```python
# Invalidation patterns
class CacheInvalidation:
    """Smart cache invalidation"""

    @staticmethod
    async def on_data_update(party: str):
        """When party data is updated"""
        # 1. Invalidate party-specific queries
        redis_cache.invalidate_party(party)

        # 2. Reload embeddings
        embeddings_cache.clear()

        # 3. Notify all clients
        await broadcast_cache_update(party)

    @staticmethod
    async def on_user_logout(user_id: str):
        """Cleanup session data"""
        redis_cache.delete(f"session:{user_id}")
        redis_cache.delete(f"usage:{user_id}")
```

---

## 5. Güvenlik Analizi

### 5.1 Authentication & Authorization

#### 5.1.1 Mevcut Implementation

```python
# src/api/middleware/auth.py

# JWT Token Creation
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        JWT_SECRET_KEY,  # ⚠️ Hardcoded!
        algorithm="HS256"
    )
    return encoded_jwt

# Token Verification
async def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        return "anonymous"  # ⚠️ Fallback to anonymous!
    # ...
```

**Sorunlar:**
- ❌ JWT secret hardcoded ("your-secret-key-change-in-production")
- ⚠️ Anonymous fallback güvenli değil
- ❌ Refresh tokens yok
- ❌ Token blacklisting yok
- ❌ Password hashing yok (plaintext stored)
- ⚠️ No logout mechanism

#### 5.1.2 API Key Validation

```python
async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if not x_api_key:
        return None
    return x_api_key  # ⚠️ No validation!
```

**Sorunlar:**
- ❌ API key validation missing
- ❌ API key rotation strategy yok
- ❌ Usage tracking per API key yok

### 5.2 Güvenlik Önerileri

#### 5.2.1 Improved Authentication

```python
# src/security/auth.py
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityManager:
    """Geliştirilmiş güvenlik yönetimi"""

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_blacklist = set()  # Redis'e taşın

    def hash_password(self, password: str) -> str:
        """Hash password with bcrypt"""
        return pwd_context.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        """Verify password"""
        return pwd_context.verify(plain, hashed)

    def create_access_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token with short TTL"""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "type": "access"
        })

        encoded = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )
        return encoded

    def create_refresh_token(self, data: dict) -> str:
        """Create long-lived refresh token"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=7)

        to_encode.update({
            "exp": expire,
            "type": "refresh"
        })

        return jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )

    def verify_token(
        self,
        token: str,
        token_type: str = "access"
    ) -> Optional[dict]:
        """Verify token and check blacklist"""
        try:
            # Check blacklist
            if token in self.token_blacklist:
                return None

            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )

            # Check token type
            if payload.get("type") != token_type:
                return None

            return payload
        except JWTError:
            return None

    def revoke_token(self, token: str):
        """Add token to blacklist"""
        self.token_blacklist.add(token)
        # In production: store in Redis with TTL

# Improved auth endpoint
@router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: TokenRequest):
    """Secure login with password hashing"""
    user = users_db.get(credentials.username)

    if not user or not security.verify_password(
        credentials.password,
        user["password_hash"]  # ← Use hash, not plaintext
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = security.create_access_token(
        data={"sub": user["username"], "tier": user["tier"]},
        expires_delta=timedelta(minutes=15)  # Short-lived
    )

    refresh_token = security.create_refresh_token(
        data={"sub": user["username"]}
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,  # ← New
        token_type="bearer",
        expires_in=15 * 60
    )

@router.post("/auth/refresh")
async def refresh_token(refresh_token: str):
    """Refresh access token"""
    payload = security.verify_token(refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = security.create_access_token(
        data={"sub": payload["sub"]}
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": 15 * 60
    }

@router.post("/auth/logout")
async def logout(
    authorization: str = Header(...),
    current_user: str = Depends(get_current_user)
):
    """Logout and revoke token"""
    token = authorization.replace("Bearer ", "")
    security.revoke_token(token)

    return {"message": "Logged out successfully"}
```

#### 5.2.2 Rate Limiting Improvements

```python
# src/api/middleware/rate_limit.py
from redis import Redis
from datetime import datetime, timedelta

class AdvancedRateLimiter:
    """Redis-backed rate limiting with multiple strategies"""

    def __init__(self, redis: Redis):
        self.redis = redis

    def get_client_id(self, request):
        """Extract client identifier"""
        # Prefer user_id, fallback to IP
        user_id = getattr(request.state, "user_id", None)
        if user_id and user_id != "anonymous":
            return f"user:{user_id}"

        return f"ip:{request.client.host}"

    async def check_rate_limit(
        self,
        request,
        limits: dict
    ) -> bool:
        """
        Check multiple rate limits

        limits = {
            "per_minute": 60,
            "per_hour": 1000,
            "per_day": 10000
        }
        """
        client_id = self.get_client_id(request)
        now = datetime.now()

        # Per-minute limit
        key_min = f"rl:{client_id}:minute:{now.strftime('%Y%m%d%H%M')}"
        if self.redis.incr(key_min) > limits.get("per_minute", 60):
            return False
        self.redis.expire(key_min, 60)

        # Per-hour limit
        key_hour = f"rl:{client_id}:hour:{now.strftime('%Y%m%d%H')}"
        if self.redis.incr(key_hour) > limits.get("per_hour", 1000):
            return False
        self.redis.expire(key_hour, 3600)

        # Per-day limit
        key_day = f"rl:{client_id}:day:{now.strftime('%Y%m%d')}"
        if self.redis.incr(key_day) > limits.get("per_day", 10000):
            return False
        self.redis.expire(key_day, 86400)

        return True

# Usage in middleware
class EnhancedRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_url="redis://localhost:6379"):
        super().__init__(app)
        self.redis = Redis.from_url(redis_url)
        self.limiter = AdvancedRateLimiter(self.redis)

    async def dispatch(self, request, call_next):
        # Skip auth endpoints
        if request.url.path.startswith("/api/v1/auth"):
            return await call_next(request)

        # Get user tier from token
        tier = await self._get_user_tier(request)
        limits = self._get_tier_limits(tier)

        # Check rate limit
        if not await self.limiter.check_rate_limit(request, limits):
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"}
            )

        # Add rate limit headers
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(limits["per_minute"])

        return response

    def _get_tier_limits(self, tier: str):
        """Get rate limits per tier"""
        limits = {
            "free": {
                "per_minute": 10,
                "per_hour": 100,
                "per_day": settings.FREE_TIER_DAILY
            },
            "pro": {
                "per_minute": 60,
                "per_hour": 1000,
                "per_day": settings.PRO_TIER_DAILY
            },
            "enterprise": {
                "per_minute": 1000,
                "per_hour": 100000,
                "per_day": -1  # Unlimited
            }
        }
        return limits.get(tier, limits["free"])
```

### 5.3 Input Validation & Sanitization

```python
# src/security/validation.py
from pydantic import BaseModel, Field, validator
import re

class SafeQueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="User question"
    )
    party: Optional[str] = Field(
        None,
        regex="^[A-ZÇĞİÖŞÜ]{2,4}$",
        description="Party code"
    )
    top_k: int = Field(5, ge=1, le=20)

    @validator('question')
    def validate_question(cls, v):
        # Remove potential injection
        v = v.strip()

        # Check for SQL injection patterns
        if any(sql in v.lower() for sql in ['select', 'drop', 'insert', 'delete']):
            raise ValueError("Suspicious content detected")

        # Check for excessive special chars
        special_chars = len([c for c in v if not c.isalnum() and not c.isspace()])
        if special_chars / len(v) > 0.3:
            raise ValueError("Too many special characters")

        return v

# CORS Policy
ALLOWED_ORIGINS = [
    "https://mizan-ai.com",
    "https://app.mizan-ai.com",
    "https://admin.mizan-ai.com",
    # NO wildcards in production!
]
```

### 5.4 Data Protection

```python
# Environment variables (DO NOT commit to git!)
# .env file:
# JWT_SECRET_KEY=<strong-random-key>
# GEMINI_API_KEY=<api-key>
# DATABASE_URL=postgresql://user:pass@host/db
# REDIS_URL=redis://user:pass@host:6379
# ALLOWED_ORIGINS=https://mizan-ai.com,https://app.mizan-ai.com

# Logging (don't log sensitive data)
import logging

def safe_log(message, user_id=None, query=None):
    """Sanitize logs"""
    # Log user_id but not password
    log_message = f"[{user_id}] {message}"
    logging.info(log_message)
    # Don't log full query - hash it instead
    if query:
        query_hash = hashlib.sha256(query.encode()).hexdigest()[:8]
        logging.debug(f"Query hash: {query_hash}")
```

### 5.5 Security Checklist

| Kontrol | Status | Açıklama |
|---------|--------|----------|
| ✅ HTTPS Enforced | ⚠️ Dev only | Production için HTTPS gerekli |
| ✅ CORS Policy | ⚠️ Permissive | Wildcard kaldırılmalı |
| ✅ Auth Implemented | ⚠️ Basic | Password hashing, token refresh gerekli |
| ❌ Rate Limiting | ⚠️ In-Memory | Redis'e migrate et |
| ❌ Input Validation | ⚠️ Partial | SQL injection/XSS checks gerekli |
| ❌ CSRF Protection | ❌ Missing | SameSite cookies ekle |
| ❌ API Key Rotation | ❌ Missing | Key versioning implement et |
| ❌ Audit Logging | ❌ Missing | All actions log et |
| ❌ Secret Management | ⚠️ Hardcoded | Vault/Secrets Manager kullan |
| ❌ Encryption at Rest | ❌ Missing | Sensitive data encrypt et |

---

## 6. Performans Analizi

### 6.1 Mevcut Bottlenecks

#### 6.1.1 Vector Search Performance

```python
# Şu anki implementation
docs = vectorstore.similarity_search(question, k=top_k, filter=filter_meta)
# ⚠️ Problemler:
# - Her sorguda embeddings yeniden hesaplanıyor
# - Large collections'da yavaş (~500ms+)
# - No indexing optimization
```

**Çözüm:**
```python
# Optimized version
class OptimizedVectorSearch:
    def __init__(self):
        self.query_cache = LRU(maxsize=1000)
        self.embedding_cache = LRU(maxsize=5000)

    async def search(self, query: str, party: Optional[str] = None):
        # 1. Check query cache first
        cache_key = f"{query}:{party}"
        if cache_key in self.query_cache:
            return self.query_cache[cache_key]

        # 2. Get or compute embedding
        query_embedding = await self._get_embedding(query)

        # 3. Vector search with index
        docs = await self.vectorstore.similarity_search_by_vector(
            query_embedding,
            k=5,
            filter={"party": party} if party else None
        )

        # 4. Cache result
        self.query_cache[cache_key] = docs

        return docs

    async def _get_embedding(self, text: str):
        if text in self.embedding_cache:
            return self.embedding_cache[text]

        embedding = await self.embeddings.aembed_query(text)
        self.embedding_cache[text] = embedding
        return embedding
```

#### 6.1.2 LLM Inference Latency

```python
# Mevcut: Sequential processing
for party in parties:
    # Each takes ~2-5 seconds
    response = llm.invoke(prompt)
    # Total: N * 2-5 seconds
```

**Çözüm:**
```python
# Parallel processing
import asyncio

async def process_parties_parallel(question: str, parties: List[str]):
    tasks = [
        llm.ainvoke(create_prompt(question, party))
        for party in parties
    ]
    # Execute all in parallel
    responses = await asyncio.gather(*tasks)
    return responses

# Time: ~max(2-5 seconds) instead of N * 2-5 seconds
```

### 6.2 Performance Metrics & Monitoring

```python
# src/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge
import time
from functools import wraps

# Metrics
request_count = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

request_latency = Histogram(
    'api_request_duration_seconds',
    'API request latency',
    ['endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.5, 5.0]
)

cache_hits = Counter(
    'cache_hits_total',
    'Cache hits',
    ['cache_type']
)

vectorstore_size = Gauge(
    'vectorstore_documents_total',
    'Total documents in vectorstore'
)

# Decorator for latency tracking
def track_latency(endpoint: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                latency = time.time() - start
                request_latency.labels(endpoint=endpoint).observe(latency)
        return wrapper
    return decorator

# Usage
@router.post("/api/v1/query")
@track_latency("query")
async def query(request: QueryRequest):
    ...

# Prometheus endpoint
@router.get("/metrics")
async def metrics():
    from prometheus_client import generate_latest
    return Response(generate_latest(), media_type="text/plain")
```

### 6.3 Load Testing Results & Optimization

```bash
# Load testing with locust
# pip install locust

# locustfile.py
from locust import HttpUser, task, between
import random

class QueryUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def query(self):
        parties = ["CHP", "AKP", "MHP", "DEM"]
        questions = [
            "Genel başkan nasıl seçilir?",
            "Parti yapısı nedir?",
            "Gençlik kolları var mı?"
        ]

        self.client.post(
            "/api/v1/query",
            json={
                "question": random.choice(questions),
                "party": random.choice(parties),
                "top_k": 5
            }
        )

    @task(1)
    def compare(self):
        self.client.post(
            "/api/v1/compare",
            json={
                "question": "Gençlik yapıları nasıl?",
                "parties": ["CHP", "AKP"]
            }
        )

# Run: locust -f locustfile.py --host=http://localhost:8000
```

**Örnek Load Test Sonuçları:**

```
Total Requests: 1000
Successful: 950 (95%)
Failed: 50 (5%)

Response Time (Percentiles):
  P50: 450ms
  P95: 2.3s
  P99: 5.1s

Throughput:
  RPS: 25 requests/second

Bottlenecks:
  - Vector search: 40% of latency
  - LLM inference: 45% of latency
  - Web search: 10% of latency
```

---

## 7. Scalability Önerileri

### 7.1 Horizontal Scaling

#### 7.1.1 Multi-Instance Setup

```yaml
# docker-compose.yml (Enhanced)
version: '3.8'

services:
  # API instances behind load balancer
  api1:
    build: .
    environment:
      - INSTANCE_ID=1
      - REDIS_URL=redis://redis:6379/0
    ports:
      - "8001:8000"
    networks:
      - mizan-network
    depends_on:
      - redis
      - postgres

  api2:
    build: .
    environment:
      - INSTANCE_ID=2
      - REDIS_URL=redis://redis:6379/0
    ports:
      - "8002:8000"
    networks:
      - mizan-network
    depends_on:
      - redis
      - postgres

  api3:
    build: .
    environment:
      - INSTANCE_ID=3
      - REDIS_URL=redis://redis:6379/0
    ports:
      - "8003:8000"
    networks:
      - mizan-network
    depends_on:
      - redis
      - postgres

  # Load Balancer
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    networks:
      - mizan-network
    depends_on:
      - api1
      - api2
      - api3

  # Shared Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - mizan-network

  # PostgreSQL (User DB)
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=mizan
      - POSTGRES_USER=mizan
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - mizan-network

  # Vector DB (Shared)
  chromadb:
    image: ghcr.io/chroma-core/chroma:latest
    ports:
      - "8288:8288"
    volumes:
      - chroma_data:/chroma/chroma_db
    networks:
      - mizan-network

volumes:
  redis_data:
  postgres_data:
  chroma_data:

networks:
  mizan-network:
    driver: bridge
```

#### 7.1.2 Nginx Load Balancer Config

```nginx
# nginx.conf
upstream api {
    least_conn;
    server api1:8000;
    server api2:8000;
    server api3:8000;

    # Health check
    check interval=3000 rise=2 fall=5 timeout=1000 type=http;
    check_http_send "GET /api/v1/health HTTP/1.0\r\n\r\n";
    check_http_expect_alive http_2xx;
}

server {
    listen 80;
    server_name _;

    client_max_body_size 10M;

    # Compression
    gzip on;
    gzip_min_length 1000;
    gzip_types text/plain application/json;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' https:; script-src 'self' 'unsafe-inline'" always;

    # API routing
    location /api/ {
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Connection pooling
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 4 32k;
    }

    # Health check status
    location /upstream_health {
        access_log off;
        default_type text/html;
        content_by_lua_block {
            local status = ngx.location.capture("/upstream_check_status")
            ngx.print(status.body)
        }
    }
}
```

### 7.2 Database Scaling

#### 7.2.1 Vector DB Replication

```python
# ChromaDB replication strategy
class ReplicatedVectorStore:
    def __init__(self):
        # Primary write node
        self.primary = ChromaDB(host="chroma-primary", port=8288)

        # Replica read nodes
        self.replicas = [
            ChromaDB(host="chroma-replica-1", port=8288),
            ChromaDB(host="chroma-replica-2", port=8288),
        ]

        self.replica_index = 0

    async def write(self, collection_name, documents):
        """Write to primary only"""
        return await self.primary.add(collection_name, documents)

    async def read(self, query, k=5):
        """Read from replicas (load balanced)"""
        replica = self.replicas[self.replica_index % len(self.replicas)]
        self.replica_index += 1

        return await replica.search(query, k)

    async def sync_replicas(self):
        """Periodic sync from primary"""
        collections = await self.primary.list_collections()

        for replica in self.replicas:
            # Get latest state from primary and sync
            for col in collections:
                docs = await self.primary.get_collection(col)
                await replica.update_collection(col, docs)
```

#### 7.2.2 PostgreSQL Scaling (for user data)

```sql
-- Master-Slave replication setup
-- Master node: postgresql-master
-- Slave nodes: postgresql-slave-1, postgresql-slave-2

-- Create replication user
CREATE USER replication WITH REPLICATION ENCRYPTED PASSWORD 'password';

-- Enable replication in postgresql.conf
wal_level = replica
max_wal_senders = 3
wal_keep_size = 1GB

-- On slave node
pg_basebackup -h postgresql-master -U replication -D /var/lib/postgresql/data -Fp -Xs -P

-- recovery.conf on slave
standby_mode = on
primary_conninfo = 'host=postgresql-master port=5432 user=replication password=password'
```

### 7.3 Caching Layer Scaling

```python
# Redis Cluster setup for high availability
class RedisCacheCluster:
    def __init__(self, nodes: List[str]):
        from rediscluster import RedisCluster

        self.cluster = RedisCluster(
            startup_nodes=[{"host": n.split(":")[0], "port": int(n.split(":")[1])} for n in nodes],
            decode_responses=True,
            skip_full_coverage_check=True
        )

    def get(self, key: str):
        return self.cluster.get(key)

    def set(self, key: str, value: str, ttl: int = 3600):
        return self.cluster.setex(key, ttl, value)

# Usage
redis_cluster = RedisCacheCluster([
    "redis-1:6379",
    "redis-2:6379",
    "redis-3:6379",
])
```

### 7.4 API Scaling Patterns

```python
# Asynchronous task queue for heavy operations
from celery import Celery
from celery.result import AsyncResult

app = Celery('mizan', broker='redis://redis:6379/1')

@app.task(bind=True)
def process_large_query(self, question: str, parties: List[str]):
    """Heavy task - runs in background"""
    results = {}

    for party in parties:
        # This is done asynchronously
        result = run_llm_analysis(question, party)
        results[party] = result

        # Progress update
        self.update_state(
            state='PROGRESS',
            meta={'current': party}
        )

    return results

# API endpoint - returns immediately with task ID
@router.post("/api/v1/analyze-batch")
async def analyze_batch(request: AnalyzeRequest):
    task = process_large_query.apply_async(
        args=[request.question, request.parties],
        expires=3600  # Task expires in 1 hour
    )

    return {
        "task_id": task.id,
        "status": "processing",
        "status_url": f"/api/v1/tasks/{task.id}"
    }

# Check task status
@router.get("/api/v1/tasks/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)

    if task_result.state == 'PENDING':
        response = {
            'state': 'PENDING',
            'current': 0,
            'total': 100,
            'status': 'Pending...'
        }
    elif task_result.state == 'PROGRESS':
        response = task_result.info
    elif task_result.state == 'SUCCESS':
        response = {
            'state': 'SUCCESS',
            'result': task_result.result
        }
    else:
        response = {
            'state': task_result.state,
            'result': str(task_result.info)
        }

    return response
```

---

## 8. Somut Kod Önerileri

### 8.1 Refactored Query Service

```python
# src/api/services/query_service.py (Improved)
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging
import asyncio

logger = logging.getLogger(__name__)

@dataclass
class QueryResult:
    answer: str
    sources: List[str]
    citations: List[Dict[str, Any]]
    latency_ms: float
    metadata: Dict[str, Any]

class ImprovedQueryService:
    """Production-ready query service"""

    def __init__(self):
        self._vectorstore = None
        self._llm = None
        self._redis = None

    @property
    def vectorstore(self):
        if not self._vectorstore:
            from src.core.cache import get_vectorstore
            self._vectorstore = get_vectorstore()
        return self._vectorstore

    @property
    def llm(self):
        if not self._llm:
            from src.core.llm_setup import create_llm_handler
            self._llm, _ = create_llm_handler("CHP")
        return self._llm

    async def process_query(
        self,
        question: str,
        party: Optional[str] = None,
        top_k: int = 5,
        user_id: str = "anonymous",
        use_cache: bool = True,
    ) -> QueryResult:
        """Process query with caching and error handling"""

        import time
        start_time = time.time()

        try:
            # 1. Check cache
            if use_cache:
                cached = await self._get_cached_result(question, party)
                if cached:
                    logger.info(f"Cache hit for query: {question[:50]}")
                    return cached

            # 2. Retrieve documents
            docs = await self._retrieve_documents(question, party, top_k)

            if not docs:
                logger.warning(f"No documents found for: {question}")
                return QueryResult(
                    answer="Sorgunuzla ilgili belgelerde bilgi bulunamadı.",
                    sources=[],
                    citations=[],
                    latency_ms=(time.time() - start_time) * 1000,
                    metadata={"docs_found": 0}
                )

            # 3. Generate response using LLM
            answer = await self._generate_answer(question, docs)

            # 4. Extract citations
            citations = self._extract_citations(docs)
            sources = list(set([c["source"] for c in citations]))

            result = QueryResult(
                answer=answer,
                sources=sources,
                citations=citations,
                latency_ms=(time.time() - start_time) * 1000,
                metadata={
                    "docs_found": len(docs),
                    "model": "gemini",
                    "user_id": user_id
                }
            )

            # 5. Cache result
            if use_cache and len(answer) > 0:
                await self._cache_result(question, party, result)

            return result

        except Exception as e:
            logger.error(f"Query processing failed: {str(e)}")
            raise

    async def _retrieve_documents(
        self,
        question: str,
        party: Optional[str] = None,
        top_k: int = 5
    ) -> List:
        """Retrieve relevant documents"""
        try:
            filter_dict = {"party": party.upper()} if party else None

            docs = self.vectorstore.similarity_search(
                question,
                k=top_k,
                filter=filter_dict
            )

            # Add relevance scoring
            for doc in docs:
                doc.metadata["retrieved_at"] = datetime.now().isoformat()

            return docs

        except Exception as e:
            logger.error(f"Document retrieval failed: {e}")
            return []

    async def _generate_answer(
        self,
        question: str,
        docs: List
    ) -> str:
        """Generate answer from documents"""

        # Format context
        context_parts = []
        for i, doc in enumerate(docs, 1):
            party = doc.metadata.get("party", "Bilinmiyor")
            page = doc.metadata.get("page", "?")
            context_parts.append(
                f"[Kaynak {i} - {party}, Sayfa {page}]:\n{doc.page_content}"
            )

        context = "\n\n".join(context_parts)

        # Prepare prompt
        prompt = f"""Aşağıdaki belge parçalarını okuyarak soruyu yanıtla.

BELGELER:
{context}

SORU: {question}

KURALLAR:
1. Sadece verilen belgelerden bilgi kullan
2. Yok olmayan bilgiler uydurma
3. Kaynakları açıkça belirt
4. Türkçe ve net cevap ver

YANIT:"""

        # Call LLM
        response = await asyncio.to_thread(
            self.llm.invoke,
            {"question": question, "context": context}
        )

        # Extract text
        if hasattr(response, "content"):
            return response.content
        elif hasattr(response, "text"):
            return response.text
        else:
            return str(response)

    def _extract_citations(self, docs: List) -> List[Dict]:
        """Extract citation information"""
        citations = []

        for i, doc in enumerate(docs, 1):
            citations.append({
                "index": i,
                "source": doc.metadata.get("source", "unknown"),
                "party": doc.metadata.get("party", "unknown"),
                "page": doc.metadata.get("page", "?"),
                "content_preview": doc.page_content[:200] + "..."
            })

        return citations

    async def _get_cached_result(
        self,
        question: str,
        party: Optional[str]
    ) -> Optional[QueryResult]:
        """Get result from Redis cache"""

        if not self._redis:
            return None

        key = self._cache_key(question, party)
        cached_json = await asyncio.to_thread(
            self._redis.get,
            key
        )

        if cached_json:
            import json
            cached_dict = json.loads(cached_json)
            return QueryResult(**cached_dict)

        return None

    async def _cache_result(
        self,
        question: str,
        party: Optional[str],
        result: QueryResult
    ):
        """Cache result in Redis"""

        if not self._redis:
            return

        import json
        key = self._cache_key(question, party)

        result_dict = {
            "answer": result.answer,
            "sources": result.sources,
            "citations": result.citations,
            "latency_ms": result.latency_ms,
            "metadata": result.metadata,
        }

        await asyncio.to_thread(
            self._redis.setex,
            key,
            86400,  # 24 hour TTL
            json.dumps(result_dict, ensure_ascii=False)
        )

    @staticmethod
    def _cache_key(question: str, party: Optional[str]) -> str:
        """Generate cache key"""
        import hashlib
        key_str = f"{question}:{party or 'all'}"
        key_hash = hashlib.md5(key_str.encode()).hexdigest()
        return f"query:{key_hash}"

    async def process_comparison(
        self,
        question: str,
        parties: List[str],
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """Process comparison in parallel"""

        # Run queries in parallel
        tasks = [
            self.process_query(question, party, top_k)
            for party in parties
        ]

        results = await asyncio.gather(*tasks)

        # Aggregate results
        comparison = self._create_comparison_summary(
            question,
            parties,
            results
        )

        return {
            "comparison": comparison,
            "party_positions": {
                party: result.answer
                for party, result in zip(parties, results)
            },
            "sources": list(set([
                s for result in results
                for s in result.sources
            ])),
        }

    def _create_comparison_summary(
        self,
        question: str,
        parties: List[str],
        results: List[QueryResult]
    ) -> str:
        """Create comparison summary"""

        summary = f"Soru: {question}\n\n"

        for party, result in zip(parties, results):
            summary += f"{party}:\n{result.answer}\n\n"

        return summary
```

### 8.2 Improved Rate Limiting

```python
# src/api/middleware/advanced_rate_limit.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class Tier:
    """User tier definitions"""
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class RateLimitConfig:
    """Rate limiting configuration"""

    TIER_LIMITS = {
        Tier.FREE: {
            "requests_per_minute": 10,
            "requests_per_hour": 100,
            "requests_per_day": 10,
        },
        Tier.PRO: {
            "requests_per_minute": 60,
            "requests_per_hour": 1000,
            "requests_per_day": 10000,
        },
        Tier.ENTERPRISE: {
            "requests_per_minute": 1000,
            "requests_per_hour": 100000,
            "requests_per_day": -1,  # Unlimited
        },
    }

class AdvancedRateLimitMiddleware(BaseHTTPMiddleware):
    """Redis-backed rate limiting"""

    def __init__(self, app, redis_client=None):
        super().__init__(app)
        self.redis = redis_client
        self.in_memory_fallback: Dict = {}

    async def dispatch(self, request: Request, call_next):
        # Skip health checks
        if request.url.path.startswith("/api/v1/health"):
            return await call_next(request)

        # Get client identifier
        client_id = self._get_client_id(request)

        # Get user tier
        tier = await self._get_user_tier(request)

        # Check rate limit
        allowed, remaining, reset_at = await self._check_limit(
            client_id,
            tier
        )

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded",
                    "reset_at": reset_at.isoformat() if reset_at else None,
                }
            )

        # Process request
        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(
            RateLimitConfig.TIER_LIMITS[tier]["requests_per_minute"]
        )
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        if reset_at:
            response.headers["X-RateLimit-Reset"] = str(int(reset_at.timestamp()))

        return response

    def _get_client_id(self, request: Request) -> str:
        """Extract client identifier"""

        # Prefer user_id from token
        if hasattr(request.state, "user_id"):
            return f"user:{request.state.user_id}"

        # Fallback to IP address
        if request.client:
            return f"ip:{request.client.host}"

        return "unknown"

    async def _get_user_tier(self, request: Request) -> str:
        """Get user tier from request"""

        if hasattr(request.state, "user_tier"):
            return request.state.user_tier

        return Tier.FREE

    async def _check_limit(
        self,
        client_id: str,
        tier: str
    ) -> tuple[bool, int, Optional[datetime]]:
        """Check if request is allowed"""

        limits = RateLimitConfig.TIER_LIMITS[tier]
        now = datetime.now()

        # Use Redis if available, else in-memory
        if self.redis:
            return await self._check_redis_limit(client_id, tier, limits)
        else:
            return self._check_memory_limit(client_id, tier, limits)

    async def _check_redis_limit(
        self,
        client_id: str,
        tier: str,
        limits: Dict
    ) -> tuple[bool, int, Optional[datetime]]:
        """Check limit using Redis"""

        now = datetime.now()
        minute_key = f"rl:{client_id}:minute:{now.strftime('%Y%m%d%H%M')}"
        hour_key = f"rl:{client_id}:hour:{now.strftime('%Y%m%d%H')}"
        day_key = f"rl:{client_id}:day:{now.strftime('%Y%m%d')}"

        # Check each limit
        min_count = int(self.redis.incr(minute_key) or 0)
        if min_count == 1:
            self.redis.expire(minute_key, 60)

        if min_count > limits["requests_per_minute"]:
            return False, 0, now + timedelta(minutes=1)

        # Similar checks for hour and day...

        return True, limits["requests_per_minute"] - min_count, None

    def _check_memory_limit(
        self,
        client_id: str,
        tier: str,
        limits: Dict
    ) -> tuple[bool, int, Optional[datetime]]:
        """Check limit using in-memory dict (fallback)"""

        if client_id not in self.in_memory_fallback:
            self.in_memory_fallback[client_id] = {
                "requests": 0,
                "reset_at": datetime.now() + timedelta(minutes=1)
            }

        client_data = self.in_memory_fallback[client_id]

        # Reset if time window passed
        if datetime.now() >= client_data["reset_at"]:
            client_data["requests"] = 0
            client_data["reset_at"] = datetime.now() + timedelta(minutes=1)

        if client_data["requests"] >= limits["requests_per_minute"]:
            return False, 0, client_data["reset_at"]

        client_data["requests"] += 1

        return (
            True,
            limits["requests_per_minute"] - client_data["requests"],
            None
        )
```

### 8.3 WebSocket Support for Streaming

```python
# src/api/routers/streaming.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Set
import logging
import asyncio
import json

router = APIRouter()
logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections.copy():
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Broadcast error: {e}")
                self.disconnect(connection)

manager = ConnectionManager()

@router.websocket("/api/v1/ws/query")
async def websocket_query(websocket: WebSocket):
    """WebSocket endpoint for streaming queries"""

    await manager.connect(websocket)

    try:
        while True:
            # Receive query
            data = await websocket.receive_json()
            question = data.get("question")
            party = data.get("party")

            logger.info(f"WebSocket query: {question}")

            # Start streaming response
            await websocket.send_json({
                "type": "start",
                "message": "Processing query..."
            })

            # Stream document retrieval
            from src.core.cache import get_vectorstore
            vectorstore = get_vectorstore()

            docs = await asyncio.to_thread(
                vectorstore.similarity_search,
                question,
                k=5,
                filter={"party": party.upper()} if party else None
            )

            await websocket.send_json({
                "type": "documents",
                "count": len(docs),
                "documents": [
                    {
                        "source": doc.metadata.get("source"),
                        "page": doc.metadata.get("page"),
                        "content": doc.page_content[:500]
                    }
                    for doc in docs
                ]
            })

            # Stream LLM response
            from src.core.llm_setup import create_llm_handler
            llm, _ = create_llm_handler(party or "CHP")

            context = "\n\n".join([doc.page_content for doc in docs])
            prompt = f"Context: {context}\n\nQuestion: {question}"

            # Simulate streaming by chunking response
            response = await asyncio.to_thread(llm.invoke, prompt)
            response_text = response.content if hasattr(response, "content") else str(response)

            # Send response in chunks
            chunk_size = 50
            for i in range(0, len(response_text), chunk_size):
                chunk = response_text[i:i+chunk_size]

                await websocket.send_json({
                    "type": "chunk",
                    "data": chunk
                })

                await asyncio.sleep(0.01)  # Simulate streaming delay

            # Send completion
            await websocket.send_json({
                "type": "complete",
                "message": "Query processing complete"
            })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
        manager.disconnect(websocket)

# Client-side usage (JavaScript)
"""
const ws = new WebSocket('ws://localhost:8000/api/v1/ws/query');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);

    switch(data.type) {
        case 'start':
            console.log('Starting:', data.message);
            break;
        case 'documents':
            console.log('Found:', data.count, 'documents');
            break;
        case 'chunk':
            document.getElementById('response').textContent += data.data;
            break;
        case 'complete':
            console.log('Done');
            break;
        case 'error':
            console.error(data.message);
            break;
    }
};

ws.send(JSON.stringify({
    question: 'Genel başkan nasıl seçilir?',
    party: 'CHP'
}));
"""
```

---

## 9. Öncelik Sıralaması ve Eylem Planı

### 9.1 Acil Öncelikler (Sprint 1-2: 2-3 hafta)

| # | Görev | Effort | Impact | Status |
|---|-------|--------|--------|--------|
| **P1** | ✅ Redis Integration | 3 days | 🔴 Critical | **TODO** |
| **P2** | 🔒 Password Hashing (Bcrypt) | 1 day | 🔴 Critical | **TODO** |
| **P3** | 📊 Basic Prometheus Metrics | 2 days | 🟠 High | **TODO** |
| **P4** | ❌ Input Validation Hardening | 2 days | 🟠 High | **TODO** |
| **P5** | 🛡️ HTTPS + CORS Hardening | 1 day | 🟠 High | **TODO** |

### 9.2 Kısa Vadeli Hedefler (Sprint 3-4: 4-6 hafta)

| # | Görev | Effort | Impact | Status |
|---|-------|--------|--------|--------|
| **P6** | 📈 Parallel Processing (asyncio) | 3 days | 🟠 High | **TODO** |
| **P7** | 🔄 Refresh Token Implementation | 2 days | 🟠 High | **TODO** |
| **P8** | 💾 PostgreSQL User Database | 4 days | 🟠 High | **TODO** |
| **P9** | 🧪 Load Testing & Optimization | 3 days | 🟠 High | **TODO** |
| **P10** | 📝 Logging & Audit Trail | 3 days | 🟡 Medium | **TODO** |

### 9.3 Orta Vadeli Hedefler (Sprint 5-8: 2-3 ay)

| # | Görev | Effort | Impact | Status |
|---|-------|--------|--------|--------|
| **P11** | 🌊 WebSocket Streaming API | 5 days | 🟡 Medium | **TODO** |
| **P12** | 📦 Docker Compose Multi-Instance | 3 days | 🟡 Medium | **TODO** |
| **P13** | 🔄 Data Replication Strategy | 5 days | 🟡 Medium | **TODO** |
| **P14** | 🧠 Hybrid Search (Semantic + BM25) | 4 days | 🟡 Medium | **TODO** |
| **P15** | 📊 Advanced Analytics Dashboard | 7 days | 🟡 Medium | **TODO** |

### 9.4 Uzun Vadeli Hedefler (Q2-Q3 2026)

| # | Görev | Effort | Impact | Status |
|---|-------|--------|--------|--------|
| **P16** | 🚀 Kubernetes Deployment | 8 days | 🟡 Medium | **FUTURE** |
| **P17** | 🔍 Advanced Search Features (Filters, Facets) | 5 days | 🟡 Medium | **FUTURE** |
| **P18** | 📱 Mobile API Optimization | 4 days | 🟡 Medium | **FUTURE** |
| **P19** | 🎓 ML-based Query Understanding | 10 days | 🟢 Nice-to-have | **FUTURE** |
| **P20** | 🌍 Multi-language Support | 7 days | 🟢 Nice-to-have | **FUTURE** |

### 9.5 Eylem Planı (Detalı)

#### **Sprint 1: Redis & Security (Week 1-2)**

```markdown
## P1: Redis Integration
- [ ] Docker Compose'a Redis ekle
- [ ] RedisCache class implement et
- [ ] Query results caching (24h TTL)
- [ ] Rate limit counters Redis'e migrate et
- [ ] Session management Redis'e migrate et
- [ ] Tests yazma

## P2: Password Hashing
- [ ] bcrypt/passlib integrate et
- [ ] User registration hash ile update et
- [ ] Login password verification implement et
- [ ] Existing users'ı migrate et

## P3: Prometheus Metrics
- [ ] prometheus_client install et
- [ ] Request count metric ekle
- [ ] Request latency histogram ekle
- [ ] Cache hit rate counter ekle
- [ ] /metrics endpoint yazma

## P4: Input Validation
- [ ] SQL injection patterns check et
- [ ] XSS detection implement et
- [ ] Special character validation ekle
- [ ] Rate limit bypass patterns fix et

## P5: HTTPS Setup
- [ ] SSL certificates generate et (self-signed dev, Let's Encrypt prod)
- [ ] Nginx HTTPS config yazma
- [ ] HSTS header ekle
- [ ] CORS whitelist configure et (remove wildcard)
```

#### **Sprint 2-3: Database & Performance**

```markdown
## P8: PostgreSQL Setup
- [ ] PostgreSQL container ekle docker-compose
- [ ] User schema design et
  - users (id, username, email, password_hash, tier, created_at, updated_at)
  - user_sessions (id, user_id, token, expires_at)
  - audit_logs (id, user_id, action, timestamp)
- [ ] SQLAlchemy ORM setup
- [ ] Migration scripts yaz

## P6: Parallel Processing
- [ ] Compare endpoint parallel queries implement et (asyncio.gather)
- [ ] Analyze endpoint parallel LLM calls
- [ ] Batch processing for large requests

## P9: Load Testing
- [ ] Locust test script yaz
- [ ] 100 concurrent users test et
- [ ] Response time metrics top le
- [ ] Bottleneck identify et ve fix et
```

---

## 10. DevOps & Deployment

### 10.1 Production Deployment Checklist

```yaml
Pre-Deployment:
  - [ ] All tests passing (pytest 95%+ coverage)
  - [ ] Security audit completed
  - [ ] Load testing (min 1000 RPS sustained)
  - [ ] Backup strategy tested
  - [ ] Rollback procedure documented

Deployment:
  - [ ] Blue-Green deployment setup
  - [ ] Database migrations automated
  - [ ] Monitoring alerts configured
  - [ ] Error tracking (Sentry) enabled
  - [ ] Log aggregation (ELK/Datadog) configured

Post-Deployment:
  - [ ] Health checks passing (90%+ over 24h)
  - [ ] Synthetic monitoring active
  - [ ] On-call rotation established
  - [ ] Incident response procedure tested
```

### 10.2 Kubernetes Deployment (Future)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mizan-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mizan-api
  template:
    metadata:
      labels:
        app: mizan-api
    spec:
      containers:
      - name: api
        image: mizan-ai/api:latest
        ports:
        - containerPort: 8000
        env:
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: mizan-secrets
              key: redis-url
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "1000m"
            memory: "1Gi"
        livenessProbe:
          httpGet:
            path: /api/v1/health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/v1/health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## Kaynaklar & Referanslar

- [FastAPI Best Practices](https://fastapi.tiangolo.com/)
- [Redis for Caching](https://redis.io/docs/guides/caching/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [OWASP API Security](https://owasp.org/www-project-api-security/)
- [Python Async Patterns](https://docs.python.org/3/library/asyncio.html)
- [Prometheus Monitoring](https://prometheus.io/docs/)

---

## Özet

Mizan-AI backend'i şu anda **prototype/MVP** aşamasındadır. Temel işlevsellik vardır ancak **production-ready** olmaktan uzak. Önerilen eylem planı izlenerek, 2-3 ay içinde **enterprise-grade** bir sistem haline getirilebilir.

**Kritik Alanlar:**
1. 🔴 **Security:** Password hashing, token management, rate limiting
2. 🔴 **Scalability:** Redis, async processing, parallel queries
3. 🔴 **Reliability:** Error handling, monitoring, logging
4. 🟠 **Performance:** Caching, indexing, load testing

**Takip Etmesi Gereken Sonrakiler:**
- Redis integration
- Password hashing
- Prometheus metrics
- PostgreSQL user DB
- Parallel processing

---

**Rapor Hazırlayanı:** Claude AI
**Tarih:** 27 Şubat 2026
**Versiyon:** 1.0
