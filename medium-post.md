# MizanAI: Türkiye'de Siyasi Bilgiye Erişimi Demokratikleştirmek

> **SEO Keywords:** Türkiye siyasi analiz, yapay zeka demokrasi, RAG sistemi, siyasi veri erişimi, açık kaynak AI, politik bilgi şeffaflığı

---

## İçindekiler

1. [Giriş: Demokrasilerde Bilgiye Erişim Sorunu](#1-giriş-demokrasilerde-bilgiye-erişim-sorunu)
2. [Türkiye'de Siyasi Bilgi Erişiminin Mevcut Durumu](#2-türkiyede-siyasi-bilgi-erişiminin-mevcut-durumu)
3. [Problem Analizi: Neden Parti Belgelerine Erişim Zor?](#3-problem-analizi-neden-parti-belgelerine-erişim-zor)
4. [Çözüm: MizanAI ve RAG Mimarisi](#4-çözüm-mizanai-ve-rag-mimarisi)
5. [Teknik Metodoloji: Multi-Agent Sistemler](#5-teknik-metodoloji-multi-agent-sistemler)
6. [Sonuçlar ve Potansiyel Etki](#6-sonuçlar-ve-potansiyel-etki)
7. [Gelecek Vizyonu: AI ve Demokratik Katılım](#7-gelecek-vizyonu-ai-ve-demokratik-katılım)
8. [Sonuç](#8-sonuç)

---

## 1. Giriş: Demokrasilerde Bilgiye Erişim Sorunu

Demokrasinin temel taşlarından biri, vatandaşların bilinçli kararlar alabilmesidir. Ancak bu bilinçli karar alma süreci, doğru ve erişilebilir bilgiye bağlıdır. Seçmenler oy verirken partilerin gerçek politikalarını, vaatlerini ve ideolojik duruşlarını ne kadar biliyor?

Araştırmalar, seçmenlerin büyük çoğunluğunun parti programlarını hiç okumadığını gösteriyor. Bu durum sadece Türkiye'ye özgü değil — dünya genelinde demokratik ülkelerde benzer bir bilgi asimetrisi yaşanıyor. Vatandaşlar, siyasi bilgiye erişmek için genellikle medya filtrelerinden geçmek zorunda kalıyor ve bu filtreler çoğu zaman taraflı veya eksik bilgi sunuyor.

**Peki neden parti belgelerini doğrudan okumuyoruz?**

Cevap basit: Bu belgeler genellikle yüzlerce sayfa uzunluğunda, hukuki dil ile yazılmış ve farklı web sitelerine dağılmış durumda. Ortalama bir vatandaşın bu belgeleri bulması, okuması ve karşılaştırması pratik olarak imkansız.

İşte tam bu noktada yapay zeka devreye giriyor. Bilgiye erişimi demokratikleştirmek, karmaşık belgeleri anlaşılır hale getirmek ve vatandaşların sorularına doğrudan, kaynaklı yanıtlar vermek — bunlar yapay zekanın çözebileceği problemler.

Bu makale, Türkiye'deki siyasi bilgi erişim sorununu analiz etmek ve bu soruna teknolojik bir çözüm önerisi sunmak amacıyla yazıldı. MizanAI projesi, yapay zeka ve doğal dil işleme teknolojilerini kullanarak vatandaşların parti politikalarına erişimini kolaylaştırmayı hedefliyor.

---

## 2. Türkiye'de Siyasi Bilgi Erişiminin Mevcut Durumu

Türkiye'de aktif olarak faaliyet gösteren 8 büyük siyasi parti bulunuyor: AKP, CHP, MHP, İYİ Parti, DEM Parti, Saadet Partisi, Zafer Partisi ve BBP. Her birinin resmi tüzükleri, parti programları, seçim beyannameleri ve politika belgeleri mevcut.

### Mevcut Bilgi Kaynakları

| Kaynak Türü | Avantajlar | Dezavantajlar |
|-------------|------------|---------------|
| **Parti Web Siteleri** | Resmi ve güncel | Dağınık, navigasyonu zor |
| **Haber Medyası** | Özetlenmiş, erişilebilir | Potansiyel taraflılık |
| **Sosyal Medya** | Hızlı, etkileşimli | Bağlamdan kopuk, manipülasyona açık |
| **Akademik Çalışmalar** | Derinlemesine analiz | Halka erişimi sınırlı |

### Sayılarla Durum

- **8** aktif siyasi parti
- **Yüzlerce sayfa** resmi belge (her parti için ortalama 100-300 sayfa)
- **8 farklı web sitesi** ve navigasyon yapısı
- **Sıfıra yakın** karşılaştırmalı analiz aracı

Türk seçmeni, partilerin politikalarını karşılaştırmak istediğinde ciddi engellerle karşılaşıyor. Mevcut kaynaklar ya çok teknik (resmi belgeler), ya potansiyel olarak taraflı (medya), ya da yüzeysel (sosyal medya).

### Bilgi Asimetrisi Sorunu

Siyasi bilgi asimetrisi, demokrasinin işleyişini doğrudan etkiler. Seçmenler:

- Partilerin ekonomi politikalarını karşılaştıramıyor
- Vaatlerin resmi belgelerde nasıl yer aldığını doğrulayamıyor
- Farklı partilerin aynı konudaki yaklaşımlarını göremiyior
- Aldıkları bilginin kaynağını kontrol edemiyor

Bu durum, bilinçli oy kullanımını zorlaştırıyor ve demokrasinin kalitesini düşürüyor.

---

## 3. Problem Analizi: Neden Parti Belgelerine Erişim Zor?

Siyasi bilgiye erişim sorununun arkasında birden fazla faktör yatıyor. Bu faktörleri anlamak, etkili bir çözüm geliştirmek için kritik öneme sahip.

### 3.1 Teknik Engeller

**Belge Formatı ve Dili:**
Parti tüzükleri ve programları genellikle hukuki bir dil ile yazılıyor. "Parti üyeliğinin askıya alınması" gibi teknik terimler, ortalama bir vatandaş için anlaşılması güç olabilir. Ayrıca bu belgeler PDF formatında sunuluyor ve metin araması sınırlı kalıyor.

**Dağınık Bilgi Mimarisi:**
Her partinin kendi web sitesi, kendi navigasyon yapısı ve kendi belge organizasyonu var. Bir kullanıcının 8 farklı web sitesinde aynı bilgiyi bulması, sistematik bir çaba gerektiriyor.

**Güncelleme Takibi:**
Parti politikaları zaman içinde değişiyor. Bu değişiklikleri takip etmek, düzenli olarak tüm parti sitelerini kontrol etmeyi gerektiriyor.

### 3.2 Bilişsel Engeller

**Bilgi Aşırı Yükü:**
Yüzlerce sayfa belgeyi okumak, analiz etmek ve karşılaştırmak ciddi bir bilişsel yük oluşturuyor. İnsanlar doğal olarak bu yükten kaçınıyor ve daha kolay erişilebilir (ama potansiyel olarak daha az güvenilir) kaynaklara yöneliyor.

**Karşılaştırma Zorluğu:**
İki partinin ekonomi politikasını karşılaştırmak istediğinizde, her iki partinin belgelerini de bulmanız, ilgili bölümleri tespit etmeniz ve karşılaştırmalı bir analiz yapmanız gerekiyor. Bu süreç saatler alabilir.

### 3.3 Güven Sorunu

**Kaynak Doğrulama:**
Medyadan aldığımız siyasi bilginin gerçekten parti programına dayandığını nasıl doğrulayabiliriz? Mevcut sistemde bu doğrulama son derece zor.

**Taraflılık Endişesi:**
Haber kaynakları, doğası gereği belirli bir perspektiften yayın yapıyor. Okuyucular, aldıkları bilginin tarafsız olup olmadığını sorgulamak durumunda kalıyor.

### 3.4 Çözüm Gereksinimleri

Bu problemlerin analizi, ideal bir çözümün şu özelliklere sahip olması gerektiğini gösteriyor:

1. **Doğal Dil Arayüzü:** Teknik sorgulamalar yerine günlük dil ile soru sorabilme
2. **Kaynak Şeffaflığı:** Her yanıtın hangi belgeden geldiğini gösterebilme
3. **Karşılaştırma Kapasitesi:** Farklı partilerin pozisyonlarını yan yana sunabilme
4. **Güncelleme Esnekliği:** Yeni belgeleri sisteme kolayca ekleyebilme
5. **Tarafsızlık:** Belgeleri olduğu gibi sunma, yorum katmama

---

## 4. Çözüm: MizanAI ve RAG Mimarisi

**MizanAI**, Türkiye'deki 8 siyasi partinin resmi belgelerini yapay zeka ile sorgulanabilir hale getiren açık kaynaklı bir platformdur. Proje adı, Arapça kökenli "mizan" kelimesinden gelir — terazi, denge, ölçü anlamına gelir. Bu isim, projenin temel misyonunu yansıtır: siyasi bilgiye dengeli ve ölçülü erişim sağlamak.

### RAG (Retrieval-Augmented Generation) Nedir?

RAG, büyük dil modellerinin (LLM) "halüsinasyon" problemini çözmek için geliştirilen bir mimaridir. Standart bir LLM, eğitim verilerinde olmayan bilgileri "uydurabilir". RAG sistemi ise:

1. **Retrieval (Geri Çağırma):** Kullanıcının sorusuna en alakalı belge parçalarını veritabanından çeker
2. **Augmentation (Zenginleştirme):** Bu belge parçalarını LLM'e bağlam olarak sunar
3. **Generation (Üretim):** LLM, sadece verilen bağlama dayanarak yanıt üretir

Bu yaklaşım, yanıtların her zaman gerçek belgelere dayandığını garanti eder.

### MizanAI Mimarisi

```
[Kullanıcı Sorusu]
       ↓
[İçerik Filtresi] → Uygunsuz içerik engelleme
       ↓
[Sorgu Analizörü] → Alt sorulara ayırma, parti tespiti
       ↓
[Paralel Arama]
    ├── [ChromaDB] → Yerel vektör veritabanı
    └── [DuckDuckGo] → Web araması (güncel bilgi için)
       ↓
[Bağlam Birleştirme] → Alakalılık puanlama
       ↓
[Ollama LLM] → Yanıt üretimi
       ↓
[SSE Stream] → Gerçek zamanlı akış
       ↓
[Next.js UI] → Markdown render
```

### Vektör Veritabanı: ChromaDB

Parti belgeleri, embedding modeli kullanılarak vektörlere dönüştürülür ve ChromaDB'de saklanır. Bu yaklaşım, semantik arama imkanı sağlar — yani kelime eşleşmesi yerine anlam benzerliği üzerinden arama yapılabilir.

**Örnek:**
- Kullanıcı sorusu: "CHP'nin ekonomi politikası nedir?"
- Sistem, "ekonomi" kelimesini aramak yerine, sorunun anlamına en yakın belge parçalarını bulur
- Bu parçalar "maliye politikası", "vergi reformu", "istihdam" gibi alakalı kavramları içerebilir

### Kaynak Şeffaflığı

MizanAI'ın en önemli özelliklerinden biri, her yanıtın kaynak göstermesidir. Kullanıcı:

- Yanıtın hangi belgeden geldiğini görebilir
- İlgili belge bölümüne doğrudan erişebilir
- Bilginin doğruluğunu bağımsız olarak doğrulayabilir

Bu şeffaflık, sistemin güvenilirliğini artırır ve "yapay zekanın söylediğine körü körüne güvenme" problemini çözer.

---

## 5. Teknik Metodoloji: Multi-Agent Sistemler

MizanAI, tek bir monolitik LLM yerine, uzmanlaşmış agent'lardan oluşan bir sistem kullanır. Bu yaklaşım, LangGraph framework'ü ile implement edilmiştir.

### Agent Mimarisi

| Agent | Görev | Araçlar |
|-------|-------|---------|
| **Supervisor** | Sorgu yönlendirme, koordinasyon | Tüm agent'lara erişim |
| **Researcher** | Bilgi toplama | ChromaDB, DuckDuckGo, Wikipedia |
| **Analyst** | Karşılaştırmalı analiz | Birden fazla parti verisi |
| **Writer** | Yanıt formatlama | Markdown, Chain-of-Thought |
| **Critic** | Kalite kontrol | Revizyon döngüsü |
| **Grader** | Alakalılık puanlama | Eşik değer: 0.3 |

### Akıllı Arama Pipeline

**1. Sorgu Analizi:**
```
"AKP ve CHP'nin ekonomi politikalarını karşılaştır"
       ↓
[Sorgu Analizörü]
       ↓
Alt sorgular:
  - "AKP ekonomi politikası"
  - "CHP ekonomi politikası"
Parti tespiti: ["AKP", "CHP"]
Karşılaştırma modu: Aktif
```

**2. Paralel Arama:**
Sistem, belirlenen partiler için eşzamanlı olarak yerel veritabanı ve web araması yapar. Bu paralel işlem, yanıt süresini önemli ölçüde kısaltır.

**3. Bağlam Değerlendirme:**
Bulunan her belge parçası, alakalılık açısından puanlanır. Eşik değerin (0.3) altında kalan sonuçlar filtrelenir. Bu mekanizma, "gürültülü" bilginin yanıta sızmasını önler.

### Gerçek Zamanlı Streaming

Kullanıcı deneyimini iyileştirmek için, yanıtlar Server-Sent Events (SSE) protokolü ile gerçek zamanlı olarak aktarılır. Kullanıcı, tüm yanıtın üretilmesini beklemek yerine, cümle cümle gelen yanıtı izleyebilir.

```typescript
// Next.js SSE Handler
const eventSource = new EventSource('/api/chat/stream');
eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    appendToResponse(data.content);
};
```

### LLM Konfigürasyonu

MizanAI, Ollama üzerinden yerel LLM kullanır. Bu yaklaşımın avantajları:

- **Gizlilik:** Sorgular üçüncü parti sunuculara gönderilmez
- **Maliyet:** API maliyeti yok
- **Özelleştirme:** Model parametreleri tam kontrol altında

```python
# src/core/llm_setup.py
OllamaLLM(
    model="qwen2.5:7b",
    temperature=0.3,      # Tutarlı yanıtlar için düşük sıcaklık
    num_predict=2048,     # Uzun yanıtlar için yeterli token
    repeat_penalty=1.2,   # Tekrar önleme
)
```

---

## 6. Sonuçlar ve Potansiyel Etki

MizanAI'ın geliştirilmesi ve test edilmesi sürecinde elde edilen sonuçlar, sistemin potansiyel etkisini ortaya koyuyor.

### Performans Metrikleri

| Metrik | Değer |
|--------|-------|
| Ortalama yanıt süresi | 3-8 saniye |
| Kaynak eşleştirme doğruluğu | %85+ |
| Desteklenen parti sayısı | 8 |
| Toplam indekslenen belge | 50+ PDF |

### Kullanım Senaryoları

**Senaryo 1: Politika Sorgulama**
```
Soru: "MHP'nin eğitim politikası nedir?"
Yanıt: [Parti programından ilgili bölümler + özet]
Kaynak: MHP Parti Programı, Sayfa 45-52
```

**Senaryo 2: Parti Karşılaştırma**
```
Soru: "CHP ile İYİ Parti'nin ekonomi yaklaşımları nasıl farklılaşıyor?"
Yanıt: [Karşılaştırmalı tablo + analiz]
Kaynaklar: CHP Program, İYİ Parti Program
```

**Senaryo 3: Vaat Doğrulama**
```
Soru: "Hangi parti asgari ücreti artırmayı vadediyor?"
Yanıt: [Tüm parti vaatlerinin taraması]
Kaynaklar: Seçim beyannameleri
```

### Demokratik Etki Potansiyeli

**1. Bilgi Eşitliği:**
Siyasi bilgiye erişim, artık araştırma kapasitesine veya zamana bağlı değil. Herkes, aynı kalitede bilgiye erişebilir.

**2. Kaynak Şeffaflığı:**
"Bir parti şunu söyledi" iddiası artık doğrulanabilir. Bu, siyasi söylemdeki manipülasyonu zorlaştırır.

**3. Karşılaştırmalı Analiz:**
Seçmenler, farklı partilerin aynı konudaki yaklaşımlarını kolayca karşılaştırabilir.

**4. Açık Kaynak Güveni:**
Kodun tamamen açık kaynak olması, sistemin tarafsızlığının bağımsız olarak doğrulanabilmesini sağlar.

### Sınırlamalar ve Zorluklar

Sistemin mevcut sınırlamalarını kabul etmek önemlidir:

- **Belge Güncelliği:** Parti belgeleri manuel olarak güncellenmeli
- **Dil Sınırı:** Şu an sadece Türkçe destekleniyor
- **LLM Sınırlamaları:** Yerel model, bulut API'lere göre daha az güçlü
- **Bağlam Penceresi:** Çok uzun sorgulamalarda bağlam sınırı

---

## 7. Gelecek Vizyonu: AI ve Demokratik Katılım

MizanAI, daha büyük bir vizyonun ilk adımıdır: yapay zekanın demokratik katılımı güçlendirmesi.

### Kısa Vadeli Hedefler (6-12 ay)

- **Meclis Tutanakları:** Milletvekillerinin meclis konuşmalarının entegrasyonu
- **Belediye Belgeleri:** Yerel yönetim kararlarının sorgulanabilir hale getirilmesi
- **Çok Dilli Destek:** İngilizce ve Kürtçe arayüz

### Orta Vadeli Hedefler (1-2 yıl)

- **Seçim Takibi:** Vaatlerin gerçekleşme oranının izlenmesi
- **Politika Değişiklik Alertleri:** Parti programlarındaki değişikliklerin otomatik bildirimi
- **API Erişimi:** Gazeteciler ve araştırmacılar için programatik erişim

### Uzun Vadeli Vizyon

**Demokratik AI Asistanı:**
Her vatandaşın cebinde, siyasi bilgiye anında erişim sağlayan tarafsız bir asistan. Bu asistan:

- Seçim dönemlerinde parti karşılaştırmaları sunar
- Meclis oylamalarını açıklar
- Yerel ve ulusal politikaları bağlamsallaştırır
- Vatandaşların temsilcileriyle iletişimini kolaylaştırır

### Global Ölçeklenebilirlik

MizanAI'ın mimarisi, farklı ülkelere adapte edilebilir şekilde tasarlandı:

- **Veri Katmanı:** Her ülkenin parti sistemine uyarlanabilir
- **Dil Desteği:** Çok dilli embedding modelleri kullanılabilir
- **Açık Kaynak:** Topluluk katkılarıyla hızlı adaptasyon

**Hayal edin:** Avrupa Birliği vatandaşlarının, 27 ülkenin parti politikalarını tek bir platformdan sorgulayabildiği bir dünya. Ya da Afrika'daki gelişen demokrasilerde, vatandaşların siyasi bilgiye ilk kez gerçek anlamda erişebildiği bir dönem.

### Etik Sorumluluk

Yapay zeka ve siyasetin kesişiminde, etik sorumluluk kritik öneme sahiptir:

1. **Tarafsızlık Taahhüdü:** Sistem hiçbir partiyi kayırmaz veya karalamaz
2. **Şeffaflık:** Tüm kod ve metodoloji açık erişimlidir
3. **Kaynak Gösterme:** Her bilgi, doğrulanabilir kaynaklara dayandırılır
4. **Manipülasyon Önleme:** İçerik filtreleri, sistemin kötüye kullanımını engeller

---

## 8. Sonuç

Demokrasi, bilinçli vatandaşların bilinçli kararlar almasına dayanır. Ancak günümüzde siyasi bilgiye erişim, beklenenden çok daha zordur. Parti programları karmaşık, kaynaklar dağınık ve medya potansiyel olarak taraflıdır.

**MizanAI**, bu soruna teknolojik bir çözüm sunuyor. RAG mimarisi ve multi-agent sistemler kullanarak:

- Parti belgelerini sorgulanabilir hale getiriyor
- Her yanıtı kaynaklarla destekliyor
- Partileri karşılaştırmalı analiz etmeyi mümkün kılıyor
- Açık kaynak olarak şeffaflık sağlıyor

Bu proje, yapay zekanın demokratik değerleri güçlendirebileceğinin somut bir kanıtıdır. Teknoloji, doğru kullanıldığında bilgi asimetrisini azaltabilir, şeffaflığı artırabilir ve vatandaşların siyasi sürece daha bilinçli katılımını sağlayabilir.

**mizan** — terazi, denge, ölçü. Siyasi bilgiye erişimde denge, demokrasinin kalitesini doğrudan etkiler. MizanAI, bu dengeyi teknoloji ile sağlamayı hedefliyor.

---

> *"Bilgi güçtür, ancak erişilebilir bilgi demokrasidir."*

---

## Yazar Hakkında

**Baran Can Ercan** — AI/ML Engineer, RAG ve Multi-Agent sistemleri konusunda uzman.

- GitHub: [barancanercan](https://github.com/barancanercan)
- LinkedIn: [barancanercan](https://linkedin.com/in/barancanercan)
- Proje: [MizanAI](https://github.com/barancanercan/mizan-ai)

---

## Kaynaklar

1. Lewis, P. et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *NeurIPS 2020*
2. Shuster, K. et al. (2021). "Retrieval Augmentation Reduces Hallucination in Conversation." *EMNLP 2021*
3. LangChain Documentation (2024). "Multi-Agent Systems with LangGraph"
4. Ollama Documentation (2024). "Running LLMs Locally"
5. ChromaDB Documentation (2024). "Vector Database for AI Applications"

---

*Bu makale, siyasi bilgiye erişimin demokratikleştirilmesi üzerine yapılan araştırmanın bir parçasıdır.*

---

**Etiketler:** #YapayZeka #Demokrasi #RAG #AçıkKaynak #Türkiye #SiyasiBilgi #LangChain #MachineLearning
