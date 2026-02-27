import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "MİZAN-AI | Türk Siyasi Belge Analiz Platformu",
  description: "Yapay zeka destekli siyasi belge analiz platformu. 8 siyasi partinin tüzük ve programlarını sorgulayın.",
  keywords: ["siyaset", "yapay zeka", "RAG", "türkiye", "parti"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="tr">
      <body className={`${inter.className} antialiased bg-[#0a0a0a] text-white`}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
