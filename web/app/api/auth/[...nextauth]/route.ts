import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";

const handler = NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID || "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
    }),
    CredentialsProvider({
      name: "Email",
      credentials: {
        email: { label: "Email", type: "email", placeholder: "ornek@email.com" },
        password: { label: "Şifre", type: "password" },
      },
      async authorize(credentials) {
        // Demo için basit doğrulama - gerçek uygulamada veritabanı kontrolü yapılmalı
        if (!credentials?.email || !credentials?.password) {
          return null;
        }

        // localStorage'da kullanıcı kayıtları tutulacak (demo amaçlı)
        // Gerçek uygulamada bu veritabanı ile yapılmalı

        // Demo kullanıcı
        if (credentials.email && credentials.password.length >= 6) {
          return {
            id: credentials.email,
            email: credentials.email,
            name: credentials.email.split("@")[0],
          };
        }

        return null;
      },
    }),
  ],
  pages: {
    signIn: "/auth/signin",
  },
  session: {
    strategy: "jwt",
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
      }
      return session;
    },
  },
});

export { handler as GET, handler as POST };
