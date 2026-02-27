"use client";

import Link from "next/link";
import { Github } from "lucide-react";

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-[#262626] bg-[#0a0a0a] mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex flex-col md:flex-row justify-between items-center gap-8">
          {/* Left - Copyright */}
          <div className="text-gray-400 text-sm">
            <p>&copy; {currentYear} MİZAN-AI. Tüm hakları saklıdır.</p>
          </div>

          {/* Right - Links */}
          <div className="flex items-center gap-6">
            <Link
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-400 hover:text-white transition-colors duration-200"
              aria-label="GitHub"
            >
              <Github className="w-5 h-5" />
            </Link>
            <Link
              href="/about"
              className="text-gray-400 hover:text-white transition-colors duration-200"
            >
              Hakkımızda
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
