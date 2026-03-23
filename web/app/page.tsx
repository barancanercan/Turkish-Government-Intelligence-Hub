"use client";

import Link from "next/link";
import Image from "next/image";
import { motion } from "framer-motion";
import { Brain, FileText, MessageSquare, Sparkles, Users, ArrowRight, Scale, Search, Zap, Shield, BookOpen } from "lucide-react";
import { Navbar } from "@/components";
import { Footer } from "@/components";
import { ScrollToTop } from "@/components/ScrollToTop";
import { StaggerContainer, StaggerItem } from "@/components/Animated";

const PARTIES = [
  { id: "CHP", name: "Cumhuriyet Halk Partisi", color: "#FF0000", shortName: "CHP" },
  { id: "AKP", name: "Adalet ve Kalkınma Partisi", color: "#E55100", shortName: "AKP" },
  { id: "MHP", name: "Milliyetçi Hareket Partisi", color: "#0066FF", shortName: "MHP" },
  { id: "İYİ", name: "İYİ Parti", color: "#FFD700", shortName: "İYİ" },
  { id: "DEM", name: "Halkların Eşitlik ve Demokrasi Partisi", color: "#9933FF", shortName: "DEM" },
  { id: "SP", name: "Saadet Partisi", color: "#00AA00", shortName: "SP" },
  { id: "ZP", name: "Zafer Partisi", color: "#1e3a5f", shortName: "ZP" },
  { id: "BBP", name: "Büyük Birlik Partisi", color: "#CC0000", shortName: "BBP" },
];

const FEATURES = [
  {
    icon: Search,
    title: "Anında Cevap",
    description: "\"AKP'nin ekonomi politikası nedir?\" gibi sorulara saniyeler içinde, kaynaklı yanıtlar alın.",
    color: "blue",
  },
  {
    icon: Scale,
    title: "Parti Karşılaştırma",
    description: "\"CHP ile MHP'nin eğitim politikalarını karşılaştır\" deyin, detaylı analiz alın.",
    color: "purple",
  },
  {
    icon: FileText,
    title: "Belge Analizi",
    description: "Parti tüzükleri, seçim beyannameleri ve programlardan doğrudan alıntılarla yanıt.",
    color: "green",
  },
  {
    icon: Shield,
    title: "Doğrulanabilir Bilgi",
    description: "Her bilginin kaynağı gösterilir. Manipülasyona karşı şeffaf ve güvenilir.",
    color: "orange",
  },
];

const USE_CASES = [
  {
    question: "Hangi parti asgari ücreti artırmayı vadediyor?",
    answer: "Partilerin ekonomi programlarını tarayarak karşılaştırmalı tablo sunar.",
  },
  {
    question: "AKP ile CHP'nin dış politika farkları neler?",
    answer: "Her iki partinin resmi belgelerinden alıntılarla analiz yapar.",
  },
  {
    question: "MHP'nin göç politikası nedir?",
    answer: "Parti programından ilgili maddeleri bulup özetler.",
  },
];

const STATS = [
  { value: "8+", label: "Siyasi Parti", color: "text-blue-500" },
  { value: "1000+", label: "Analiz Edilen Belge", color: "text-purple-500" },
  { value: "100%", label: "Kaynaklandırılmış", color: "text-green-500" },
  { value: "Real-time", label: "AI Analiz", color: "text-pink-500" },
];

export default function Home() {
  return (
    <div className="min-h-screen bg-background text-foreground overflow-x-hidden">
      <Navbar />
      <ScrollToTop />

      <main>
        {/* Hero Section */}
        <section className="relative min-h-screen flex items-center justify-center pt-20 pb-16 px-4 sm:px-6 lg:px-8 overflow-hidden">
          {/* Animated Background */}
          <div className="absolute inset-0 -z-10">
            <div className="absolute inset-0 bg-gradient-to-br from-background via-background to-primary/5" />
            <div className="absolute top-1/4 left-1/4 w-[600px] h-[600px] bg-primary/10 rounded-full blur-[120px] animate-pulse-glow" />
            <div className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-purple-500/10 rounded-full blur-[100px] animate-pulse-glow" style={{ animationDelay: "1s" }} />
            <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-background/50" />
          </div>

          <div className="max-w-6xl mx-auto text-center relative z-10">
            <StaggerContainer delay={0.1}>
              <StaggerItem>
                <motion.div
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.6 }}
                  className="mb-8"
                >
                  <div className="relative inline-block">
                    <div className="relative">
                      <Image
                        src="/logo.png"
                        alt="MizanAI"
                        width={160}
                        height={160}
                        className="mx-auto rounded-2xl border-2 border-primary/30 shadow-2xl shadow-primary/20"
                        priority
                      />
                      <motion.div
                        animate={{ scale: [1, 1.05, 1], opacity: [0.3, 0.5, 0.3] }}
                        transition={{ duration: 3, repeat: Infinity }}
                        className="absolute inset-0 rounded-2xl bg-gradient-to-br from-primary/40 via-purple-500/20 to-transparent"
                      />
                    </div>
                    <motion.div
                      animate={{ scale: [1, 1.3, 1], opacity: [0.2, 0.4, 0.2] }}
                      transition={{ duration: 4, repeat: Infinity }}
                      className="absolute -inset-4 rounded-3xl bg-gradient-to-r from-primary/20 via-purple-500/10 to-blue-500/20 blur-2xl -z-10"
                    />
                  </div>
                </motion.div>
              </StaggerItem>

              <StaggerItem>
                <motion.h1
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.2 }}
                  className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-4"
                >
                  <span className="relative">
                    <span className="absolute inset-0 blur-2xl bg-gradient-to-r from-primary via-purple-500 to-blue-500 opacity-30 rounded-lg" />
                    <span className="relative bg-gradient-to-r from-white via-blue-100 to-purple-200 bg-clip-text text-transparent">
                      MizanAI
                    </span>
                  </span>
                </motion.h1>
              </StaggerItem>

              <StaggerItem>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.25 }}
                  className="flex flex-col items-center gap-3 mb-6"
                >
                  {/* Dictionary Meaning */}
                  <div className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-primary/10 to-purple-500/10 border border-primary/20 rounded-xl">
                    <BookOpen className="w-4 h-4 text-primary" />
                    <span className="text-sm text-gray-300">
                      <span className="text-primary font-medium">mizan</span>
                      <span className="text-gray-500 mx-2">|</span>
                      <span className="italic">isim, Arapça</span>
                      <span className="text-gray-500 mx-2">•</span>
                      <span>terazi, denge, ölçü</span>
                    </span>
                  </div>

                  {/* GitHub Badge */}
                  <a
                    href="https://github.com/barancanercan/mizan-ai"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 px-4 py-1.5 bg-card/50 border border-border rounded-full text-sm text-gray-400 hover:text-white hover:border-primary/50 transition-all"
                  >
                    <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                    Open Source on GitHub
                  </a>
                </motion.div>
              </StaggerItem>

              <StaggerItem>
                <motion.p
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.3 }}
                  className="text-xl sm:text-2xl text-gray-300 mb-4 max-w-3xl mx-auto leading-relaxed"
                >
                  Türkiye'nin yapay zeka destekli siyasi belge analiz platformu
                </motion.p>
              </StaggerItem>

              <StaggerItem>
                <motion.p
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.4 }}
                  className="text-gray-400 mb-10 max-w-2xl mx-auto text-lg"
                >
                  8 siyasi partinin tüzük ve programlarını sorgulayın, karşılaştırın.
                  Her yanıt kaynak gösterimli, her bilgi doğrulanabilir.
                </motion.p>
              </StaggerItem>

              <StaggerItem>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.5 }}
                  className="flex flex-col sm:flex-row gap-4 justify-center mb-16"
                >
                  <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                    <Link
                      href="/chat"
                      className="inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-primary to-purple-600 rounded-xl font-semibold text-white shadow-lg shadow-primary/25 hover:shadow-glow-md transition-all duration-300 group"
                    >
                      <MessageSquare className="w-5 h-5 group-hover:animate-pulse" />
                      Sohbete Başla
                      <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </Link>
                  </motion.div>
                  <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                    <Link
                      href="/about"
                      className="inline-flex items-center gap-2 px-8 py-4 border border-border rounded-xl font-semibold text-gray-300 hover:text-white hover:border-gray-500 hover:bg-secondary/50 transition-all duration-200"
                    >
                      Hakkımızda
                    </Link>
                  </motion.div>
                </motion.div>
              </StaggerItem>

              {/* Scroll Indicator removed - was showing as "0" */}
            </StaggerContainer>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-24 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
          <div className="absolute inset-0 -z-10">
            <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-border to-transparent" />
            <div className="absolute bottom-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-border to-transparent" />
          </div>
          
          <div className="max-w-6xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl sm:text-5xl font-bold mb-4">Neden MİZAN-AI?</h2>
              <p className="text-gray-400 text-lg">En gelişmiş siyasi analiz araçları</p>
            </motion.div>

            <StaggerContainer className="grid md:grid-cols-2 lg:grid-cols-4 gap-6" delay={0.1}>
              {FEATURES.map((feature) => (
                <StaggerItem key={feature.title}>
                  <motion.div
                    whileHover={{ y: -8, transition: { duration: 0.3 } }}
                    className="group relative p-8 rounded-2xl border border-border bg-card/50 hover:bg-card hover:border-primary/30 transition-all duration-300 h-full flex flex-col"
                  >
                    <div className={`absolute inset-0 rounded-2xl bg-gradient-to-br ${
                      feature.color === 'blue' ? 'from-primary/5 to-transparent' :
                      feature.color === 'purple' ? 'from-purple-500/5 to-transparent' :
                      feature.color === 'green' ? 'from-green-500/5 to-transparent' :
                      'from-orange-500/5 to-transparent'
                    } opacity-0 group-hover:opacity-100 transition-opacity duration-300`} />

                    <div className={`relative inline-flex items-center justify-center w-14 h-14 rounded-xl mb-5 ${
                      feature.color === 'blue' ? 'bg-blue-500/10 text-blue-500' :
                      feature.color === 'purple' ? 'bg-purple-500/10 text-purple-500' :
                      feature.color === 'green' ? 'bg-green-500/10 text-green-500' :
                      'bg-orange-500/10 text-orange-500'
                    }`}>
                      <feature.icon className="w-7 h-7" />
                    </div>

                    <h3 className="relative text-lg font-bold mb-3 text-foreground group-hover:text-white transition-colors">
                      {feature.title}
                    </h3>
                    <p className="relative text-gray-400 text-sm leading-relaxed flex-grow">
                      {feature.description}
                    </p>

                    <motion.div
                      initial={{ scaleX: 0 }}
                      whileHover={{ scaleX: 1 }}
                      className={`absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r ${
                        feature.color === 'blue' ? 'from-blue-500 to-cyan-400' :
                        feature.color === 'purple' ? 'from-purple-500 to-pink-500' :
                        feature.color === 'green' ? 'from-green-500 to-emerald-400' :
                        'from-orange-500 to-amber-400'
                      } origin-left rounded-full`}
                    />
                  </motion.div>
                </StaggerItem>
              ))}
            </StaggerContainer>
          </div>
        </section>

        {/* Use Cases Section */}
        <section className="py-24 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
          <div className="absolute inset-0 -z-10">
            <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-border to-transparent" />
          </div>

          <div className="max-w-6xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl sm:text-5xl font-bold mb-4">Ne Sorabilirsiniz?</h2>
              <p className="text-gray-400 text-lg">Gerçek kullanım senaryoları</p>
            </motion.div>

            <div className="grid md:grid-cols-3 gap-6">
              {USE_CASES.map((useCase, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                  className="relative p-6 rounded-2xl border border-border bg-card/30 hover:bg-card/50 transition-all group"
                >
                  <div className="flex items-start gap-3 mb-4">
                    <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
                      <MessageSquare className="w-4 h-4 text-primary" />
                    </div>
                    <p className="text-white font-medium leading-relaxed">"{useCase.question}"</p>
                  </div>
                  <div className="flex items-start gap-3 pl-11">
                    <Zap className="w-4 h-4 text-green-500 flex-shrink-0 mt-0.5" />
                    <p className="text-gray-400 text-sm">{useCase.answer}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Parties Section */}
        <section id="parties" className="py-24 px-4 sm:px-6 lg:px-8 relative">
          <div className="absolute inset-0 -z-10">
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] bg-primary/5 rounded-full blur-[120px]" />
          </div>

          <div className="max-w-6xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl sm:text-5xl font-bold mb-4">Desteklenen Partiler</h2>
              <p className="text-gray-400 text-lg">8 siyasi partinin tüzük ve programlarına erişin</p>
            </motion.div>

            <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-4">
              {PARTIES.map((party, index) => (
                <motion.div
                  key={party.id}
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.3, delay: index * 0.05 }}
                >
                  <Link href={`/chat?party=${party.id}`} className="group block">
                    <motion.div
                      whileHover={{ y: -8, scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      className="relative p-4 rounded-2xl border border-border/50 bg-card/30 backdrop-blur-sm hover:border-opacity-100 transition-all duration-300 text-center"
                      style={{ borderColor: `${party.color}40` }}
                    >
                      <div
                        className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                        style={{ background: `linear-gradient(135deg, ${party.color}10 0%, transparent 100%)` }}
                      />
                      <div
                        className="relative w-14 h-14 mx-auto rounded-xl flex items-center justify-center text-xl font-bold mb-3 transition-transform group-hover:scale-110"
                        style={{
                          backgroundColor: `${party.color}15`,
                          color: party.color,
                          boxShadow: `0 4px 20px ${party.color}20`
                        }}
                      >
                        {party.shortName}
                      </div>
                      <p className="relative text-xs text-gray-400 group-hover:text-gray-300 transition-colors line-clamp-2 min-h-[32px]">
                        {party.name}
                      </p>
                    </motion.div>
                  </Link>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="py-24 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
          <div className="absolute inset-0 -z-10 bg-gradient-to-b from-transparent via-primary/5 to-transparent" />
          
          <div className="max-w-6xl mx-auto">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {STATS.map((stat, index) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                  className="text-center"
                >
                  <motion.div
                    initial={{ scale: 0 }}
                    whileInView={{ scale: 1 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5, delay: index * 0.1 + 0.2, type: "spring" }}
                    className={`text-4xl sm:text-5xl font-bold mb-2 ${stat.color}`}
                  >
                    {stat.value}
                  </motion.div>
                  <p className="text-gray-400 text-sm">{stat.label}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section id="cta" className="py-24 px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="relative overflow-hidden rounded-3xl p-12 text-center"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-background to-purple-500/20" />
              <div className="absolute inset-0 bg-gradient-to-b from-primary/5 via-transparent to-purple-500/5" />
              
              <div className="relative z-10">
                <motion.div
                  initial={{ scale: 0 }}
                  whileInView={{ scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                  className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-primary/20 text-primary mb-6"
                >
                  <Sparkles className="w-8 h-8" />
                </motion.div>
                
                <h2 className="text-4xl sm:text-5xl font-bold mb-4">Hemen Deneyin</h2>
                <p className="text-gray-300 text-lg mb-8 max-w-xl mx-auto">
                  Türk siyasi partileri hakkında merak ettiklerinizi sorun. Akıllı ajanlarımız anında cevaplasın.
                </p>
                
                <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                  <Link
                    href="/chat"
                    className="inline-flex items-center gap-3 px-10 py-5 bg-gradient-to-r from-primary to-purple-600 rounded-xl font-semibold text-white shadow-lg shadow-primary/25 hover:shadow-glow-md transition-all duration-300 group"
                  >
                    <Sparkles className="w-5 h-5 group-hover:animate-pulse" />
                    Sohbete Başla
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </Link>
                </motion.div>
              </div>
            </motion.div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}