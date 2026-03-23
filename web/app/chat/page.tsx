'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import ReactMarkdown from 'react-markdown';
import { motion, AnimatePresence } from 'framer-motion';
import {
  MessageSquare,
  Plus,
  Trash2,
  Menu,
  X,
  Send,
  User,
  Loader2,
  Home,
  Sparkles,
} from 'lucide-react';
import { TypingIndicator, MessageSkeleton } from '@/components/Skeleton';

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

// Unique ID generator to prevent duplicate keys
const generateUniqueId = () => `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

const QUICK_QUESTIONS = [
  'AKP ve CHP arasındaki farklar nelerdir?',
  'Hangi parti asgari ücreti en çok artırmayı vadediyor?',
  'MHP ile İYİ Parti neden ayrıldı?',
  'Partilerin ekonomi politikalarını karşılaştır',
];

export default function ChatPage() {
  const [chats, setChats] = useState<Chat[]>([]);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [isInitialLoading, setIsInitialLoading] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const loadChatsFromStorage = () => {
    if (typeof window === 'undefined') return [];
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

  useEffect(() => {
    const loadedChats = loadChatsFromStorage();
    setChats(loadedChats);

    if (loadedChats.length > 0) {
      const lastChat = loadedChats[loadedChats.length - 1];
      setCurrentChatId(lastChat.id);
      setMessages(lastChat.messages);
    }
    
    setTimeout(() => setIsInitialLoading(false), 500);
  }, []);

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

  const createNewChat = () => {
    const newChat: Chat = {
      id: generateUniqueId(),
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

  const handleStreamMessage = async (userMessage: string, activeChatId: string) => {
    let streamedContent = '';
    let sourcesList: string[] = [];
    let queryType = '';
    let hasError = false;

    try {
      const response = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      if (!response.body) {
        throw new Error('No response body');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      const assistantMessageId = generateUniqueId();
      const placeholderMessage: Message = {
        id: assistantMessageId,
        role: 'assistant',
        content: '',
        sources: [],
      };

      setMessages(prev => [...prev, placeholderMessage]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (!line.trim() || !line.startsWith('data: ')) continue;
          
          const data = line.slice(6).trim();
          if (!data) continue;

          if (data === '[DONE]') {
            break;
          }

          try {
            const parsed = JSON.parse(data);

            if (parsed.error) {
              console.error('Backend error:', parsed.error);
              hasError = true;
              streamedContent += `\n\nHata: ${parsed.error}`;
            }

            if (parsed.content) {
              streamedContent += parsed.content;
              setMessages(prev =>
                prev.map(msg =>
                  msg.id === assistantMessageId
                    ? { ...msg, content: streamedContent }
                    : msg
                )
              );
            }

            if (parsed.sources && Array.isArray(parsed.sources)) {
              sourcesList = parsed.sources;
            }

            if (parsed.query_type) {
              queryType = parsed.query_type;
            }
          } catch (e) {
            console.warn('Parse error:', e, 'Data:', data);
          }
        }
      }

      const finalContent = streamedContent.trim() || (hasError ? 'İşlem sırasında hata oluştu.' : 'Yanıt alınamadı.');
      
      setMessages(prev =>
        prev.map(msg =>
          msg.id === assistantMessageId
            ? {
                ...msg,
                content: finalContent,
                sources: sourcesList,
                queryType: queryType,
              }
            : msg
        )
      );

      const userMsg: Message = {
        id: generateUniqueId(),
        role: 'user',
        content: userMessage,
      };

      const finalAssistantMsg: Message = {
        id: assistantMessageId,
        role: 'assistant',
        content: finalContent,
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
        id: generateUniqueId(),
        role: 'assistant',
        content: error instanceof Error ? `Bağlantı sorunu: ${error.message}` : 'Bağlantı sorunu yaşandı. Lütfen tekrar deneyin.',
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const messageText = inputValue;

    let activeChatId = currentChatId;
    if (!activeChatId) {
      const newChat: Chat = {
        id: generateUniqueId(),
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

    const userMessage: Message = {
      id: generateUniqueId(),
      role: 'user',
      content: messageText,
    };

    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInputValue('');
    setIsLoading(true);

    let chatTitle = 'Yeni Sohbet';
    if (messages.length === 0 && messageText.length > 50) {
      chatTitle = messageText.substring(0, 50) + '...';
    } else if (messages.length === 0) {
      chatTitle = messageText;
    }

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

    try {
      await handleStreamMessage(messageText, activeChatId);
    } finally {
      setIsLoading(false);
    }
  };

  const currentChat = chats.find((c) => c.id === currentChatId);

  return (
    <div className="flex h-screen bg-background text-foreground overflow-hidden">
      {isMobile && isSidebarOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-background/80 backdrop-blur-sm z-40"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      <AnimatePresence mode="wait">
        {isSidebarOpen && (
          <motion.aside
            initial={{ x: -300, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -300, opacity: 0 }}
            transition={{ type: "spring", damping: 25, stiffness: 200 }}
            className={`fixed md:static top-0 left-0 h-screen w-72 bg-card border-r border-border flex flex-col z-50 ${
              isMobile ? 'shadow-2xl' : ''
            }`}
          >
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="p-4 border-b border-border"
            >
              <Link href="/" className="flex items-center gap-3 hover:opacity-80 transition group">
                <div className="relative">
                  <Image src="/logo.png" alt="MizanAI" width={36} height={36} className="rounded-xl border border-primary/20" />
                  <div className="absolute inset-0 rounded-xl bg-primary/20 opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
                <span className="font-bold text-lg">MizanAI</span>
              </Link>
              {isMobile && (
                <button
                  onClick={() => setIsSidebarOpen(false)}
                  className="absolute right-4 top-4 p-1 hover:bg-muted rounded-lg transition-colors"
                >
                  <X size={20} />
                </button>
              )}
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.15 }}
              className="p-4"
            >
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={createNewChat}
                className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-primary to-purple-600 hover:from-primary/90 hover:to-purple-600/90 py-3 px-4 rounded-xl font-medium transition-all shadow-lg shadow-primary/20"
              >
                <Plus size={20} />
                Yeni Sohbet
              </motion.button>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="flex-1 overflow-y-auto"
            >
              {isInitialLoading ? (
                <div className="p-4 space-y-3">
                  {[1, 2, 3].map((i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.1 }}
                      className="p-3 rounded-xl bg-muted/30"
                    >
                      <div className="h-4 bg-muted rounded w-3/4 mb-2 animate-pulse" />
                      <div className="h-3 bg-muted rounded w-1/3 animate-pulse" />
                    </motion.div>
                  ))}
                </div>
              ) : chats.length === 0 ? (
                <div className="p-4 text-center text-muted-foreground text-sm">
                  Henüz sohbet yok. Yeni sohbet oluşturun.
                </div>
              ) : (
                <div className="space-y-2 p-2">
                  {chats.map((chat, index) => (
                    <motion.div
                      key={chat.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.05 }}
                      onClick={() => loadChat(chat.id)}
                      className={`w-full text-left p-3 rounded-xl transition-all duration-200 flex items-start justify-between group cursor-pointer ${
                        currentChatId === chat.id
                          ? 'bg-primary/10 text-primary border border-primary/20'
                          : 'bg-muted/30 hover:bg-muted/50 text-muted-foreground hover:text-foreground'
                      }`}
                    >
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium truncate">
                          {chat.title}
                        </p>
                        <p className="text-xs text-muted-foreground mt-1">
                          {new Date(chat.createdAt).toLocaleDateString('tr-TR')}
                        </p>
                      </div>
                      <motion.button
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                        onClick={(e) => deleteChat(chat.id, e)}
                        className="ml-2 p-1.5 opacity-0 group-hover:opacity-100 hover:bg-destructive/20 rounded-lg transition-all"
                      >
                        <Trash2 size={16} />
                      </motion.button>
                    </motion.div>
                  ))}
                </div>
              )}
            </motion.div>
          </motion.aside>
        )}
      </AnimatePresence>

      <motion.main
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex-1 flex flex-col bg-background"
      >
        <motion.header
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="border-b border-border p-4 flex items-center justify-between bg-card/50 backdrop-blur-sm"
        >
          <div className="flex items-center gap-4">
            {isMobile && (
              <motion.button
                whileTap={{ scale: 0.9 }}
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                className="p-2 hover:bg-muted rounded-lg transition-colors"
              >
                <Menu size={24} />
              </motion.button>
            )}
            <div>
              <h2 className="text-lg font-semibold">
                {currentChat?.title || 'Sohbet Seçin'}
              </h2>
              {currentChat && (
                <p className="text-xs text-muted-foreground mt-0.5">
                  {currentChat.messages.length} mesaj
                </p>
              )}
            </div>
          </div>

          <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
            <Link
              href="/"
              className="flex items-center gap-2 px-4 py-2 bg-muted hover:bg-muted/80 rounded-lg text-sm transition-colors"
            >
              <Home size={16} />
              <span className="hidden sm:inline">Ana Sayfa</span>
            </Link>
          </motion.div>
        </motion.header>

        <div className="flex-1 overflow-y-auto p-4">
          <div className="max-w-4xl mx-auto space-y-6">
            {messages.length === 0 ? (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="h-full flex flex-col items-center justify-center text-center py-12"
              >
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", delay: 0.2 }}
                  className="mb-6 relative"
                >
                  <Image src="/logo.png" alt="MizanAI" width={80} height={80} className="rounded-2xl border-2 border-primary/20 shadow-lg shadow-primary/10" />
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                    className="absolute inset-0 rounded-2xl bg-gradient-to-br from-primary/30 to-purple-500/30 blur-lg"
                  />
                </motion.div>
                
                <motion.h3
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 }}
                  className="text-xl font-bold mb-2"
                >
                  MizanAI Asistan
                </motion.h3>
                <motion.p
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                  className="text-muted-foreground text-sm max-w-md mb-6"
                >
                  Türk siyasi partileri hakkında sorular sorun. CHP, AKP, MHP, İYİ, DEM, SP, ZP, BBP hakkında bilgi alabilirsiniz.
                </motion.p>
                
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 }}
                  className="flex flex-wrap gap-2 justify-center max-w-lg"
                >
                  {QUICK_QUESTIONS.map((q, i) => (
                    <motion.button
                      key={q}
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.5 + i * 0.05 }}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={() => setInputValue(q)}
                      className="px-4 py-2 bg-muted/50 hover:bg-muted hover:border-primary/30 border border-transparent rounded-lg text-sm transition-all"
                    >
                      {q}
                    </motion.button>
                  ))}
                </motion.div>
              </motion.div>
            ) : (
              <AnimatePresence mode="popLayout">
                {messages.map((message, index) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 20, scale: 0.98 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    transition={{ duration: 0.3, delay: index * 0.05 }}
                    className={`flex gap-4 ${
                      message.role === 'user' ? 'flex-row-reverse' : ''
                    }`}
                  >
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ delay: 0.1 }}
                      className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 overflow-hidden shadow-md"
                    >
                      {message.role === 'user' ? (
                        <div className="w-full h-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">
                          <User size={18} className="text-white" />
                        </div>
                      ) : (
                        <div className="relative">
                          <Image src="/logo.png" alt="AI" width={36} height={36} className="rounded-lg border border-primary/20" />
                        </div>
                      )}
                    </motion.div>

                    <div className={`max-w-md lg:max-w-2xl ${message.role === 'user' ? 'items-end' : 'items-start'}`}>
                      <motion.div
                        whileHover={{ scale: 1.01 }}
                        className={`p-4 rounded-2xl ${
                          message.role === 'user'
                            ? 'bg-gradient-to-br from-primary to-purple-600 text-white rounded-tr-md'
                            : 'bg-card border border-border text-foreground rounded-tl-md'
                        }`}
                      >
                        <div className="break-words prose prose-invert prose-sm max-w-none">
                          <ReactMarkdown
                            components={{
                              p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                              ul: ({ children }) => <ul className="list-disc list-inside mb-2 space-y-1">{children}</ul>,
                              ol: ({ children }) => <ol className="list-decimal list-inside mb-2 space-y-1">{children}</ol>,
                              li: ({ children }) => <li className="text-inherit">{children}</li>,
                              strong: ({ children }) => <strong className="font-bold text-inherit">{children}</strong>,
                              em: ({ children }) => <em className="italic">{children}</em>,
                              h1: ({ children }) => <h1 className="text-xl font-bold mb-2">{children}</h1>,
                              h2: ({ children }) => <h2 className="text-lg font-bold mb-2">{children}</h2>,
                              h3: ({ children }) => <h3 className="text-base font-bold mb-1">{children}</h3>,
                              code: ({ children }) => <code className="bg-muted px-1.5 py-0.5 rounded text-sm">{children}</code>,
                              blockquote: ({ children }) => <blockquote className="border-l-4 border-primary/50 pl-3 italic text-muted-foreground">{children}</blockquote>,
                            }}
                          >
                            {message.content}
                          </ReactMarkdown>
                        </div>
                      </motion.div>

                      {message.role === 'assistant' && (
                        <motion.div
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          transition={{ delay: 0.2 }}
                          className="mt-3 text-xs text-muted-foreground space-y-2"
                        >
                          {message.queryType && (
                            <p className="flex items-center gap-1">
                              <Sparkles className="w-3 h-3" />
                              Sorgu Tipi: {message.queryType}
                            </p>
                          )}
                          {message.sources && message.sources.length > 0 && (
                            <div className="flex flex-wrap gap-2">
                              {message.sources.map((source, idx) => {
                                const fileName = source.split(/[/\\]/).pop() || source;
                                const partyName = fileName.replace('.pdf', '').toUpperCase();
                                return (
                                  <motion.span
                                    key={idx}
                                    initial={{ opacity: 0, scale: 0.8 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    transition={{ delay: idx * 0.05 }}
                                    className="inline-flex items-center px-2.5 py-1 bg-primary/10 text-primary rounded-md"
                                  >
                                    {partyName}
                                  </motion.span>
                                );
                              })}
                            </div>
                          )}
                        </motion.div>
                      )}
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            )}

          {isLoading && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex gap-4 items-start"
            >
              <div className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 overflow-hidden shadow-md">
                <Image src="/logo.png" alt="AI" width={36} height={36} className="rounded-lg border border-primary/20" />
              </div>
              <div className="bg-card border border-border p-5 rounded-2xl rounded-tl-md min-w-[200px]">
                <div className="flex items-center gap-3">
                  <TypingIndicator />
                  <span className="text-sm text-muted-foreground">Araştırıyor...</span>
                </div>
              </div>
            </motion.div>
          )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="border-t border-border p-4 bg-card/50 backdrop-blur-sm"
        >
          <div className="flex gap-3 max-w-4xl mx-auto">
            <motion.input
              whileFocus={{ scale: 1.01 }}
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
              className="flex-1 bg-muted/50 border border-border rounded-xl px-4 py-3 text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/20 disabled:opacity-50 transition-all"
            />
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleSendMessage}
              disabled={isLoading || !inputValue.trim()}
              className="bg-gradient-to-r from-primary to-purple-600 hover:from-primary/90 hover:to-purple-600/90 disabled:opacity-50 disabled:cursor-not-allowed px-5 py-3 rounded-xl font-medium transition-all shadow-lg shadow-primary/20 flex items-center justify-center"
            >
              {isLoading ? (
                <Loader2 size={20} className="animate-spin" />
              ) : (
                <Send size={20} />
              )}
            </motion.button>
          </div>
        </motion.div>
      </motion.main>
    </div>
  );
}