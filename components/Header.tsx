'use client';

import Link from 'next/link';
import Image from 'next/image';
import { ShoppingCart, Menu, Search, User, Heart } from 'lucide-react';
import { useCart } from '@/contexts/CartContext';
import { Button } from '@/components/ui/button';
import { useState } from 'react';

export default function Header() {
  const { cartCount } = useCart();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/80">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center gap-8">
            <Link href="/" className="flex items-center space-x-3">
              <Image
                src="/logo.svg"
                alt="Alpha Medical Care Logo"
                width={40}
                height={48}
                className="h-12 w-auto"
              />
              <div className="hidden flex-col sm:flex">
                <span className="text-lg font-bold text-blue-600 leading-tight">ALPHA</span>
                <span className="text-[10px] font-light text-blue-600 tracking-widest">MEDICAL CARE</span>
              </div>
            </Link>

            <nav className="hidden lg:flex lg:gap-6">
              <Link
                href="/products"
                className="text-sm font-medium text-slate-700 transition-colors hover:text-blue-600"
              >
                All Products
              </Link>
              <Link
                href="/categories/pain-relief"
                className="text-sm font-medium text-slate-700 transition-colors hover:text-blue-600"
              >
                Pain Relief
              </Link>
              <Link
                href="/categories/rehabilitation"
                className="text-sm font-medium text-slate-700 transition-colors hover:text-blue-600"
              >
                Rehabilitation
              </Link>
              <Link
                href="/categories/wellness"
                className="text-sm font-medium text-slate-700 transition-colors hover:text-blue-600"
              >
                Wellness
              </Link>
              <Link
                href="/blog"
                className="text-sm font-medium text-slate-700 transition-colors hover:text-blue-600"
              >
                Blog
              </Link>
            </nav>
          </div>

          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" className="hidden md:inline-flex">
              <Search className="h-5 w-5" />
            </Button>

            <Link href="/account">
              <Button variant="ghost" size="icon">
                <User className="h-5 w-5" />
              </Button>
            </Link>

            <Button variant="ghost" size="icon" className="hidden md:inline-flex">
              <Heart className="h-5 w-5" />
            </Button>

            <Link href="/cart">
              <Button variant="ghost" size="icon" className="relative">
                <ShoppingCart className="h-5 w-5" />
                {cartCount > 0 && (
                  <span className="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-blue-600 text-xs font-bold text-white">
                    {cartCount}
                  </span>
                )}
              </Button>
            </Link>

            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              <Menu className="h-5 w-5" />
            </Button>
          </div>
        </div>

        {mobileMenuOpen && (
          <div className="border-t py-4 lg:hidden">
            <nav className="flex flex-col gap-4">
              <Link
                href="/products"
                className="text-sm font-medium text-slate-700 transition-colors hover:text-blue-600"
              >
                All Products
              </Link>
              <Link
                href="/categories/pain-relief"
                className="text-sm font-medium text-slate-700 transition-colors hover:text-blue-600"
              >
                Pain Relief
              </Link>
              <Link
                href="/categories/rehabilitation"
                className="text-sm font-medium text-slate-700 transition-colors hover:text-blue-600"
              >
                Rehabilitation
              </Link>
              <Link
                href="/categories/wellness"
                className="text-sm font-medium text-slate-700 transition-colors hover:text-blue-600"
              >
                Wellness
              </Link>
              <Link
                href="/blog"
                className="text-sm font-medium text-slate-700 transition-colors hover:text-blue-600"
              >
                Blog
              </Link>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
}
