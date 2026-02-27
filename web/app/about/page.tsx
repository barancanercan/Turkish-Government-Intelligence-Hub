'use client';

import { ArrowRight, Github, Mail, Zap, Network } from 'lucide-react';
import Link from 'next/link';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      <Navbar />

      {/* Hero Section */}
      <section className="relative overflow-hidden px-6 py-20 sm:py-32">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl sm:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            Biz Kimiz?
          </h1>
          <p className="text-xl sm:text-2xl text-gray-300 mb-12">
            Mizan-AI Hakkında
          </p>
          <div className="w-16 h-1 bg-gradient-to-r from-blue-500 to-cyan-500"></div>
        </div>
      </section>

      {/* Mission & Vision Section */}
      <section className="px-6 py-20 border-t border-gray-800">
        <div className="max-w-4xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12">
            {/* Mission */}
            <div className="bg-gradient-to-br from-gray-900 to-gray-950 rounded-lg p-8 border border-gray-800">
              <div className="flex items-center mb-4">
                <Zap className="w-6 h-6 text-blue-400 mr-3" />
                <h2 className="text-2xl font-bold">Misyon</h2>
              </div>
              <p className="text-gray-300 leading-relaxed">
                Türk siyasi bilgilerine erişimi demokratikleştirmek ve herkesin şeffaf, doğru bilgiye kolayca ulaşabilmesini sağlamak.
              </p>
            </div>

            {/* Vision */}
            <div className="bg-gradient-to-br from-gray-900 to-gray-950 rounded-lg p-8 border border-gray-800">
              <div className="flex items-center mb-4">
                <Network className="w-6 h-6 text-cyan-400 mr-3" />
                <h2 className="text-2xl font-bold">Vizyon</h2>
              </div>
              <p className="text-gray-300 leading-relaxed">
                Yapay zeka teknolojisi ile desteklenen, şeffaf ve güvenilir bir siyasi bilgi platformu olmak.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-6 py-20 border-t border-gray-800">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold mb-12">Proje Özellikleri</h2>
          <div className="grid sm:grid-cols-2 gap-6">
            <div className="bg-gray-900/50 rounded-lg p-6 border border-gray-800">
              <h3 className="font-semibold text-blue-400 mb-2">Tool-Augmented RAG (T-RAG)</h3>
              <p className="text-gray-400">Gelişmiş mimarisi ile doğru ve güvenilir yanıtlar sunar.</p>
            </div>
            <div className="bg-gray-900/50 rounded-lg p-6 border border-gray-800">
              <h3 className="font-semibold text-cyan-400 mb-2">LangGraph Multi-Agent</h3>
              <p className="text-gray-400">Orchestration teknolojisi ile kompleks görevleri çözer.</p>
            </div>
            <div className="bg-gray-900/50 rounded-lg p-6 border border-gray-800">
              <h3 className="font-semibold text-blue-400 mb-2">8 Siyasi Partinin Kaynakları</h3>
              <p className="text-gray-400">Tüzük ve programları güvenli veritabanında saklanır.</p>
            </div>
            <div className="bg-gray-900/50 rounded-lg p-6 border border-gray-800">
              <h3 className="font-semibold text-cyan-400 mb-2">ChromaDB Vektör Veritabanı</h3>
              <p className="text-gray-400">Hızlı ve etkili semantik arama imkanı sağlar.</p>
            </div>
            <div className="sm:col-span-2 bg-gray-900/50 rounded-lg p-6 border border-gray-800">
              <h3 className="font-semibold text-blue-400 mb-2">BGE-M3 Türkçe Embeddings</h3>
              <p className="text-gray-400">Türkçe dil işleme konusunda optimize edilmiş embeddings kullanır.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Technology Stack Section */}
      <section className="px-6 py-20 border-t border-gray-800">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold mb-12">Teknoloji Stack</h2>
          <div className="bg-gradient-to-br from-gray-900 to-gray-950 rounded-lg p-8 border border-gray-800">
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-blue-500 rounded-full mr-3"></div>
                <span>Next.js</span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-cyan-500 rounded-full mr-3"></div>
                <span>FastAPI</span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-blue-500 rounded-full mr-3"></div>
                <span>LangChain</span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-cyan-500 rounded-full mr-3"></div>
                <span>ChromaDB</span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-blue-500 rounded-full mr-3"></div>
                <span>Ollama</span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-cyan-500 rounded-full mr-3"></div>
                <span>Tailwind CSS</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Developer Section */}
      <section className="px-6 py-20 border-t border-gray-800">
        <div className="max-w-4xl mx-auto">
          <div className="bg-gradient-to-r from-blue-900/20 to-cyan-900/20 rounded-lg p-8 border border-blue-800/30">
            <h2 className="text-2xl font-bold mb-6">Geliştirici</h2>
            <p className="text-gray-300 mb-6">
              Mizan-AI, <span className="font-semibold text-blue-400">Baran Can Ercan</span> tarafından geliştirilmektedir.
            </p>
            <a
              href="https://github.com/barancan"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center text-blue-400 hover:text-blue-300 transition"
            >
              <Github className="w-5 h-5 mr-2" />
              GitHub Profilini Ziyaret Et
              <ArrowRight className="w-4 h-4 ml-2" />
            </a>
          </div>
        </div>
      </section>

      {/* Contact & CTA Section */}
      <section className="px-6 py-20 border-t border-gray-800">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6">Sorularınız mı var?</h2>
          <p className="text-gray-300 mb-12 text-lg">
            Bize ulaşın veya doğrudan sohbete başlayın
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="mailto:barancanercan@gmail.com"
              className="inline-flex items-center justify-center px-8 py-3 rounded-lg bg-gray-900 border border-gray-700 text-white hover:bg-gray-800 transition"
            >
              <Mail className="w-5 h-5 mr-2" />
              E-posta Gönder
            </a>
            <Link
              href="/chat"
              className="inline-flex items-center justify-center px-8 py-3 rounded-lg bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold hover:from-blue-700 hover:to-cyan-700 transition"
            >
              Sohbete Başla
              <ArrowRight className="w-5 h-5 ml-2" />
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
