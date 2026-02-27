# Building a Political RAG System with LangChain and Turkish NLP

## Türkiye'nin ilk AI destekli siyasi belge analiz platformu nasıl inşa edildi?

---

### Giriş

Siyasi partilerin tüzüklerini, açıklamalarını ve meclis konuşmalarını analiz eden bir RAG sistemi inşa etmek istediğimizde, birçok teknik zorlukla karşılaştık. Bu yazıda, MİZAN-AI projesinin teknik mimarisini ve karşılaştığımız zorlukları paylaşacağım.

### Neden RAG?

Geleneksel arama motorları, anahtar kelime eşleştirmesi yaparken,语义 arama (semantic search) daha doğal ve kapsamlı sonuçlar sunar. Özellikle siyasi belgeler gibi karmaşık metinlerde, kullanıcının sorusunun anlamını anlamak kritik öneme sahiptir.

### Mimariye Genel Bakış

```
Kullanıcı Sorusu
       │
       ▼
┌──────────────────┐
│  Intent Router   │  ← Sorguyu analiz et
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Vector Search   │  ← ChromaDB'de semantic search
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   LLM Generation │  ← Gemini/Ollama ile yanıt
└────────┬─────────┘
         │
         ▼
    Kullanıcıya Yanıt
```

### Türkçe NLP Zorlukları

1. **Embedding Modeli**: Türkçe için optimize edilmiş embedding modeli seçmek kritik. `Turkish-BGE-M3` kullandık.

2. **Tokenizasyon**: Türkçe'nin sondan ekleme özelliği (agglutinative) nedeniyle token sayısı hızla artabiliyor.

3. **Karşılaştırma**: "CHP ve AKP'nin ekonomi politikası" gibi karşılaştırmalı sorgular özel dikkat gerektiriyor.

### Öğrenilen Dersler

1. **Fallback Stratejisi**: API kotaları tükenebilir. Ollama ile local fallback şart.

2. **Caching**: Vector store ve embeddings'i cache'lemek performansı 10x artırıyor.

3. **Kalite Kontrolü**: Her yanıt için kaynak gösterimi şeffaflık sağlıyor.

### Sonuç

Bu proje, Türkiye'de açık veri ve yapay zeka entegrasyonunun öncü örneklerinden biri. Amacımız, vatandaşların siyasi partileri daha iyi anlamasını sağlamak.

---

**Sonraki yazıda**: Multi-Agent orchestration ve LangGraph entegrasyonunu detaylıca inceleyeceğiz.
