'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import Image from 'next/image';
import chelsea from '../../../public/chelsea.svg'

interface NavItem {
  label: string;
  href: string;
}

const NAV_ITEMS: NavItem[] = [
  { label: 'Dashboard', href: '/' },
  { label: 'Table', href: '/table' },
  { label: 'Fixture', href: '/fixture' },
  { label: 'Team', href: '/team' },
  { label: 'Search', href: '/search' },
];

export default function NavBar() {
  const pathname = usePathname();

  const isActive = (href: string): boolean => {
    if (href === '/') {
      return pathname === '/';
    }
    return pathname.startsWith(href);
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-2xl bg-white/90 border-b border-blue-200/30 shadow-xl">
      <div className="max-w-7xl mx-auto px-8 py-5">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-600 to-cyan-500 shadow-lg flex items-center justify-center">
              <Image
                src={chelsea}
                alt='Logo'
              />
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-blue-700 to-cyan-600 bg-clip-text text-transparent">
              FPL‑Oracle
            </span>
          </div>

          {/* Navigation Links */}
          <div className="flex gap-3">
            {NAV_ITEMS.map((item) => {
              const active = isActive(item.href);
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`px-6 py-2.5 rounded-2xl font-semibold transition-all duration-300 ease-out ${active
                    ? 'bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow-lg hover:shadow-xl'
                    : 'text-gray-700 hover:bg-blue-50/80 hover:text-blue-700'
                    }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
}
