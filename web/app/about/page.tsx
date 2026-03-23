'use client';

import { motion } from 'framer-motion';
import { ArrowRight, Github, Mail, Zap, Network, Shield, Search, Bot, Database, Sparkles, Cpu, Globe, FileText, Linkedin, ExternalLink, Code2, Layers, Brain } from 'lucide-react';
import Link from 'next/link';
import Image from 'next/image';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';
import { ScrollToTop } from '@/components/ScrollToTop';
import { StaggerContainer, StaggerItem } from '@/components/Animated';

const FEATURES = [
  {
    icon: Bot,
    title: 'Multi-Agent Yapay Zeka',
    description: 'LangGraph tabanlı Supervisor, Researcher, Analyst, Writer ve Critic ajanları koordineli çalışır.',
    color: 'blue',
  },
  {
    icon: Search,
    title: 'Akıllı Arama Pipeline',
    description: 'Sorgu analizi, parti tespiti, web araması ve sonuç sentezleme tek pipeline\'da.',
    color: 'purple',
  },
  {
    icon: Database,
    title: 'Vektör Veritabanı',
    description: 'ChromaDB ile semantik arama ve parti bazlı filtreleme. BGE-M3 Türkçe embeddings.',
    color: 'green',
  },
  {
    icon: Shield,
    title: 'Güvenlik Katmanı',
    description: 'İçerik filtresi, JWT kimlik doğrulama, CORS kontrolü ve XSS koruması.',
    color: 'orange',
  },
  {
    icon: Globe,
    title: 'Web Entegrasyonu',
    description: 'DuckDuckGo araması ve Wikipedia entegrasyonu ile güncel bilgi erişimi.',
    color: 'cyan',
  },
  {
    icon: Sparkles,
    title: 'Gerçek Zamanlı Akış',
    description: 'SSE ile cümle bazlı streaming ve yazıyor animasyonu.',
    color: 'pink',
  },
];

const STATS = [
  { value: '8', label: 'Siyasi Parti', suffix: '' },
  { value: '1000+', label: 'Belge', suffix: '+' },
  { value: '%100', label: 'Kaynak', suffix: '' },
  { value: 'Real-time', label: 'AI', suffix: '' },
];

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-background text-foreground overflow-x-hidden">
      <Navbar />
      <ScrollToTop />

      <main>
        {/* Hero Section */}
        <section className="relative overflow-hidden px-6 py-32 sm:py-40">
          <div className="absolute inset-0 -z-10">
            <div className="absolute inset-0 bg-gradient-to-br from-background via-background to-primary/5" />
            <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-primary/10 rounded-full blur-[120px]" />
            <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-purple-500/10 rounded-full blur-[100px]" />
          </div>

          <div className="max-w-5xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="mb-8"
            >
              <div className="relative inline-block mb-6">
                <Image
                  src="/logo.jpg"
                  alt="MizanAI"
                  width={120}
                  height={120}
                  className="rounded-2xl border-2 border-primary/30 shadow-2xl shadow-primary/20"
                  priority
                />
                <motion.div
                  animate={{ scale: [1, 1.1, 1], opacity: [0.3, 0.5, 0.3] }}
                  transition={{ duration: 3, repeat: Infinity }}
                  className="absolute inset-0 rounded-2xl bg-gradient-to-br from-primary/40 via-purple-500/20 to-transparent"
                />
              </div>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-6"
            >
              <span className="relative">
                <span className="absolute inset-0 blur-2xl bg-gradient-to-r from-primary via-purple-500 to-blue-500 opacity-30 rounded-lg" />
                <span className="relative bg-gradient-to-r from-white via-blue-100 to-purple-200 bg-clip-text text-transparent">
                  MizanAI
                </span>
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-xl sm:text-2xl text-gray-300 mb-6 max-w-2xl mx-auto"
            >
              Türkiye'nin İlk Yapay Zeka Destekli
              <br />
              <span className="text-primary font-semibold">Siyasi Belge Analiz Platformu</span>
            </motion.p>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="text-gray-400 text-lg mb-12 max-w-xl mx-auto"
            >
              8 siyasi partinin tüzük, program ve belgelerini yapay zeka ile analiz edin.
              Doğrulanabilir kaynaklar ile güvenilir bilgi alın.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="flex flex-col sm:flex-row gap-4 justify-center"
            >
              <Link
                href="/chat"
                className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-primary to-purple-600 rounded-xl font-semibold text-white shadow-lg shadow-primary/25 hover:shadow-glow-md transition-all"
              >
                Sohbete Başla
                <ArrowRight className="w-5 h-5" />
              </Link>
            </motion.div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="px-6 py-16 border-y border-border/50">
          <div className="max-w-5xl mx-auto">
            <StaggerContainer className="grid grid-cols-2 md:grid-cols-4 gap-8" delay={0.05}>
              {STATS.map((stat, index) => (
                <StaggerItem key={stat.label}>
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.1 }}
                    className="text-center"
                  >
                    <div className="text-3xl sm:text-4xl font-bold text-primary mb-1">
                      {stat.value}
                      {stat.suffix}
                    </div>
                    <div className="text-gray-400 text-sm">{stat.label}</div>
                  </motion.div>
                </StaggerItem>
              ))}
            </StaggerContainer>
          </div>
        </section>

        {/* Mission & Vision Section */}
        <section className="px-6 py-24">
          <div className="max-w-5xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <h2 className="text-3xl sm:text-4xl font-bold mb-4">Misyon & Vizyon</h2>
              <p className="text-gray-400 text-lg">Demokratik bilgi erişimi için teknoloji</p>
            </motion.div>

            <div className="grid md:grid-cols-2 gap-8">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5 }}
                className="relative p-8 rounded-2xl border border-border bg-card/50 hover:bg-card hover:border-primary/30 transition-all duration-300"
              >
                <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-primary/5 to-transparent opacity-0 hover:opacity-100 transition-opacity" />
                <div className="relative">
                  <div className="flex items-center mb-4">
                    <div className="p-3 rounded-xl bg-primary/10 text-primary mr-3">
                      <Zap className="w-6 h-6" />
                    </div>
                    <h3 className="text-2xl font-bold">Misyonumuz</h3>
                  </div>
                  <p className="text-gray-300 leading-relaxed">
                    Türk siyasi bilgilerine erişimi demokratikleştirmek ve herkesin 
                    şeffaf, doğru bilgiye kolayca ulaşabilmesini sağlamak. Yapay zeka 
                    teknolojisini kullanarak siyasi belgelerin analizini herkes için 
                    erişilebilir hale getirmek.
                  </p>
                </div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: 0.1 }}
                className="relative p-8 rounded-2xl border border-border bg-card/50 hover:bg-card hover:border-purple-500/30 transition-all duration-300"
              >
                <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-purple-500/5 to-transparent opacity-0 hover:opacity-100 transition-opacity" />
                <div className="relative">
                  <div className="flex items-center mb-4">
                    <div className="p-3 rounded-xl bg-purple-500/10 text-purple-500 mr-3">
                      <Network className="w-6 h-6" />
                    </div>
                    <h3 className="text-2xl font-bold">Vizyonumuz</h3>
                  </div>
                  <p className="text-gray-300 leading-relaxed">
                    Yapay zeka teknolojisi ile desteklenen, şeffaf ve güvenilir 
                    bir siyasi bilgi platformu olmak. Türkiye'nin siyasi partilerini 
                    karşılaştırabileceğiniz, politikalarını analiz edebileceğiniz 
                    tek adres olmak.
                  </p>
                </div>
              </motion.div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="px-6 py-24 border-t border-border/50">
          <div className="max-w-5xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <h2 className="text-3xl sm:text-4xl font-bold mb-4">Teknik Özellikler</h2>
              <p className="text-gray-400 text-lg">Modern mimari ile güçlü altyapı</p>
            </motion.div>

            <StaggerContainer className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6" delay={0.08}>
              {FEATURES.map((feature) => (
                <StaggerItem key={feature.title}>
                  <motion.div
                    whileHover={{ y: -5 }}
                    className="relative p-6 rounded-2xl border border-border bg-card/50 hover:bg-card transition-all duration-300 h-full"
                  >
                    <div className={`absolute inset-0 rounded-2xl bg-gradient-to-br ${
                      feature.color === 'blue' ? 'from-primary/5' :
                      feature.color === 'purple' ? 'from-purple-500/5' :
                      feature.color === 'green' ? 'from-green-500/5' :
                      feature.color === 'orange' ? 'from-orange-500/5' :
                      feature.color === 'cyan' ? 'from-cyan-500/5' :
                      'from-pink-500/5'
                    } to-transparent opacity-0 hover:opacity-100 transition-opacity`} />
                    
                    <div className="relative">
                      <div className={`p-3 rounded-xl mb-4 inline-flex ${
                        feature.color === 'blue' ? 'bg-blue-500/10 text-blue-500' :
                        feature.color === 'purple' ? 'bg-purple-500/10 text-purple-500' :
                        feature.color === 'green' ? 'bg-green-500/10 text-green-500' :
                        feature.color === 'orange' ? 'bg-orange-500/10 text-orange-500' :
                        feature.color === 'cyan' ? 'bg-cyan-500/10 text-cyan-500' :
                        'bg-pink-500/10 text-pink-500'
                      }`}>
                        <feature.icon className="w-6 h-6" />
                      </div>
                      <h3 className="font-bold text-lg mb-2">{feature.title}</h3>
                      <p className="text-gray-400 text-sm leading-relaxed">{feature.description}</p>
                    </div>
                  </motion.div>
                </StaggerItem>
              ))}
            </StaggerContainer>
          </div>
        </section>

        {/* Technology Stack Section */}
        <section className="px-6 py-24 border-t border-border/50">
          <div className="max-w-5xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <h2 className="text-3xl sm:text-4xl font-bold mb-4">Teknoloji Stack</h2>
              <p className="text-gray-400 text-lg">Endüstri standartlarına uygun modern teknolojiler</p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="relative rounded-2xl border border-border bg-card/50 p-8"
            >
              <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {[
                  { icon: Cpu, name: 'Ollama', desc: 'Local LLM' },
                  { icon: Bot, name: 'LangGraph', desc: 'Multi-Agent' },
                  { icon: Database, name: 'ChromaDB', desc: 'Vector Store' },
                  { icon: Search, name: 'DuckDuckGo', desc: 'Web Search' },
                  { icon: FileText, name: 'BGE-M3', desc: 'Embeddings' },
                  { icon: Globe, name: 'Wikipedia', desc: 'Bilgi Kaynağı' },
                  { icon: Shield, name: 'FastAPI', desc: 'REST API' },
                  { icon: Sparkles, name: 'Next.js 15', desc: 'Frontend' },
                ].map((tech, index) => (
                  <motion.div
                    key={tech.name}
                    initial={{ opacity: 0, scale: 0.9 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.05 }}
                    className="flex items-center gap-3 p-4 rounded-xl bg-muted/30 hover:bg-muted/50 transition-colors"
                  >
                    <tech.icon className="w-8 h-8 text-primary flex-shrink-0" />
                    <div>
                      <div className="font-semibold text-sm">{tech.name}</div>
                      <div className="text-xs text-gray-500">{tech.desc}</div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </div>
        </section>

        {/* Developer Section */}
        <section id="developer" className="px-6 py-24 border-t border-border/50">
          <div className="max-w-4xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-12"
            >
              <h2 className="text-3xl sm:text-4xl font-bold mb-4">Geliştirici</h2>
              <p className="text-gray-400 text-lg">Bu projenin arkasındaki mühendis</p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="relative rounded-2xl border border-primary/20 bg-gradient-to-br from-primary/10 via-card to-purple-500/10 p-8 md:p-12"
            >
              <div className="flex flex-col md:flex-row items-center gap-8">
                <div className="relative">
                  <div className="w-32 h-32 rounded-2xl bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center text-5xl font-bold text-white shadow-2xl shadow-primary/30">
                    BC
                  </div>
                  <motion.div
                    animate={{ scale: [1, 1.1, 1], opacity: [0.3, 0.5, 0.3] }}
                    transition={{ duration: 3, repeat: Infinity }}
                    className="absolute -inset-2 rounded-3xl bg-gradient-to-br from-primary/30 to-purple-500/30 blur-xl -z-10"
                  />
                </div>

                <div className="flex-1 text-center md:text-left">
                  <h3 className="text-2xl font-bold mb-2">Baran Can Ercan</h3>
                  <p className="text-primary font-medium mb-4">AI/ML Engineer & Full-Stack Developer</p>
                  <p className="text-gray-300 leading-relaxed mb-6">
                    Yapay zeka, makine öğrenmesi ve doğal dil işleme alanlarında uzmanlaşmış bir mühendis.
                    MizanAI, domain-specific RAG sistemleri, multi-agent mimarileri ve production-ready
                    AI uygulamaları geliştirme konusundaki uzmanlığımı sergileyen bir projedir.
                  </p>

                  <div className="flex flex-wrap gap-2 justify-center md:justify-start mb-6">
                    {['LangChain', 'LangGraph', 'RAG', 'Multi-Agent', 'FastAPI', 'Next.js', 'Python', 'TypeScript'].map((skill) => (
                      <span
                        key={skill}
                        className="px-3 py-1 text-xs font-medium bg-primary/10 text-primary rounded-full border border-primary/20"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>

                  <div className="flex flex-wrap gap-3 justify-center md:justify-start">
                    <a
                      href="https://linkedin.com/in/barancanercan"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-[#0077B5] hover:bg-[#006699] text-white font-medium transition-colors"
                    >
                      <Linkedin className="w-4 h-4" />
                      LinkedIn
                    </a>
                    <a
                      href="https://github.com/barancanercan"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-muted hover:bg-muted/80 border border-border transition-colors"
                    >
                      <Github className="w-4 h-4" />
                      GitHub
                    </a>
                    <a
                      href="mailto:barancanercan@gmail.com"
                      className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-muted hover:bg-muted/80 border border-border transition-colors"
                    >
                      <Mail className="w-4 h-4" />
                      E-posta
                    </a>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Project Highlights Section */}
        <section className="px-6 py-24 border-t border-border/50">
          <div className="max-w-5xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-12"
            >
              <h2 className="text-3xl sm:text-4xl font-bold mb-4">Proje Öne Çıkanları</h2>
              <p className="text-gray-400 text-lg">Bu projede kullanılan ileri seviye teknikler</p>
            </motion.div>

            <div className="grid md:grid-cols-3 gap-6">
              {[
                {
                  icon: Brain,
                  title: 'Domain-Specific RAG',
                  description: 'Türk siyasi belgelerine özel optimize edilmiş Retrieval-Augmented Generation sistemi. Türkçe BGE-M3 embeddings ile yüksek doğruluk.',
                  color: 'blue'
                },
                {
                  icon: Layers,
                  title: 'Multi-Agent Orchestration',
                  description: 'LangGraph ile koordine çalışan Supervisor, Researcher, Analyst ve Writer ajanları. Karmaşık sorguları böl-yönet stratejisi ile çözüm.',
                  color: 'purple'
                },
                {
                  icon: Code2,
                  title: 'Production-Ready Architecture',
                  description: 'FastAPI + Next.js 15 ile SSE streaming, JWT auth, CORS, retry logic ve graceful error handling. Deployment-ready kod kalitesi.',
                  color: 'green'
                },
              ].map((item, index) => (
                <motion.div
                  key={item.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="relative p-6 rounded-2xl border border-border bg-card/50 hover:bg-card hover:border-primary/30 transition-all duration-300"
                >
                  <div className={`p-3 rounded-xl mb-4 inline-flex ${
                    item.color === 'blue' ? 'bg-blue-500/10 text-blue-500' :
                    item.color === 'purple' ? 'bg-purple-500/10 text-purple-500' :
                    'bg-green-500/10 text-green-500'
                  }`}>
                    <item.icon className="w-6 h-6" />
                  </div>
                  <h3 className="font-bold text-lg mb-2">{item.title}</h3>
                  <p className="text-gray-400 text-sm leading-relaxed">{item.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="px-6 py-24 border-t border-border/50">
          <div className="max-w-3xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              className="relative rounded-2xl p-12 overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-background to-purple-500/20" />
              <div className="relative z-10">
                <h2 className="text-3xl sm:text-4xl font-bold mb-4">Hazır mısınız?</h2>
                <p className="text-gray-300 text-lg mb-8 max-w-xl mx-auto">
                  Türk siyasi partileri hakkında merak ettiklerinizi sorun. 
                  Yapay zeka destekli analizimiz anında cevaplasın.
                </p>
                <Link
                  href="/chat"
                  className="inline-flex items-center gap-3 px-10 py-5 bg-gradient-to-r from-primary to-purple-600 rounded-xl font-semibold text-white shadow-lg shadow-primary/25 hover:shadow-glow-md transition-all"
                >
                  <Sparkles className="w-5 h-5" />
                  Sohbete Başla
                  <ArrowRight className="w-5 h-5" />
                </Link>
              </div>
            </motion.div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}