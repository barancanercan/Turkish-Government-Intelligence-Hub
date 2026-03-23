"use client";

import Link from "next/link";
import Image from "next/image";
import { motion } from "framer-motion";
import { Github, Linkedin, Mail, Scale } from "lucide-react";

const FOOTER_LINKS = {
  product: [
    { label: "Ana Sayfa", href: "/" },
    { label: "Sohbete Başla", href: "/chat" },
    { label: "Hakkımızda", href: "/about" },
  ],
  parties: [
    { label: "CHP", href: "/chat?party=CHP" },
    { label: "AKP", href: "/chat?party=AKP" },
    { label: "MHP", href: "/chat?party=MHP" },
    { label: "Diğer Partiler", href: "/chat" },
  ],
  resources: [
    { label: "GitHub", href: "https://github.com/barancanercan/mizan-ai" },
    { label: "API Dokümantasyonu", href: "/about#api" },
  ],
};

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="relative border-t border-border bg-card/30 mt-16 overflow-hidden">
      <div className="absolute inset-0 -z-10">
        <div className="absolute inset-0 bg-gradient-to-t from-primary/5 to-transparent" />
        <div className="absolute bottom-0 left-1/4 w-[400px] h-[400px] bg-primary/10 rounded-full blur-[100px]" />
        <div className="absolute bottom-0 right-1/4 w-[300px] h-[300px] bg-purple-500/10 rounded-full blur-[80px]" />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-8 lg:gap-12">
          <div className="col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="flex items-center gap-3 mb-4"
            >
              <div className="relative">
                <Image
                  src="/logo.jpg"
                  alt="MizanAI"
                  width={40}
                  height={40}
                  className="rounded-xl"
                />
                <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/20 to-purple-500/20 opacity-50" />
              </div>
              <span className="text-xl font-bold">MizanAI</span>
            </motion.div>
            <motion.p
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="text-muted-foreground text-sm mb-6 max-w-xs"
            >
              Türkiye'nin yapay zeka destekli siyasi belge analiz platformu.
              8 siyasi partinin belgelerini karşılaştırın.
            </motion.p>
            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="flex items-center gap-4"
            >
              <Link
                href="https://github.com/barancanercan/mizan-ai"
                target="_blank"
                rel="noopener noreferrer"
                className="p-2.5 rounded-lg bg-muted/50 hover:bg-muted hover:text-primary text-muted-foreground transition-all duration-200"
                aria-label="GitHub"
              >
                <Github className="w-5 h-5" />
              </Link>
              <Link
                href="https://linkedin.com/in/barancanercan"
                target="_blank"
                rel="noopener noreferrer"
                className="p-2.5 rounded-lg bg-muted/50 hover:bg-muted hover:text-primary text-muted-foreground transition-all duration-200"
                aria-label="LinkedIn"
              >
                <Linkedin className="w-5 h-5" />
              </Link>
              <Link
                href="mailto:barancanercan@gmail.com"
                className="p-2.5 rounded-lg bg-muted/50 hover:bg-muted hover:text-primary text-muted-foreground transition-all duration-200"
                aria-label="Email"
              >
                <Mail className="w-5 h-5" />
              </Link>
            </motion.div>
          </div>

          <div>
            <motion.h4
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="font-semibold mb-4 text-sm uppercase tracking-wider text-muted-foreground"
            >
              Ürün
            </motion.h4>
            <ul className="space-y-3">
              {FOOTER_LINKS.product.map((link, index) => (
                <motion.li
                  key={link.label}
                  initial={{ opacity: 0, x: -10 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.05 }}
                >
                  <Link
                    href={link.href}
                    className="text-muted-foreground hover:text-foreground transition-colors text-sm"
                  >
                    {link.label}
                  </Link>
                </motion.li>
              ))}
            </ul>
          </div>

          <div>
            <motion.h4
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="font-semibold mb-4 text-sm uppercase tracking-wider text-muted-foreground"
            >
              Partiler
            </motion.h4>
            <ul className="space-y-3">
              {FOOTER_LINKS.parties.map((link, index) => (
                <motion.li
                  key={link.label}
                  initial={{ opacity: 0, x: -10 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.05 }}
                >
                  <Link
                    href={link.href}
                    className="text-muted-foreground hover:text-foreground transition-colors text-sm"
                  >
                    {link.label}
                  </Link>
                </motion.li>
              ))}
            </ul>
          </div>

          <div>
            <motion.h4
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="font-semibold mb-4 text-sm uppercase tracking-wider text-muted-foreground"
            >
              Kaynaklar
            </motion.h4>
            <ul className="space-y-3">
              {FOOTER_LINKS.resources.map((link, index) => (
                <motion.li
                  key={link.label}
                  initial={{ opacity: 0, x: -10 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.05 }}
                >
                  <Link
                    href={link.href}
                    target={link.href.startsWith('http') ? '_blank' : undefined}
                    rel={link.href.startsWith('http') ? 'noopener noreferrer' : undefined}
                    className="text-muted-foreground hover:text-foreground transition-colors text-sm"
                  >
                    {link.label}
                  </Link>
                </motion.li>
              ))}
            </ul>
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mt-12 pt-8 border-t border-border/50 flex flex-col sm:flex-row justify-between items-center gap-4"
        >
          <div className="flex items-center gap-2 text-muted-foreground text-sm">
            <Scale className="w-4 h-4 text-primary" />
            <span>&copy; {currentYear} MizanAI. Tüm hakları saklıdır.</span>
          </div>
          <p className="text-muted-foreground text-sm">
            Geliştirici:{" "}
            <Link
              href="https://github.com/barancanercan"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary hover:underline"
            >
              Baran Can Ercan
            </Link>
          </p>
        </motion.div>
      </div>
    </footer>
  );
}