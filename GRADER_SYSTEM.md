# Context Grading Sistemi

## Genel Bakış

Mizan-AI projesi için Context Grading sistemi eklenmiştir. Bu sistem, RAG (Retrieval-Augmented Generation) pipeline'ında alakasız belgeleri otomatik olarak filtreler ve sadece ilgili belgeleri context'e ekler.

## Sistem Bileşenleri

### 1. ContextGrader Sınıfı (`src/agents/grader.py`)

Belgelerin soruya olan alakalılığını değerlendiren ana sınıftır.

#### Özellikler:
- **RELEVANCE_THRESHOLD**: Varsayılan eşik değeri 0.5 (0-1 arası)
- **grade_document()**: Tek bir belgeyi değerlendiren metod
- **filter_documents()**: Belge koleksiyonunu filtreleyen metod

#### Grading Kriteri:
1. **Parti Eşleşmesi** (0.4 puan): Sorulan partinin belgede geçip geçmediği
2. **Keyword Eşleşmeleri** (0.4 puan): Soru ve belge arasındaki ortak anlamlı kelimelerin sayısı
3. **Soru Tipi Eşleşmesi** (0.2 puan): 
   - "kimdir?" -> "başkan", "genel başkan", "lider" vb.
   - "nedir?" -> "tanım", "amaç", "ilke" vb.

#### Singleton Pattern:
```python
from src.agents import get_context_grader

grader = get_context_grader()  # İlk çağrıda instance oluşturulur
grader2 = get_context_grader()  # Aynı instance döndürülür
```

### 2. QueryService Entegrasyonu (`src/api/services/query_service.py`)

#### Güncellenen Metodlar:

**process_query()**
```python
# Adım 1: Vector DB'den benzer belgeleri al
docs = self.vectorstore.similarity_search(question, k=top_k, filter=filter_meta)

# Adım 2: Grader ile alakalı olanları filtrele
grader = get_context_grader()
filtered_docs, scores = grader.filter_documents(question, docs)

# Adım 3: Sadece filtrelenmiş belgeleri context'e ekle
context_parts = []
for i, doc in enumerate(filtered_docs):
    score = scores[i]
    context_parts.append(f"[Kaynak {i+1}] (Relevans: {score:.2f}):\n{doc.page_content}")
context = "\n\n".join(context_parts)
```

**process_comparison()**
- Her parti için benzer belgeleri al
- Grader ile alakalı olanları filtrele
- Sadece filtrelenmiş belgelerle karşılaştırma yap
- Log'a filtered vs original belge sayısını yaz

### 3. Modül Exportları (`src/agents/__init__.py`)

```python
from .grader import ContextGrader, get_context_grader

__all__ = [
    # ...diğer exportlar...
    "ContextGrader",
    "get_context_grader",
]
```

## Kullanım Örnekleri

### Tek Belgeyi Değerlendirme

```python
from langchain_core.documents import Document
from src.agents import get_context_grader

grader = get_context_grader()

doc = Document(
    page_content="CHP'nin ekonomi politikası...",
    metadata={"party": "CHP", "source": "web"}
)

score = grader.grade_document("CHP ekonomi politikası nedir?", doc)
print(f"Relevans skoru: {score:.2f}")
```

### Belge Koleksiyonunu Filtreleme

```python
from src.agents import get_context_grader

grader = get_context_grader()

# Benzer belgeler
documents = [doc1, doc2, doc3, ...]

# Filtrele
filtered, scores = grader.filter_documents("Seçim stratejileri", documents)

print(f"Orijinal: {len(documents)} belge")
print(f"Filtrelenmiş: {len(filtered)} belge")

for doc, score in zip(filtered, scores):
    print(f"  - {doc.metadata['party']}: {score:.2f}")
```

### QueryService ile Entegrasyon

```python
from src.api.services import QueryService

service = QueryService()

# Grader otomatik olarak kullanılacak
result = await service.process_query(
    question="AKP'nin sağlık politikası nedir?",
    party="AKP",
    top_k=10  # Top 10 alıyor, grader filtreler
)

# Result içinde sadece ilgili kaynaklar var
print(f"Yanıt: {result['answer']}")
print(f"Kaynaklar: {result['sources']}")
```

## Performans ve Lojistik

### Filtre Davranışı
- **Eşiğin üzerinde belgeler**: Direkt olarak context'e eklenir
- **Eşiğin altında tüm belgeler**: En yüksek skorlu 2 belge fallback olarak kullanılır

### Logging
Sistem debug logs'ta filtreleme detaylarını kaydeder:

```
DEBUG: PASS [0.85]: CHP - "CHP ekonomik reform programı..."
DEBUG: PASS [0.72]: AKP - "Hükümet ekonomik tedbirler açıkladı..."
DEBUG: FAIL [0.35]: HDP - "Enerji kaynakları hakkında bilgi..."
WARNING: No docs passed threshold, using top 2
```

### Eşik Değeri Ayarlama

```python
# Varsayılan eşik (0.5)
filtered, scores = grader.filter_documents(question, docs)

# Özel eşik
filtered, scores = grader.filter_documents(question, docs, threshold=0.7)  # Daha katı
filtered, scores = grader.filter_documents(question, docs, threshold=0.3)  # Daha esnek
```

## Öneriler

1. **Eşik Değeri**: Çoğu senaryo için 0.5 yeterlidir. Çok spesifik sorgular için 0.6-0.7 deneyin.
2. **LLM-tabanlı Grading**: Gelecekte LLM'yi entegre ederek daha akıllı grading yapılabilir.
3. **Metricsler**: Grading accuracy'sini ölçmek için user feedback mekanizması eklenebilir.
4. **Stop Words**: Türkçe stop words listesi projektin dilini yansıtmak için genişletilebilir.

## Dosya Listesi

```
src/
├── agents/
│   ├── __init__.py (güncellenmiş - grader export)
│   ├── grader.py (YENİ)
│   ├── analyst.py
│   ├── critic.py
│   ├── graph.py
│   ├── prompts.py
│   ├── researcher.py
│   ├── state.py
│   ├── supervisor.py
│   ├── tools.py
│   └── writer.py
├── api/
│   └── services/
│       ├── __init__.py
│       └── query_service.py (güncellenmiş - grader entegrasyonu)
```

## Testler

```bash
# Grader modülü test et
python -c "from src.agents import ContextGrader, get_context_grader; print('OK')"

# QueryService test et
python -c "from src.api.services import QueryService; print('OK')"

# Full entegrasyon test et (async)
python -c "
import asyncio
from src.api.services import QueryService

async def test():
    service = QueryService()
    # result = await service.process_query('Test soru')
    # print(result)
    
asyncio.run(test())
"
```

## İletişim ve Destek

Herhangi bir soru veya geliştirme önerisi için Mizan-AI ekibine başvurunuz.
