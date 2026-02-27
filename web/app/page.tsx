"use client";

import Link from "next/link";
import { Brain, FileText, MessageSquare, Sparkles, Users } from "lucide-react";
import { Navbar } from "@/components";
import { Footer } from "@/components";

const PARTIES = [
  { id: "CHP", name: "Cumhuriyet Halk Partisi", color: "#FF0000" },
  { id: "AKP", name: "Adalet ve Kalkınma Partisi", color: "#E55100" },
  { id: "MHP", name: "Milliyetçi Hareket Partisi", color: "#0066FF" },
  { id: "İYİ", name: "İYİ Parti", color: "#FFD700" },
  { id: "DEM", name: "Halkların Eşitlik ve Demokrasi Partisi", color: "#9933FF" },
  { id: "SP", name: "Saadet Partisi", color: "#00AA00" },
  { id: "ZP", name: "Zafer Partisi", color: "#1e3a5f" },
  { id: "BBP", name: "Büyük Birlik Partisi", color: "#CC0000" },
];

export default function Home() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      <Navbar />

      {/* Hero Section */}
      <section className="pt-24 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto text-center">
          <div className="mb-6 inline-block">
            <span className="px-4 py-2 rounded-full bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 text-blue-400 text-sm font-medium">
              🚀 Siyasi Analiz Platformu
            </span>
          </div>

          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6 bg-gradient-to-r from-white via-blue-200 to-purple-200 bg-clip-text text-transparent">
            MİZAN-AI
          </h1>

          <p className="text-xl sm:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
            Türkiye'nin ilk yapay zeka destekli siyasi belge analiz platformu
          </p>

          <p className="text-gray-400 mb-10 max-w-2xl mx-auto">
            Multi-agent sistemimiz ile siyasi partilerin tüzük, program ve belgelerini analiz edin.
            Doğrulanabilir kaynaklar ile güvenilir bilgi alın.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            <Link
              href="/chat"
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-500 rounded-lg font-semibold hover:shadow-lg hover:shadow-blue-500/50 transition transform hover:scale-105"
            >
              <MessageSquare className="w-5 h-5 inline mr-2" />
              Sohbete Başla
            </Link>
            <Link
              href="/about"
              className="px-8 py-4 border border-gray-600 rounded-lg font-semibold hover:border-gray-400 transition"
            >
              Hakkımızda
            </Link>
          </div>

          {/* Scroll indicator */}
          <div className="animate-bounce flex justify-center">
            <svg
              className="w-6 h-6 text-gray-500"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
            </svg>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-transparent to-[#0f0f0f]">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl sm:text-5xl font-bold mb-4">Neden MİZAN-AI?</h2>
            <p className="text-gray-400 text-lg">En gelişmiş siyasi analiz araçları</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="group p-8 rounded-xl border border-[#262626] bg-[#0f0f0f] hover:border-blue-500/50 hover:bg-[#1a1a2e] transition transform hover:scale-105">
              <div className="mb-4 inline-block p-3 rounded-lg bg-blue-500/10">
                <Brain className="w-8 h-8 text-blue-500" />
              </div>
              <h3 className="text-xl font-bold mb-3">Multi-Agent Sistem</h3>
              <p className="text-gray-400">
                LangGraph ile güçlendirilmiş akıllı ajanlar, karmaşık siyasi soruları analiz etmek için koordineli çalışır.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="group p-8 rounded-xl border border-[#262626] bg-[#0f0f0f] hover:border-purple-500/50 hover:bg-[#1a1a2e] transition transform hover:scale-105">
              <div className="mb-4 inline-block p-3 rounded-lg bg-purple-500/10">
                <Users className="w-8 h-8 text-purple-500" />
              </div>
              <h3 className="text-xl font-bold mb-3">8 Siyasi Parti</h3>
              <p className="text-gray-400">
                Tüm partilerin tüzük, program ve resmi belgelerinin tam veritabanında arama yapın.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="group p-8 rounded-xl border border-[#262626] bg-[#0f0f0f] hover:border-green-500/50 hover:bg-[#1a1a2e] transition transform hover:scale-105">
              <div className="mb-4 inline-block p-3 rounded-lg bg-green-500/10">
                <FileText className="w-8 h-8 text-green-500" />
              </div>
              <h3 className="text-xl font-bold mb-3">Kaynak Gösterimli</h3>
              <p className="text-gray-400">
                Her yanıta doğrulanabilir kaynaklar eşlik eder. Bilginin nereden geldiğini her zaman görün.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Parties Section */}
      <section id="parties" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl sm:text-5xl font-bold mb-4">Erişilebilir Partiler</h2>
            <p className="text-gray-400 text-lg">Türkiye'nin tüm ana siyasi partileri</p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {PARTIES.map((party) => (
              <Link
                key={party.id}
                href={`/chat?party=${party.id}`}
                className="group p-6 rounded-xl border border-[#262626] bg-[#0f0f0f] hover:border-opacity-100 transition transform hover:scale-105 flex flex-col items-center text-center"
                style={{
                  borderColor: party.color + "40",
                  backgroundColor: party.color + "08",
                }}
              >
                <div
                  className="w-12 h-12 rounded-lg mb-4 group-hover:shadow-lg transition"
                  style={{
                    backgroundColor: party.color + "20",
                    borderLeft: `3px solid ${party.color}`,
                  }}
                />
                <h3 className="font-bold text-sm">{party.id}</h3>
                <p className="text-xs text-gray-500 mt-1">{party.name}</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-transparent to-[#0f0f0f]">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-blue-500 mb-2">8+</div>
              <p className="text-gray-400">Siyasi Parti</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-purple-500 mb-2">1000+</div>
              <p className="text-gray-400">Analiz Edilen Belge</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-green-500 mb-2">100%</div>
              <p className="text-gray-400">Kaynaklandırılmış</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-pink-500 mb-2">Real-time</div>
              <p className="text-gray-400">AI Analiz</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section id="cta" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 border border-blue-500/30 rounded-2xl p-12 text-center">
            <h2 className="text-4xl sm:text-5xl font-bold mb-4">Hemen Deneyin</h2>
            <p className="text-gray-300 text-lg mb-8 max-w-2xl mx-auto">
              Türk siyasi partileri hakkında merak ettiklerinizi sorun. Akıllı ajanlarımız anında cevapla...
            </p>
            <Link
              href="/chat"
              className="inline-block px-10 py-4 bg-gradient-to-r from-blue-600 to-blue-500 rounded-lg font-semibold hover:shadow-lg hover:shadow-blue-500/50 transition transform hover:scale-105"
            >
              <Sparkles className="w-5 h-5 inline mr-2" />
              Sohbete Başla
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
