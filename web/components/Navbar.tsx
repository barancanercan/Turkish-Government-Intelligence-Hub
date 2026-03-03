"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { useSession, signOut } from "next-auth/react";
import { Menu, X, LogOut, LogIn } from "lucide-react";

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const { data: session } = useSession();

  const toggleMenu = () => setIsOpen(!isOpen);

  const navLinks = [
    { href: "/", label: "Ana Sayfa" },
    { href: "/chat", label: "Sohbet" },
    { href: "/about", label: "Hakkımızda" },
  ];

  return (
    <nav className="sticky top-0 z-50 backdrop-blur-md bg-[#0a0a0a]/80 border-b border-[#262626]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 font-bold text-xl group">
            <Image src="/logo.png" alt="MizanAI" width={36} height={36} className="rounded-lg" />
            <span className="text-white">MizanAI</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-gray-300 hover:text-white transition-colors duration-200"
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* Right side - Auth */}
          <div className="hidden md:flex items-center gap-4">
            {session?.user ? (
              <>
                <span className="text-gray-300 text-sm">{session.user.name || session.user.email}</span>
                <button
                  onClick={() => signOut()}
                  className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors duration-200"
                >
                  <LogOut className="w-4 h-4" />
                  Çıkış Yap
                </button>
              </>
            ) : (
              <Link
                href="/auth/signin"
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors duration-200"
              >
                <LogIn className="w-4 h-4" />
                Giriş Yap
              </Link>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={toggleMenu}
            className="md:hidden p-2 text-gray-300 hover:text-white transition-colors"
            aria-label="Toggle menu"
          >
            {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden border-t border-[#262626]">
            <div className="px-2 pt-2 pb-4 space-y-2">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="block px-3 py-2 text-gray-300 hover:text-white hover:bg-[#1a1a1a] rounded-lg transition-colors duration-200"
                  onClick={() => setIsOpen(false)}
                >
                  {link.label}
                </Link>
              ))}
              <div className="border-t border-[#262626] pt-2 mt-2">
                {session?.user ? (
                  <>
                    <div className="px-3 py-2 text-gray-300 text-sm">
                      {session.user.name || session.user.email}
                    </div>
                    <button
                      onClick={() => {
                        signOut();
                        setIsOpen(false);
                      }}
                      className="w-full flex items-center gap-2 px-3 py-2 text-red-400 hover:text-red-300 hover:bg-[#1a1a1a] rounded-lg transition-colors duration-200"
                    >
                      <LogOut className="w-4 h-4" />
                      Çıkış Yap
                    </button>
                  </>
                ) : (
                  <Link
                    href="/auth/signin"
                    className="flex items-center gap-2 px-3 py-2 text-blue-400 hover:text-blue-300 hover:bg-[#1a1a1a] rounded-lg transition-colors duration-200"
                    onClick={() => setIsOpen(false)}
                  >
                    <LogIn className="w-4 h-4" />
                    Giriş Yap
                  </Link>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
