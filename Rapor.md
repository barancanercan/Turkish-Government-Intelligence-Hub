# MİZAN-AI SaaS UYGUNLUK DEĞERLENDİRME RAPORU

---

## 1. PROJE ÖZETİ

**Mizan-AI**, Türkiye'deki 8 büyük siyasi partinin (CHP, AKP, MHP, İYİ, DEM, SP, ZP, BBP) resmi tüzük ve programlarını yapay zeka destekli bir arayüz üzerinden sorgulanabilir hale getiren bir **Tool-Augmented RAG (T-RAG) platformudur**.

Kullanıcılar doğal dilde soru sorarak parti belgelerinden kaynak gösterimli yanıtlar alabilir, partilerin tutumlarını karşılaştırabilir ve web aramasıyla güncel bilgilere erişebilir.

**Temel Teknolojiler:**
- ChromaDB vektör veritabanı
- Türkçe BGE-M3 embeddings
- Google Gemini 2.0 Flash + Ollama fallback
- Streamlit arayüzü

---

## 2. HEDEF KİTLE ANALİZİ

### Kimler Kullanır?
| Segment | Kullanım Amacı | Potansiyel |
|---------|----------------|------------|
| Gazeteciler/Medya | Parti politikalarını araştırma, haber hazırlama | Yüksek |
| Akademisyenler | Siyasi analiz, karşılaştırmalı çalışmalar | Orta-Yüksek |
| Sivil Toplum Kuruluşları | Politika izleme, savunuculuk | Orta |
| Seçmenler/Vatandaşlar | Bilinçli oy verme, parti araştırma | Yüksek (sezonluk) |
| Siyasi Danışmanlar | Rakip analizi, strateji geliştirme | Düşük hacim, yüksek değer |
| Öğrenciler | Akademik araştırma, tez çalışmaları | Orta |

### Online Erişilebilirlik
- **Evet**, tamamen web tabanlı erişim mümkün
- Streamlit üzerinden canlı demo mevcut
- Docker ile kolay deployment

### Sürekli İhtiyaç Durumu
- **Zayıf nokta**: Siyasi ilgi dönemsel/sezonluk (seçim öncesi yoğunlaşır)
- Seçim dışı dönemlerde kullanım düşebilir
- Sürekli aktif kullanım için ek değer katmanları gerekli

---

## 3. TEKRAR EDEN DEĞER (RECURRING VALUE)

### Kullanıcı Neden Tekrar Gelir?

**Güçlü Yönler:**
- Parti belgeleri güncellendikçe yeni içerik
- Gündem değiştikçe farklı konularda sorgulama ihtiyacı
- Karşılaştırmalı analiz ihtiyacı devam eder

**Zayıf Yönler:**
- Temel veri seti statik (tüzükler nadiren değişir)
- Bir kez öğrenilen bilgi için tekrar sorgulamaya gerek kalmayabilir
- Kullanıcı "bilgiyi aldıktan sonra" geri dönmeyebilir

### Süreklilik Değerlendirmesi
- Mevcut haliyle **düşük-orta** tekrar kullanım
- Haber akışı, meclis kararları, güncel gelişmeler entegrasyonu ile artırılabilir
- "Alert/Bildirim" sistemi ile kullanıcı bağlılığı sağlanabilir

**Skor: 5/10**

---

## 4. ÖLÇEKLENEBİLİRLİK (SCALABILITY)

### İnsan Gücüne Bağımlılık
- **Düşük**: Sistem otomatik çalışıyor
- PDF işleme, vektör oluşturma, sorgulama tamamen otomatik
- Yeni parti ekleme manuel iş gerektiriyor (PDF toplama, metadata)

### Büyüme Potansiyeli
| Alan | Zorluk | Açıklama |
|------|--------|----------|
| Kullanıcı sayısı artışı | Kolay | Cloud altyapı ile ölçeklenir |
| Yeni parti ekleme | Orta | Manuel PDF toplama gerekir |
| Yeni ülke/dil ekleme | Zor | Embedding modeli, veri kaynakları değişir |
| Veri hacmi artışı | Kolay | ChromaDB ölçeklenebilir |

### Teknik Ölçeklenebilirlik
- Mikro servis mimarisi uygulanabilir
- API-first yaklaşımla B2B entegrasyon mümkün
- Caching mekanizması mevcut

**Skor: 7/10**

---

## 5. GELİR MODELİ UYGUNLUĞU

### Abonelik Modeli Analizi

**Uygun Senaryolar:**
| Model | Fiyat Aralığı | Hedef | Uygunluk |
|-------|---------------|-------|----------|
| Freemium | Ücretsiz (limitli) | Bireysel kullanıcılar | Yüksek |
| Pro | 50-150 TL/ay | Gazeteciler, araştırmacılar | Orta |
| Enterprise | 500-2000 TL/ay | Medya kuruluşları, STK'lar | Düşük-Orta |
| API Access | Kullanım bazlı | Geliştiriciler, entegrasyonlar | Orta |

**Fiyatlandırma Zorlukları:**
- Türkiye pazarında ödeme yapma alışkanlığı düşük
- Ücretsiz alternatiflerle (ChatGPT + manuel arama) rekabet
- Niş pazar: toplam adreslenebilir pazar sınırlı

**Potansiyel Gelir Kaynakları:**
1. Abonelik (B2C/B2B)
2. API erişim ücretleri
3. Özel raporlar/analizler (proje bazlı)
4. White-label çözümler
5. Reklam (freemium modelde)

**Skor: 5/10**

---

## 6. ÜRÜNLEŞTİRME SEVİYESİ

### Standart Ürün Potansiyeli

**Mevcut Durum:**
- Temel ürün standartlaştırılmış
- Self-service kullanım mümkün
- Minimal özelleştirme gereksinimi

**Ürünleştirme Güçlü Yönleri:**
- Arayüz hazır ve kullanılabilir
- Onboarding gerektirmez
- Dokümantasyon mevcut

**Proje Bazlı Kalma Riski:**
- Özel veri setleri için danışmanlık gerekebilir
- Enterprise müşteriler özel entegrasyon isteyebilir
- Farklı sektörlere uyarlama (hukuk, finans) proje bazlı

### Değerlendirme
Ürün, mevcut haliyle **yüksek ürünleştirme seviyesine** sahip. Ancak gelir artışı için proje bazlı işler gerekebilir.

**Skor: 8/10**

---

## 7. ONLINE SUNUM UYGUNLUĞU

### İnternet Üzerinden Sunum

**Tam Uyumluluk:**
- %100 web tabanlı
- Fiziksel bileşen yok
- Herhangi bir cihazdan erişilebilir
- Cloud-native mimari

**Fiziksel Bağımlılıklar:**
- **Yok** - Tüm veri dijital (PDF'ler)
- Ollama fallback için local çalışma opsiyonu mevcut

**Deployment Seçenekleri:**
- Streamlit Cloud (mevcut)
- Docker container
- Kubernetes
- Herhangi bir cloud provider

**Skor: 10/10**

---

## 8. TEKNİK UYGULANABİLİRLİK

### Otomasyon Durumu

**Tam Otomatik İşlemler:**
- Sorgu işleme ve yanıt üretimi
- Vektör araması
- Web araması entegrasyonu
- İçerik filtreleme
- LLM fallback mekanizması

**Yarı Otomatik İşlemler:**
- Yeni veri ekleme (PDF toplama manuel, işleme otomatik)
- Model güncelleme

### Teknik Darboğazlar

| Darboğaz | Şiddet | Çözüm |
|----------|--------|-------|
| LLM API maliyetleri | Yüksek | Ollama fallback mevcut |
| Türkçe NLP kalitesi | Orta | BGE-M3 optimize edilmiş |
| Veri güncelliği | Orta | Otomatik scraping eklenebilir |
| Rate limiting | Düşük | Caching mevcut |

### Mimari Olgunluk
- 6 fazlı geliştirme tamamlanmış
- Test suite mevcut
- Security layer (prompt injection koruması) aktif
- Modüler, genişletilebilir yapı

**Skor: 8/10**

---

## 9. RİSKLER VE ZAYIF NOKTALAR

### SaaS Modelini Zorlaştıran Faktörler

| Risk | Etki | Olasılık | Açıklama |
|------|------|----------|----------|
| **Niş pazar** | Yüksek | Kesin | Türk siyaseti spesifik, global ölçeklenme zor |
| **Sezonluk talep** | Yüksek | Yüksek | Seçim dönemleri dışında düşük kullanım |
| **Ödeme alışkanlığı** | Orta | Yüksek | Türkiye'de dijital abonelik adaptasyonu düşük |
| **Ücretsiz alternatifler** | Orta | Kesin | ChatGPT + manuel arama ile rekabet |
| **Veri statikliği** | Orta | Orta | Tüzükler nadiren değişir |
| **Yasal/politik riskler** | Düşük | Düşük | Siyasi içerik hassasiyeti |
| **LLM bağımlılığı** | Orta | Orta | API kesintileri, maliyet artışları |

### Kritik Zayıflıklar
1. **Tek ülke odağı**: Türkiye dışına genişleme ciddi çaba gerektirir
2. **Dar use case**: Sadece siyasi belge analizi, çapraz satış zor
3. **Churn riski**: Bilgi alındıktan sonra abonelik iptali yüksek olabilir

---

## 10. GENEL DEĞERLENDİRME

### Skor Tablosu

| Kriter | Skor | Ağırlık |
|--------|------|---------|
| Tekrar Eden Değer | 5/10 | Kritik |
| Ölçeklenebilirlik | 7/10 | Önemli |
| Gelir Modeli Uygunluğu | 5/10 | Kritik |
| Ürünleştirme Seviyesi | 8/10 | Önemli |
| Online Sunum Uygunluğu | 10/10 | Temel |
| Teknik Uygulanabilirlik | 8/10 | Önemli |

### **TOPLAM SKOR: 43/60**

### SaaS Uygunluk Seviyesi: UYGUN (41-50 Bandı)

---

## NİHAİ KARAR

### Mizan-AI SaaS Yapılmalı mı?

**KOŞULLU EVET** - Ancak mevcut haliyle değil.

**Gerekçe:**

Mizan-AI teknik olarak güçlü, ürünleştirme seviyesi yüksek ve %100 online sunulabilir bir platform. Ancak **sürdürülebilir gelir** için kritik zayıflıkları var:

1. **Recurring value zayıf**: Kullanıcı bilgiyi aldıktan sonra geri dönme motivasyonu düşük
2. **Pazar dar**: Sadece Türk siyaseti ile sınırlı
3. **Sezonluk talep**: Seçim dönemleri dışında kullanım düşecek

**SaaS Başarısı İçin Gerekli Dönüşümler:**
- Statik belge analizinden **dinamik bilgi platformuna** evrilmeli
- Tek dikey'den **çoklu dikey** yapıya genişlemeli
- Bireysel kullanıcıdan **B2B odağına** kaymalı

---

## 11. GELİŞTİRME ÖNERİLERİ

### Kısa Vadeli (0-3 Ay)

| Öneri | Etki | Çaba |
|-------|------|------|
| **Günlük haber entegrasyonu** | Yüksek | Orta |
| Parti açıklamalarını otomatik toplama | Yüksek | Orta |
| E-posta alert sistemi | Orta | Düşük |
| API erişimi açma | Orta | Düşük |

### Orta Vadeli (3-6 Ay)

| Öneri | Etki | Çaba |
|-------|------|------|
| **Meclis tutanakları ekleme** | Yüksek | Yüksek |
| Milletvekili profilleri | Orta | Orta |
| Karşılaştırmalı rapor oluşturucu | Yüksek | Orta |
| White-label B2B çözümü | Yüksek | Yüksek |

### Uzun Vadeli (6-12 Ay)

| Öneri | Etki | Çaba |
|-------|------|------|
| **Çoklu ülke desteği** (AB, Balkanlar) | Çok Yüksek | Çok Yüksek |
| Hukuk/mevzuat dikeyi | Yüksek | Yüksek |
| Kurumsal analiz platformu | Yüksek | Yüksek |
| Tahmin/trend analizi (AI) | Orta | Yüksek |

### Gelir Modeli Önerileri

```
ÖNERİLEN GELİR YAPISI:

Freemium Katman (Ücretsiz)
├── Günlük 10 sorgu limiti
├── Tek parti analizi
└── Temel yanıtlar (kaynak yok)

Pro Katman (99 TL/ay)
├── Sınırsız sorgu
├── Tüm partiler + karşılaştırma
├── Kaynak gösterimi + PDF indirme
└── E-posta alertleri

Enterprise Katman (Özel Fiyat)
├── API erişimi
├── Özel veri entegrasyonu
├── White-label seçeneği
├── SLA garantisi
└── Dedike destek
```

### Pivot Alternatifleri

Mevcut teknoloji altyapısı şu alanlara uyarlanabilir:

1. **Hukuk-Tech**: Mevzuat ve içtihat analizi
2. **Finans-Tech**: Şirket raporları ve regülasyon analizi
3. **Medya Intelligence**: Haber ve sosyal medya analizi
4. **Akademik Platform**: Akademik makale analizi

---

## ÖZET

Mizan-AI, teknik açıdan olgun ve iyi tasarlanmış bir RAG platformu. Ancak **SaaS iş modeli için "sticky" değer önerisi zayıf**.

**Başarılı SaaS dönüşümü için:**
- Statik belgelerden dinamik veri akışına geçiş
- B2B odaklı gelir modeli
- Çoklu dikey genişleme

Bu dönüşümler yapılırsa, platform güçlü bir SaaS adayı haline gelebilir.

---

*Rapor Tarihi: 26 Şubat 2026*
*Değerlendirme Versiyonu: 1.0*
