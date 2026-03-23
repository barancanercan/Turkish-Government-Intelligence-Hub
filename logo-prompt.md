# MizanAI Logo Tasarım Promptları

## Tasarım Sistemi Analizi

### Renk Paleti
| Renk | Hex | Kullanım |
|------|-----|----------|
| **Primary Blue** | `#3B82F6` | Ana vurgu rengi |
| **Purple Accent** | `#8B5CF6` | Gradient ikincil |
| **Background** | `#030712` | Koyu arka plan |
| **White** | `#F9FAFB` | Metin/kontrast |

### Marka Özellikleri
- **Mizan:** Türkçe/Arapça'da "terazi, denge" anlamına gelir
- **Sektör:** AI, Yapay Zeka, NLP, Siyasi Analiz
- **Hedef Kitle:** Profesyoneller, araştırmacılar, teknoloji meraklıları
- **Ton:** Modern, güvenilir, teknolojik, profesyonel

---

## Midjourney Promptları

### Prompt 1 - Minimalist Terazi + AI (ÖNERİLEN)

```
A minimalist logo icon for "MizanAI", a balance scale merged with artificial intelligence neural network nodes, geometric and sleek design, the scale transforms into connected AI nodes at the tips, gradient from electric blue #3B82F6 to purple #8B5CF6, on pure black background #030712, vector style, modern tech aesthetic, clean lines, suitable for app icon, professional SaaS branding --v 6.1 --ar 1:1 --style raw
```

### Prompt 2 - Abstract Geometric

```
Abstract geometric logo mark for AI company "MizanAI", balanced symmetrical design representing equilibrium, interconnected hexagonal shapes forming a subtle scale silhouette, glowing blue #3B82F6 and purple #8B5CF6 gradient, minimalist modern style, dark background #030712, tech startup aesthetic, vector illustration, clean and professional --v 6.1 --ar 1:1 --style raw
```

### Prompt 3 - Lettermark M

```
Modern lettermark logo "M" for "MizanAI" tech company, the letter M stylized as balanced scale arms, incorporating circuit board lines and AI neural connections, gradient blue #3B82F6 to purple #8B5CF6, on black background #030712, geometric minimalist design, suitable for favicon and app icon, premium SaaS branding --v 6.1 --ar 1:1 --style raw
```

### Prompt 4 - Scale + Brain Fusion

```
Iconic logo combining justice scale and human brain neural network for "MizanAI", the scale plates replaced with glowing AI nodes, symmetrical balanced composition, neon blue #3B82F6 and purple #8B5CF6 glow effect, dark background #030712, futuristic minimal style, tech company branding, vector art --v 6.1 --ar 1:1 --style raw
```

---

## DALL-E 3 Promptları

### Prompt 1 - Primary

```
Design a modern minimalist logo for "MizanAI", an AI-powered political analysis platform. The logo should feature an abstract balance scale that seamlessly integrates with AI/neural network elements. Use a gradient from bright blue (#3B82F6) to purple (#8B5CF6). The design should be geometric, clean, and work well as both a large logo and small favicon. Place on a pure dark background (#030712). Style: flat vector, modern tech aesthetic, professional SaaS branding.
```

### Prompt 2 - Alternative

```
Create a sleek icon logo for "MizanAI" AI technology company. Concept: balanced scales made of connected nodes representing artificial intelligence network. The design should be symmetrical and convey trust, balance, and innovation. Color scheme: electric blue (#3B82F6) transitioning to violet (#8B5CF6) gradient. Background: very dark navy (#030712). Style: minimalist, geometric, suitable for web and mobile app icon.
```

---

## Ideogram Promptları

### Prompt 1

```
Logo design, "MizanAI" artificial intelligence company, minimalist balance scale icon fused with neural network nodes, geometric symmetrical design, gradient blue #3B82F6 to purple #8B5CF6, dark background #030712, modern tech startup aesthetic, vector style, clean professional branding, suitable for app icon
```

---

## Leonardo AI Promptları

### Prompt 1

```
Professional logo icon for MizanAI AI technology platform, abstract balance scale merged with artificial intelligence neural connections, minimalist geometric design, electric blue and purple gradient (#3B82F6 to #8B5CF6), pure black background, modern tech company branding, vector illustration style, clean lines, suitable for web and mobile
```

---

## Teknik Gereksinimler

### Dosya Formatları
- **PNG:** Şeffaf arka plan, 512x512px minimum
- **SVG:** Vektör format (ideal)
- **ICO:** Favicon için 32x32, 64x64

### Kullanım Alanları
| Boyut | Kullanım |
|-------|----------|
| 16x16 | Favicon (browser tab) |
| 32x32 | Favicon (retina) |
| 180x180 | Apple touch icon |
| 512x512 | PWA icon, social media |
| 1024x1024 | App store, marketing |

### Arka Plan Uyumu
```css
/* Logo dark background ile kullanılmalı */
background: #030712;
/* veya gradient */
background: linear-gradient(135deg, #030712 0%, #111827 100%);
```

---

## Logo Seçim Kriterleri

1. **Ölçeklenebilirlik:** 16px favicon'dan 1024px'e kadar net görünmeli
2. **Tanınabilirlik:** Tek bakışta AI + Balance konsepti anlaşılmalı
3. **Renk Uyumu:** Mevcut UI ile %100 uyumlu olmalı
4. **Basitlik:** Detaydan kaçınılmalı, minimal olmalı
5. **Zamansızlık:** Trend'lere bağlı olmayan tasarım

---

## Post-Processing

Logo oluşturduktan sonra:

1. **Arka planı şeffaf yap** (remove.bg veya Photoshop)
2. **Renkleri kontrol et** - Tam olarak #3B82F6 ve #8B5CF6 olmalı
3. **Farklı boyutlarda test et** - Favicon, navbar, hero
4. **Glow efekti ekle** (opsiyonel) - CSS ile yapılabilir

```css
/* CSS Glow Effect */
.logo {
  filter: drop-shadow(0 0 20px rgba(59, 130, 246, 0.4));
}
```

---

## Mevcut UI'da Test

Logo'yu seçtikten sonra şu yerlerde test et:

1. `web/public/logo.png` - Ana logo
2. `web/public/favicon.ico` - Browser tab
3. `web/app/layout.tsx` - Meta tags
4. Navbar'da görünüm
5. Footer'da görünüm
6. Chat sidebar'da görünüm
