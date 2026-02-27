'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import {
  MessageSquare,
  Plus,
  Trash2,
  Menu,
  X,
  Send,
  Bot,
  User,
  Loader2,
  Scale,
  Home,
} from 'lucide-react';
import { TypingIndicator } from '@/components/TypingIndicator';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
  queryType?: string;
  qualityScore?: number;
}

interface Chat {
  id: string;
  title: string;
  messages: Message[];
  createdAt: string;
}

export default function ChatPage() {
  const [chats, setChats] = useState<Chat[]>([]);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);


  // localStorage işlemleri
  const loadChatsFromStorage = () => {
    if (typeof window === 'undefined') return;
    try {
      const stored = localStorage.getItem('mizan_chats');
      if (stored) {
        return JSON.parse(stored) as Chat[];
      }
    } catch (error) {
      console.error('Error loading chats:', error);
    }
    return [];
  };

  const saveChatsToStorage = (chatsToSave: Chat[]) => {
    if (typeof window === 'undefined') return;
    try {
      localStorage.setItem('mizan_chats', JSON.stringify(chatsToSave));
    } catch (error) {
      console.error('Error saving chats:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Responsive kontrol
  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
      if (window.innerWidth >= 768) {
        setIsSidebarOpen(true);
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // İlk yükleme
  useEffect(() => {
    const loadedChats = loadChatsFromStorage();
    setChats(loadedChats);

    if (loadedChats.length > 0) {
      const lastChat = loadedChats[loadedChats.length - 1];
      setCurrentChatId(lastChat.id);
      setMessages(lastChat.messages);
    }
  }, []);

  // Aktif sohbeti yükle
  const loadChat = (chatId: string) => {
    const chat = chats.find((c) => c.id === chatId);
    if (chat) {
      setCurrentChatId(chatId);
      setMessages(chat.messages);
      if (isMobile) {
        setIsSidebarOpen(false);
      }
    }
  };

  // Yeni sohbet oluştur
  const createNewChat = () => {
    const newChat: Chat = {
      id: Date.now().toString(),
      title: 'Yeni Sohbet',
      messages: [],
      createdAt: new Date().toISOString(),
    };

    const updatedChats = [...chats, newChat];
    setChats(updatedChats);
    saveChatsToStorage(updatedChats);
    setCurrentChatId(newChat.id);
    setMessages([]);
    if (isMobile) {
      setIsSidebarOpen(false);
    }
  };

  // Sohbet sil
  const deleteChat = (chatId: string, e?: React.MouseEvent) => {
    e?.stopPropagation();
    const updatedChats = chats.filter((c) => c.id !== chatId);
    setChats(updatedChats);
    saveChatsToStorage(updatedChats);

    if (currentChatId === chatId) {
      if (updatedChats.length > 0) {
        const lastChat = updatedChats[updatedChats.length - 1];
        setCurrentChatId(lastChat.id);
        setMessages(lastChat.messages);
      } else {
        setCurrentChatId(null);
        setMessages([]);
      }
    }
  };

  // SSE Stream handler
  const handleStreamMessage = async (userMessage: string, activeChatId: string) => {
    let streamedContent = '';
    let sourcesList: string[] = [];
    let queryType = '';

    try {
      const response = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok || !response.body) {
        throw new Error('Stream response error');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      // Create assistant message placeholder
      const assistantMessageId = (Date.now() + 1).toString();
      const placeholderMessage: Message = {
        id: assistantMessageId,
        role: 'assistant',
        content: '',
        sources: [],
      };

      // Add placeholder and update UI
      setMessages(prev => [...prev, placeholderMessage]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);

            if (data === '[DONE]') {
              // Streaming completed
              break;
            }

            try {
              const parsed = JSON.parse(data);

              if (parsed.content) {
                streamedContent += parsed.content;
                // Update message in real-time
                setMessages(prev =>
                  prev.map(msg =>
                    msg.id === assistantMessageId
                      ? { ...msg, content: streamedContent }
                      : msg
                  )
                );
              }

              if (parsed.sources) {
                sourcesList = parsed.sources;
              }

              if (parsed.query_type) {
                queryType = parsed.query_type;
              }

              if (parsed.error) {
                console.error('Stream error:', parsed.error);
                streamedContent = `Hata: ${parsed.error}`;
              }
            } catch (e) {
              // Ignore JSON parse errors for non-JSON data
            }
          }
        }
      }

      // Final update with all metadata
      setMessages(prev =>
        prev.map(msg =>
          msg.id === assistantMessageId
            ? {
                ...msg,
                content: streamedContent || 'Yanıt alınamadı.',
                sources: sourcesList,
                queryType: queryType,
              }
            : msg
        )
      );

      // Save to storage
      const userMsg: Message = {
        id: Date.now().toString(),
        role: 'user',
        content: userMessage,
      };

      const finalAssistantMsg: Message = {
        id: assistantMessageId,
        role: 'assistant',
        content: streamedContent || 'Yanıt alınamadı.',
        sources: sourcesList,
        queryType: queryType,
      };

      setChats(prevChats => {
        const updatedChats = prevChats.map(c =>
          c.id === activeChatId
            ? {
                ...c,
                messages: [...c.messages, userMsg, finalAssistantMsg],
              }
            : c
        );
        saveChatsToStorage(updatedChats);
        return updatedChats;
      });
    } catch (error) {
      console.error('Stream error:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Bağlantı sorunu yaşandı. Lütfen tekrar deneyin.',
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  };

  // Mesaj gönder
  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const messageText = inputValue;

    // Eğer aktif sohbet yoksa yeni oluştur
    let activeChatId = currentChatId;
    if (!activeChatId) {
      const newChat: Chat = {
        id: Date.now().toString(),
        title: messageText.length > 50 ? messageText.substring(0, 50) + '...' : messageText,
        messages: [],
        createdAt: new Date().toISOString(),
      };
      const updatedChats = [...chats, newChat];
      setChats(updatedChats);
      saveChatsToStorage(updatedChats);
      setCurrentChatId(newChat.id);
      activeChatId = newChat.id;
    }

    // Kullanıcı mesajı ekle
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: messageText,
    };

    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInputValue('');
    setIsLoading(true);

    // Sohbet başlığını güncelle
    let chatTitle = 'Yeni Sohbet';
    if (messages.length === 0 && messageText.length > 50) {
      chatTitle = messageText.substring(0, 50) + '...';
    } else if (messages.length === 0) {
      chatTitle = messageText;
    }

    // Update chat title
    setChats(prevChats => {
      const updatedChats = prevChats.map(c =>
        c.id === activeChatId
          ? {
              ...c,
              title: chatTitle,
              messages: updatedMessages,
            }
          : c
      );
      saveChatsToStorage(updatedChats);
      return updatedChats;
    });

    // Use streaming endpoint
    try {
      await handleStreamMessage(messageText, activeChatId);
    } finally {
      setIsLoading(false);
    }
  };

  // Mevcut sohbet
  const currentChat = chats.find((c) => c.id === currentChatId);

  return (
    <div className="flex h-screen bg-[#0a0a0a] text-white">
      {/* Sidebar Overlay (Mobil) */}
      {isMobile && isSidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed md:static top-0 left-0 h-screen w-64 bg-[#141414] border-r border-gray-800 flex flex-col transition-transform duration-300 z-50 ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        }`}
      >
        {/* Logo / Başlık */}
        <div className="p-4 border-b border-gray-800 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition">
            <div className="p-1.5 bg-blue-600 rounded-lg">
              <Scale size={18} className="text-white" />
            </div>
            <h1 className="font-bold text-lg">Mizan AI</h1>
          </Link>
          {isMobile && (
            <button
              onClick={() => setIsSidebarOpen(false)}
              className="md:hidden p-1 hover:bg-gray-700 rounded"
            >
              <X size={20} />
            </button>
          )}
        </div>

        {/* Yeni Sohbet Butonu */}
        <div className="p-4">
          <button
            onClick={createNewChat}
            className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 py-3 px-4 rounded-lg font-medium transition-colors"
          >
            <Plus size={20} />
            Yeni Sohbet
          </button>
        </div>

        {/* Sohbet Listesi */}
        <div className="flex-1 overflow-y-auto">
          {chats.length === 0 ? (
            <div className="p-4 text-center text-gray-400 text-sm">
              Henüz sohbet yok. Yeni sohbet oluşturun.
            </div>
          ) : (
            <div className="space-y-2 p-2">
              {chats.map((chat) => (
                <div
                  key={chat.id}
                  onClick={() => loadChat(chat.id)}
                  className={`w-full text-left p-3 rounded-lg transition-colors flex items-start justify-between group cursor-pointer ${
                    currentChatId === chat.id
                      ? 'bg-blue-600 text-white'
                      : 'bg-[#1a1a1a] hover:bg-gray-700 text-gray-300'
                  }`}
                >
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">
                      {chat.title}
                    </p>
                    <p className="text-xs text-gray-400 mt-1">
                      {new Date(chat.createdAt).toLocaleDateString('tr-TR')}
                    </p>
                  </div>
                  <button
                    onClick={(e) => deleteChat(chat.id, e)}
                    className="ml-2 p-1 opacity-0 group-hover:opacity-100 hover:bg-red-600/20 rounded transition-all"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col bg-[#1a1a1a]">
        {/* Header */}
        <header className="border-b border-gray-800 p-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            {isMobile && (
              <button
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                className="p-2 hover:bg-gray-700 rounded md:hidden"
              >
                <Menu size={24} />
              </button>
            )}
            <div>
              <h2 className="text-xl font-bold">
                {currentChat?.title || 'Sohbet Seçin'}
              </h2>
              {currentChat && (
                <p className="text-xs text-gray-400 mt-1">
                  {currentChat.messages.length} mesaj
                </p>
              )}
            </div>
          </div>

          {/* Ana Sayfa Linki */}
          <Link
            href="/"
            className="flex items-center gap-2 px-3 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-sm transition-colors"
          >
            <Home size={16} />
            <span className="hidden sm:inline">Ana Sayfa</span>
          </Link>
        </header>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          <div className="max-w-4xl mx-auto space-y-6">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-gray-400">
              <div className="p-4 bg-blue-600/10 rounded-full mb-6">
                <Bot size={48} className="text-blue-500" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Mizan AI Asistan</h3>
              <p className="text-sm text-center max-w-md mb-6">
                Turk siyasi partileri hakkinda sorular sorun. CHP, AKP, MHP, IYI, DEM, SP, ZP, BBP hakkinda bilgi alabilirsiniz.
              </p>
              <div className="flex flex-wrap gap-2 justify-center max-w-lg">
                {['CHP ekonomi politikasi', 'AKP egitim programi', 'MHP dis politika', 'Partileri karsilastir'].map((q) => (
                  <button
                    key={q}
                    onClick={() => setInputValue(q)}
                    className="px-3 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-sm transition-colors"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <>
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex gap-4 ${
                    message.role === 'user' ? 'flex-row-reverse' : ''
                  }`}
                >
                  {/* Avatar */}
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                      message.role === 'user'
                        ? 'bg-blue-600'
                        : 'bg-gray-700'
                    }`}
                  >
                    {message.role === 'user' ? (
                      <User size={18} />
                    ) : (
                      <Bot size={18} />
                    )}
                  </div>

                  {/* Mesaj Içeriği */}
                  <div
                    className={`max-w-md lg:max-w-2xl ${
                      message.role === 'user' ? 'flex-row-reverse' : ''
                    }`}
                  >
                    <div
                      className={`p-4 rounded-lg ${
                        message.role === 'user'
                          ? 'bg-blue-600 text-white rounded-tr-none'
                          : 'bg-gray-800 text-gray-100 rounded-tl-none'
                      }`}
                    >
                      <p className="break-words">{message.content}</p>
                    </div>

                    {/* Metadata (Asistan Mesajları İçin) */}
                    {message.role === 'assistant' && (
                      <div className="mt-2 text-xs text-gray-500 space-y-1">
                        {message.queryType && (
                          <p>Sorgu Tipi: {message.queryType}</p>
                        )}
                        {message.qualityScore && (
                          <p>Kalite Puanı: {message.qualityScore}%</p>
                        )}
                        {message.sources && message.sources.length > 0 && (
                          <div>
                            <p className="font-medium text-gray-400 mb-1">
                              Kaynaklar:
                            </p>
                            <div className="flex flex-wrap gap-2">
                              {message.sources.map((source, idx) => {
                                // Sadece dosya adini goster
                                const fileName = source.split(/[/\\]/).pop() || source;
                                const partyName = fileName.replace('.pdf', '').toUpperCase();
                                return (
                                  <span
                                    key={idx}
                                    className="inline-flex items-center px-2 py-1 bg-blue-500/20 text-blue-400 rounded text-xs"
                                  >
                                    {partyName}
                                  </span>
                                );
                              })}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {/* Yükleme Göstergesi */}
              {isLoading && (
                <div className="flex gap-4 items-center">
                  <div className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 bg-gray-700">
                    <Bot size={18} />
                  </div>
                  <TypingIndicator />
                </div>
              )}

              <div ref={messagesEndRef} />
            </>
          )}
          </div>
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-800 p-4">
          <div className="flex gap-2 max-w-4xl mx-auto">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
              placeholder="Mesaj yazın..."
              disabled={isLoading}
              className="flex-1 bg-[#0a0a0a] border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:opacity-50"
            />
            <button
              onClick={handleSendMessage}
              disabled={isLoading || !inputValue.trim()}
              className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed px-4 py-3 rounded-lg font-medium transition-colors flex items-center justify-center"
            >
              {isLoading ? (
                <Loader2 size={20} className="animate-spin" />
              ) : (
                <Send size={20} />
              )}
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
