import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import NavBar from './components/NavBar';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'FPL‑Oracle Dashboard',
  description: 'Advanced FPL analytics and insights',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/pl.jpg" type="image/x-icon" />
      </head>
      <body className={`${inter.className} bg-gradient-to-br from-blue-50 via-slate-50 to-cyan-50 min-h-screen`}>
        <NavBar />
        <main className="pt-24 px-8 pb-16">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </body>
    </html>
  );
}
