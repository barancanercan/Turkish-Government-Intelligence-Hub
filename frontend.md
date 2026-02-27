# MİZAN-AI Frontend Mimarisi Analizi

## 1. Mevcut Durum Analizi

### 1.1 Teknoloji Stack

**Framework & Core**
- **Next.js**: 15.1.6 (App Router ile)
- **React**: 19.0.0 (Son sürüm)
- **TypeScript**: 5.7.3 (Strict mode etkin)
- **Tailwind CSS**: 3.4.17 (Utility-first styling)

**State Management & HTTP**
- **React Hooks**: useState, useEffect, useRef (Client-side state)
- **localStorage**: Chat yönetimi ve kalıcılık
- **Fetch API**: Backend iletişimi (REST)

**Authentication & Authorization**
- **NextAuth.js**: 4.24.7 (Session yönetimi)
- **Session Provider**: Client-side SessionProvider wrapper

**UI & Icons**
- **Lucide React**: 0.468.0 (Icon library)
- **clsx**: Koşullu CSS class yönetimi
- **tailwind-merge**: Tailwind class birleştirme

**AI/ML Integration**
- **@ai-sdk/react**: 1.1.21 (Vercel AI SDK - henüz kullanılmıyor)
- **ai**: 4.1.62 (LLM streaming utilities)

### 1.2 Proje Yapısı

```
web/
├── app/
│   ├── layout.tsx                    # Root layout (metadata, providers)
│   ├── page.tsx                      # Ana sayfa (hero, features, parties)
│   ├── chat/
│   │   └── page.tsx                  # Chat sayfası (main conversation UI)
│   ├── about/
│   │   └── page.tsx                  # Hakkımızda sayfası
│   ├── auth/
│   │   └── signin/page.tsx           # Giriş sayfası
│   ├── api/
│   │   ├── chat/route.ts             # Chat API endpoint
│   │   └── auth/[...nextauth]/route.ts
│   ├── providers.tsx                 # NextAuth SessionProvider
│   └── globals.css                   # Global stiller
├── components/
│   ├── index.ts                      # Barrel export
│   ├── Navbar.tsx                    # Navigation (responsive)
│   ├── Footer.tsx                    # Footer component
│   ├── Button.tsx                    # Reusable button component
│   ├── Card.tsx                      # Card + CardHeader/Content/Footer
│   ├── Badge.tsx                     # Badge component
│   ├── Container.tsx                 # Layout container
│   └── AppLayout.tsx                 # (Oluşturulması bekleniyor)
├── types/
│   └── next-auth.d.ts               # NextAuth type definitions
├── next.config.ts                    # Next.js konfigürasyonu
├── tailwind.config.ts                # Tailwind konfigürasyonu
└── tsconfig.json                     # TypeScript konfigürasyonu
```

### 1.3 Component Architecture

#### Chat Page (web/app/chat/page.tsx)
- **State Management**: 7 useState hook (chats, messages, currentChatId, inputValue, isSidebarOpen, isLoading, isMobile)
- **Persistence**: localStorage'da tüm sohbetleri saklar
- **Layout**:
  - Sidebar (sol) - sohbet listesi ve yeni sohbet butonu
  - Main area (sağ) - mesajlar ve input
- **Features**:
  - Sohbet geçmişi yönetimi
  - Responsive sidebar (mobilde kapatılabilir)
  - Auto-scroll to latest message
  - Loading indicators
  - Source citation (PDF file names)

#### Home Page (web/app/page.tsx)
- **Sections**:
  - Hero section (başlık, açıklama, CTA buttons)
  - Features section (3 kart)
  - Parties section (8 parti seçimi)
  - Stats section
  - Final CTA
- **Styling**: Gradient backgrounds, hover effects, animations (bounce)

#### Navbar Component
- **Features**:
  - Sticky positioning (z-50)
  - Mobile hamburger menu
  - NextAuth session display
  - Responsive design
  - Light mode authentication UI

### 1.4 API Integrasyon

**Chat API Route** (/api/chat)
- POST endpoint
- Backend'e `/api/v1/query` ile istek gönderir
- Response fields: response, sources, queryType, qualityScore
- Fallback error handling
- Environment variable: BACKEND_URL

### 1.5 CSS & Styling Stratejisi

- **Color Scheme**: Dark theme (#0a0a0a, #1a1a1a, #141414)
- **Accent Colors**: Mavi (#0066FF, #3b82f6), Mor, Yeşil, Pembe
- **Font**: Inter (Google Fonts)
- **Responsive**: Mobile-first approach (sm, md, lg breakpoints)
- **Animations**: Tailwind built-in (bounce, spin, fade)

---

## 2. Mevcut Sorunlar ve Eksiklikler

### 2.1 Chat UI Sorunları
- ❌ **Streaming Yok**: Full response alınana kadar waitbar gösterilir (UX kötü)
- ❌ **Typing Indicator Yok**: Asistan yazmaya başladığını göstermez
- ❌ **Markdown Rendering Yok**: Yanıtlar plain text olarak gösterilir
- ❌ **Code Block Highlighting Yok**: Kod parçaları vurgulanmaz
- ❌ **Copy to Clipboard**: Yanıtları kopyalama özelliği yok

### 2.2 State Management Sorunları
- ⚠️ **7 useState**: Fazla state hook, prop drilling riski
- ⚠️ **localStorage Prop Drilling**: Sohbetler manuel yönetilir
- ⚠️ **Re-render**: useCallback/useMemo yok, performans etkileri olabilir

### 2.3 Accessibility (A11y) Sorunları
- ❌ **ARIA Labels**: Minimum accessibility attributes
- ❌ **Keyboard Navigation**: Sohbet listesinde Tab desteği eksik
- ❌ **Focus Management**: Modal'da focus trap yok
- ❌ **Contrast**: Bazı kombinasyonlar WCAG AA'yi geçmeyebilir

### 2.4 Performance Sorunları
- ⚠️ **Code Splitting**: AppLayout.tsx import edilir ama kullanılmaz
- ⚠️ **Image Optimization**: Local images optimize edilmez
- ⚠️ **Bundle Size**: @ai-sdk/react yüklü ama kullanılmıyor

### 2.5 Mobile/Responsive Sorunları
- ⚠️ **Message Width**: lg:max-w-2xl mobilde çok dar
- ⚠️ **Input Area**: Keyboard açılırken viewport resize problemi mobilde
- ⚠️ **Touch Targets**: Avatar/buttons <44px olabilir

### 2.6 Seçenek Sistem İşleyişinde Sorunlar
- ⚠️ **Global Theme Yok**: Dark mode hardcoded, light mode desteği yok
- ⚠️ **i18n Yok**: Tüm stringler hardcoded Türkçe

---

## 3. UI/UX İyileştirme Önerileri

### 3.1 Chat Experience (Öncelik: ÇIKMAZ)
- **Streaming Responses**: Server-Sent Events (SSE) ile token-by-token streaming
- **Typing Indicator**: Animated dots veya pulse animation
- **Markdown Support**: remark, rehype libraries ile
- **Copy Button**: Her mesajın sağında copy/clipboard button
- **Regenerate**: Asistan yanıtını yeniden generate etme

### 3.2 Mesaj Gösterimi
- **User Avatars**: Initials veya gravatar
- **Timestamps**: Mesajlarda saat göstermek
- **Edit UI**: Kullanıcı mesajını düzenleme (optional)
- **Delete UI**: Mesaj silme (optional)

### 3.3 Sidebar Geliştirmeleri
- **Search Bar**: Sohbetleri araştırma
- **Sorting**: Son kullanılan/alfabetik
- **Tags**: Sohbetlere tag ekleme
- **Export**: Sohbetleri JSON/PDF export

### 3.4 Visual Feedback
- **Loading States**: Skeleton screens
- **Error Boundaries**: React Error Boundary wrapper
- **Toast Notifications**: Sonuç bildirimleri (delete, save vb.)
- **Confirmation Dialogs**: Kritik işlemler için

---

## 4. Performance Önerileri

### 4.1 Code Splitting & Lazy Loading
```typescript
// Dynamic imports for heavy components
const ChatSidebar = dynamic(() => import('./ChatSidebar'), {
  loading: () => <ChatSidebarSkeleton />
});

const MarkdownRenderer = dynamic(() => import('./MarkdownRenderer'), {
  loading: () => <div>Yükleniyor...</div>
});
```

### 4.2 State Management Optimization
```typescript
// useCallback & useMemo kullanımı
const handleSendMessage = useCallback(async (message: string) => {
  // implementation
}, [currentChatId, messages]);

const sortedChats = useMemo(() => {
  return chats.sort((a, b) =>
    new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
  );
}, [chats]);
```

### 4.3 Context API Replacement
```typescript
// Zustand veya Context API ile centralized state
// localStorage'dan manuel yönetimi kurtarmak

// contexts/ChatContext.tsx
import { createContext, useContext } from 'react';
interface ChatContextType {
  chats: Chat[];
  currentChat: Chat | null;
  addChat: (chat: Chat) => void;
  updateChat: (id: string, chat: Partial<Chat>) => void;
}
```

### 4.4 Image Optimization
```typescript
// Next.js Image component kullanımı
import Image from 'next/image';

<Image
  src="/party-logo.png"
  alt="Parti Logosu"
  width={48}
  height={48}
  priority={false}
/>
```

### 4.5 Web Vitals
- **LCP**: Optimize images, minimize JavaScript
- **FID**: useCallback ile event handler memoization
- **CLS**: Layout shift minimize etmek (explicit sizing)

---

## 5. Modern Chat UI Önerileri

### 5.1 Streaming Response Implementation

```typescript
// lib/useChat.ts - Custom hook
import { useCallback, useState } from 'react';

interface UseStreamChatOptions {
  onChunk?: (chunk: string) => void;
  onComplete?: (fullResponse: string) => void;
  onError?: (error: Error) => void;
}

export function useStreamChat(options: UseStreamChatOptions) {
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = useCallback(async (message: string) => {
    setIsLoading(true);
    let fullResponse = '';

    try {
      const response = await fetch('/api/chat/stream', {
        method: 'POST',
        body: JSON.stringify({ message }),
        headers: { 'Content-Type': 'application/json' },
      });

      if (!response.body) throw new Error('No response body');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        fullResponse += chunk;
        options.onChunk?.(chunk);
      }

      options.onComplete?.(fullResponse);
    } catch (error) {
      options.onError?.(error as Error);
    } finally {
      setIsLoading(false);
    }
  }, [options]);

  return { sendMessage, isLoading };
}
```

### 5.2 Typing Indicator Component

```typescript
// components/TypingIndicator.tsx
export function TypingIndicator() {
  return (
    <div className="flex gap-1">
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"
          style={{
            animationDelay: `${i * 0.15}s`,
          }}
        />
      ))}
    </div>
  );
}
```

### 5.3 Message Component with Actions

```typescript
// components/ChatMessage.tsx
interface ChatMessageProps {
  message: Message;
  onCopy?: (text: string) => void;
  onRegenerate?: (id: string) => void;
}

export function ChatMessage({
  message,
  onCopy,
  onRegenerate,
}: ChatMessageProps) {
  const [showActions, setShowActions] = useState(false);

  return (
    <div
      className="group flex gap-3 hover:bg-gray-900/30 p-3 rounded"
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
    >
      {/* Avatar */}
      <div className="flex-shrink-0">
        {message.role === 'user' ? (
          <UserAvatar />
        ) : (
          <BotAvatar />
        )}
      </div>

      {/* Content */}
      <div className="flex-1">
        <MarkdownRenderer content={message.content} />
      </div>

      {/* Actions */}
      {showActions && (
        <div className="flex gap-2">
          <button
            onClick={() => onCopy?.(message.content)}
            title="Kopyala"
            className="p-2 hover:bg-gray-700 rounded"
          >
            <Copy size={16} />
          </button>

          {message.role === 'assistant' && (
            <button
              onClick={() => onRegenerate?.(message.id)}
              title="Yeniden Oluştur"
              className="p-2 hover:bg-gray-700 rounded"
            >
              <RotateCw size={16} />
            </button>
          )}
        </div>
      )}
    </div>
  );
}
```

### 5.4 Markdown Renderer

```typescript
// components/MarkdownRenderer.tsx
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypePrism from 'rehype-prism-plus';

interface MarkdownRendererProps {
  content: string;
}

export function MarkdownRenderer({ content }: MarkdownRendererProps) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypePrism]}
      components={{
        code({ node, inline, className, children, ...props }) {
          const match = /language-(\w+)/.exec(className || '');
          return !inline && match ? (
            <pre className="bg-gray-900 rounded p-4 overflow-x-auto">
              <code className={className} {...props}>
                {children}
              </code>
            </pre>
          ) : (
            <code className="bg-gray-800 px-2 py-1 rounded text-sm" {...props}>
              {children}
            </code>
          );
        },
        a({ href, children }) {
          return (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:underline"
            >
              {children}
            </a>
          );
        },
      }}
    >
      {content}
    </ReactMarkdown>
  );
}
```

### 5.5 Server-Sent Events (SSE) API Route

```typescript
// app/api/chat/stream/route.ts
import { NextRequest } from 'next/server';

export async function POST(req: NextRequest) {
  const { message, chatId } = await req.json();

  const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';

  return new Response(
    new ReadableStream({
      async start(controller) {
        try {
          const response = await fetch(
            `${backendUrl}/api/v1/query/stream`,
            {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                question: message,
                top_k: 5,
                stream: true,
              }),
            }
          );

          if (!response.body) throw new Error('No response body');

          const reader = response.body.getReader();
          const decoder = new TextDecoder();

          while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const text = decoder.decode(value);
            controller.enqueue(new TextEncoder().encode(text));
          }

          controller.close();
        } catch (error) {
          controller.error(error);
        }
      },
    }),
    {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    }
  );
}
```

---

## 6. Accessibility (A11y) Önerileri

### 6.1 ARIA Attributes

```typescript
// Chat input alanı
<input
  type="text"
  aria-label="Mesaj yazın"
  aria-describedby="message-help"
  placeholder="Mesaj yazın..."
/>
<p id="message-help" className="sr-only">
  Sorunuzu yazıp Enter'a basarak gönderebilirsiniz
</p>

// Sohbet listesi
<div
  role="list"
  aria-label="Sohbet Geçmişi"
>
  {chats.map((chat) => (
    <div
      key={chat.id}
      role="listitem"
      aria-current={currentChatId === chat.id ? 'true' : 'false'}
    >
      {/* ... */}
    </div>
  ))}
</div>
```

### 6.2 Keyboard Navigation

```typescript
// Sidebar navigation keyboard support
const handleKeyDown = (e: React.KeyboardEvent, chatId: string) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    loadChat(chatId);
  }
};

<div
  role="button"
  tabIndex={0}
  onClick={() => loadChat(chat.id)}
  onKeyDown={(e) => handleKeyDown(e, chat.id)}
  aria-pressed={currentChatId === chat.id}
>
  {/* ... */}
</div>
```

### 6.3 Color Contrast Fix

```css
/* Contrast improvement */
.text-gray-500 { /* Şu an 2.6:1 ratio */
  @apply text-gray-400; /* İyileştirilmiş ratio */
}

/* Focus styles */
input:focus-visible {
  @apply ring-2 ring-blue-500 ring-offset-2 ring-offset-gray-900;
}

button:focus-visible {
  @apply ring-2 ring-blue-500 ring-offset-2 ring-offset-gray-900;
}
```

---

## 7. SEO Optimizasyonu

### 7.1 Metadata Improvements

```typescript
// app/layout.tsx
export const metadata: Metadata = {
  title: 'MİZAN-AI | Türk Siyasi Belge Analiz Platformu',
  description:
    'Yapay zeka destekli siyasi belge analiz platformu. 8 siyasi partinin tüzük ve programlarını sorgulayın.',
  keywords: ['siyaset', 'yapay zeka', 'RAG', 'türkiye', 'parti'],
  // New additions
  author: 'Mizan-AI',
  openGraph: {
    title: 'MİZAN-AI | Türk Siyasi Belge Analiz Platformu',
    description: 'AI ile siyasi bilgilere erişin',
    type: 'website',
    locale: 'tr_TR',
    images: [
      {
        url: 'https://mizan-ai.dev/og-image.png',
        width: 1200,
        height: 630,
      },
    ],
  },
  alternates: {
    canonical: 'https://mizan-ai.dev',
  },
};
```

### 7.2 Structured Data

```typescript
// components/StructuredData.tsx
export function StructuredData() {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{
        __html: JSON.stringify({
          '@context': 'https://schema.org',
          '@type': 'WebApplication',
          name: 'MİZAN-AI',
          description: 'Türk siyasi belge analiz platformu',
          url: 'https://mizan-ai.dev',
          applicationCategory: 'InformationApplication',
          offers: {
            '@type': 'Offer',
            price: '0',
            priceCurrency: 'TRY',
          },
        }),
      }}
    />
  );
}
```

---

## 8. Dark/Light Theme Desteği

### 8.1 Theme Provider

```typescript
// hooks/useTheme.ts
import { useEffect, useState } from 'react';

export function useTheme() {
  const [theme, setTheme] = useState<'light' | 'dark'>('dark');

  useEffect(() => {
    // localStorage'dan theme yükle
    const stored = localStorage.getItem('theme');
    if (stored) {
      setTheme(stored as 'light' | 'dark');
    } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      setTheme('dark');
    }
  }, []);

  useEffect(() => {
    // HTML'e theme class ekle
    document.documentElement.classList.toggle('dark', theme === 'dark');
    localStorage.setItem('theme', theme);
  }, [theme]);

  return {
    theme,
    toggleTheme: () => setTheme(theme === 'dark' ? 'light' : 'dark'),
  };
}
```

### 8.2 Theme Toggle Component

```typescript
// components/ThemeToggle.tsx
import { Moon, Sun } from 'lucide-react';
import { useTheme } from '@/hooks/useTheme';

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
      className="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-800"
    >
      {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
    </button>
  );
}
```

### 8.3 Tailwind Config Update

```typescript
// tailwind.config.ts
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dark: {
          primary: '#0a0a0a',
          secondary: '#1a1a1a',
          tertiary: '#141414',
        },
        light: {
          primary: '#ffffff',
          secondary: '#f5f5f5',
          tertiary: '#e5e5e5',
        },
      },
    },
  },
};
```

---

## 9. Internationalization (i18n) - Future

### 9.1 Setup (Recommend next-intl)

```bash
npm install next-intl
```

### 9.2 Structure

```
locales/
├── tr.json      # Türkçe
└── en.json      # İngilizce

messages/
├── common.json
├── chat.json
└── home.json
```

### 9.3 Usage

```typescript
import { useTranslations } from 'next-intl';

export function ChatPage() {
  const t = useTranslations('chat');

  return (
    <button>{t('sendMessage')}</button>
  );
}
```

---

## 10. Modern Zustand State Management (Optional)

### 10.1 Chat Store

```typescript
// lib/store/chatStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
}

interface Chat {
  id: string;
  title: string;
  messages: Message[];
  createdAt: string;
}

interface ChatStore {
  chats: Chat[];
  currentChatId: string | null;
  addChat: (chat: Chat) => void;
  updateChat: (id: string, updates: Partial<Chat>) => void;
  deleteChat: (id: string) => void;
  addMessage: (chatId: string, message: Message) => void;
  setCurrentChat: (id: string) => void;
}

export const useChatStore = create<ChatStore>()(
  persist(
    (set, get) => ({
      chats: [],
      currentChatId: null,

      addChat: (chat) =>
        set((state) => ({
          chats: [...state.chats, chat],
          currentChatId: chat.id,
        })),

      updateChat: (id, updates) =>
        set((state) => ({
          chats: state.chats.map((chat) =>
            chat.id === id ? { ...chat, ...updates } : chat
          ),
        })),

      deleteChat: (id) =>
        set((state) => {
          const filtered = state.chats.filter((c) => c.id !== id);
          return {
            chats: filtered,
            currentChatId:
              state.currentChatId === id
                ? filtered[filtered.length - 1]?.id ?? null
                : state.currentChatId,
          };
        }),

      addMessage: (chatId, message) =>
        set((state) => ({
          chats: state.chats.map((chat) =>
            chat.id === chatId
              ? { ...chat, messages: [...chat.messages, message] }
              : chat
          ),
        })),

      setCurrentChat: (id) =>
        set(() => ({
          currentChatId: id,
        })),
    }),
    {
      name: 'chat-storage',
    }
  )
);
```

### 10.2 Usage

```typescript
// components/ChatPage.tsx
import { useChatStore } from '@/lib/store/chatStore';

export default function ChatPage() {
  const {
    chats,
    currentChatId,
    addChat,
    addMessage,
    deleteChat,
  } = useChatStore();

  // Simplified component logic
}
```

---

## 11. Somut Kod Önerileri - Öncelikli Geliştirmeler

### 11.1 Chat Hook Refactor

```typescript
// hooks/useChat.ts
import { useCallback, useRef, useState } from 'react';

interface UseChatOptions {
  chatId?: string;
}

export function useChat({ chatId }: UseChatOptions) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const sendMessage = useCallback(
    async (content: string) => {
      setError(null);
      setIsLoading(true);

      try {
        const controller = new AbortController();
        abortControllerRef.current = controller;

        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: content,
            chatId,
          }),
          signal: controller.signal,
        });

        if (!response.ok) throw new Error('API Error');

        const data = await response.json();

        const assistantMessage: Message = {
          id: `msg-${Date.now()}`,
          role: 'assistant',
          content: data.response,
          sources: data.sources,
        };

        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err) {
        if (err instanceof Error && err.name !== 'AbortError') {
          setError(err.message);
        }
      } finally {
        setIsLoading(false);
        abortControllerRef.current = null;
      }
    },
    [chatId]
  );

  const cancel = useCallback(() => {
    abortControllerRef.current?.abort();
    setIsLoading(false);
  }, []);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    cancel,
  };
}
```

### 11.2 Error Boundary

```typescript
// components/ChatErrorBoundary.tsx
'use client';

import React, { ReactNode } from 'react';
import { AlertCircle } from 'lucide-react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ChatErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error) {
    console.error('Chat Error:', error);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex items-center justify-center h-screen bg-[#0a0a0a]">
          <div className="text-center p-8 bg-[#1a1a1a] rounded-lg border border-red-500/20">
            <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-bold text-white mb-2">
              Bir Hata Oluştu
            </h2>
            <p className="text-gray-400 mb-6">
              {this.state.error?.message || 'Bilinmeyen bir hata'}
            </p>
            <button
              onClick={() =>
                this.setState({ hasError: false, error: null })
              }
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
            >
              Yeniden Dene
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
```

### 11.3 Toast Notification System

```typescript
// lib/toast.ts
import { create } from 'zustand';

interface Toast {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info' | 'warning';
  duration?: number;
}

interface ToastStore {
  toasts: Toast[];
  addToast: (toast: Omit<Toast, 'id'>) => void;
  removeToast: (id: string) => void;
}

export const useToastStore = create<ToastStore>((set) => ({
  toasts: [],

  addToast: (toast) => {
    const id = `toast-${Date.now()}`;
    set((state) => ({
      toasts: [...state.toasts, { ...toast, id }],
    }));

    if (toast.duration !== 0) {
      setTimeout(() => {
        set((state) => ({
          toasts: state.toasts.filter((t) => t.id !== id),
        }));
      }, toast.duration || 3000);
    }
  },

  removeToast: (id) =>
    set((state) => ({
      toasts: state.toasts.filter((t) => t.id !== id),
    })),
}));

// Usage
export const toast = {
  success: (message: string) =>
    useToastStore.getState().addToast({
      message,
      type: 'success',
    }),
  error: (message: string) =>
    useToastStore.getState().addToast({
      message,
      type: 'error',
    }),
  info: (message: string) =>
    useToastStore.getState().addToast({
      message,
      type: 'info',
    }),
};
```

---

## 12. Öncelik Sıralaması & Roadmap

### Faz 1: KRITIK (Sprint 1-2)
1. **Streaming Responses** - Chat UX iyileştirmesi (1 gün)
2. **Markdown Rendering** - Yanıtlarda format desteği (1 gün)
3. **Error Boundaries** - Hata yönetimi (0.5 gün)
4. **ARIA Labels & A11y** - Accessibility (1 gün)

### Faz 2: ÖNEMLİ (Sprint 3-4)
5. **State Management Refactor** - Zustand veya Context (2 gün)
6. **Typing Indicator** - UX iyileştirmesi (0.5 gün)
7. **Copy/Regenerate Buttons** - Message actions (1 gün)
8. **Toast Notifications** - Feedback system (1 gün)

### Faz 3: İYİLEŞTİRME (Sprint 5)
9. **Keyboard Navigation** - Full accessibility (1 gün)
10. **Chat Search** - Sidebar arama (1 gün)
11. **Theme Toggle** - Dark/Light mode (0.5 gün)
12. **Performance Optimization** - Code splitting, memoization (1 gün)

### Faz 4: FUTURE (Sprint 6+)
13. **i18n Setup** - Multi-language support
14. **Export Features** - JSON/PDF export
15. **Image Optimization** - Next.js Image component
16. **Advanced Analytics** - User behavior tracking

---

## 13. Teknik Borç & Cleanup

### Yapılması Gerekenler
- [ ] Kullanılmayan `@ai-sdk/react` dependency'si kaldır
- [ ] `AppLayout.tsx` component'ı tamamla veya sil
- [ ] Global CSS cleanup (hardcoded colors)
- [ ] TypeScript strict mode tam uyum
- [ ] ESLint rules setup (react-hooks, a11y)

### Paket Güncellemeleri Gerekli
```json
{
  "devDependencies": {
    "react-markdown": "^9.0.0",
    "remark-gfm": "^4.0.0",
    "rehype-prism-plus": "^2.0.0"
  },
  "dependencies": {
    "zustand": "^4.4.0",
    "clsx": "^2.1.1",
    "framer-motion": "^10.16.0"
  }
}
```

---

## 14. Testing Strategy

### Unit Tests
```typescript
// __tests__/hooks/useChat.test.ts
describe('useChat', () => {
  it('should send message and receive response', async () => {
    const { result } = renderHook(() => useChat());

    await act(async () => {
      await result.current.sendMessage('test');
    });

    expect(result.current.messages).toHaveLength(1);
  });
});
```

### E2E Tests
```typescript
// e2e/chat.spec.ts
import { test, expect } from '@playwright/test';

test('chat flow', async ({ page }) => {
  await page.goto('/chat');
  await page.fill('input', 'Test message');
  await page.click('button:has-text("Gönder")');

  await expect(page.locator('text=Test message')).toBeVisible();
});
```

---

## 15. Deployment & Performance Considerations

### Build Optimization
```bash
# Bundle analysis
npm run build -- --analyze

# Performance metrics
npm run lighthouse
```

### Environment Variables
```env
# .env.local
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key
```

### CDN & Caching
- Static assets: Vercel Edge Network
- API responses: Cache-Control headers
- Images: CloudFlare Workers

---

## Sonuç

MİZAN-AI frontend'i **solid bir temel** üzerine kurulmuş olsa da, **modern chat UX** standartlarına ulaşmak için:

1. **Streaming & real-time** features eklenmeli
2. **State management** centralized hale getirilmeli
3. **A11y ve UX** improvements yapılmalı
4. **Performance** optimizasyonları uygulanmalı

**Tahmini Implementation Time**: 3-4 sprint (6-8 hafta)
**ROI**: Kullanıcı memnuniyeti %40-50 artış, performance %30 iyileştirme
