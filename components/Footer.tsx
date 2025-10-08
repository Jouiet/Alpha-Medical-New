import Link from 'next/link';
import { Facebook, Instagram, Twitter, Mail, Phone, MapPin } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t bg-slate-50">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4">
          <div>
            <div className="mb-4 flex items-center space-x-2">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-teal-400">
                <span className="text-xl font-bold text-white">P</span>
              </div>
              <span className="text-lg font-semibold text-slate-900">PhysioWellness</span>
            </div>
            <p className="mb-4 text-sm text-slate-600">
              Your trusted partner for professional physiotherapy and wellness equipment. Quality products for recovery and well-being.
            </p>
            <div className="flex gap-4">
              <a href="#" className="text-slate-600 transition-colors hover:text-blue-600">
                <Facebook className="h-5 w-5" />
              </a>
              <a href="#" className="text-slate-600 transition-colors hover:text-blue-600">
                <Instagram className="h-5 w-5" />
              </a>
              <a href="#" className="text-slate-600 transition-colors hover:text-blue-600">
                <Twitter className="h-5 w-5" />
              </a>
            </div>
          </div>

          <div>
            <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-900">
              Shop
            </h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/products" className="text-slate-600 transition-colors hover:text-blue-600">
                  All Products
                </Link>
              </li>
              <li>
                <Link href="/categories/pain-relief" className="text-slate-600 transition-colors hover:text-blue-600">
                  Pain Relief
                </Link>
              </li>
              <li>
                <Link href="/categories/rehabilitation" className="text-slate-600 transition-colors hover:text-blue-600">
                  Rehabilitation
                </Link>
              </li>
              <li>
                <Link href="/categories/wellness" className="text-slate-600 transition-colors hover:text-blue-600">
                  Wellness & Beauty
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-900">
              Information
            </h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/about" className="text-slate-600 transition-colors hover:text-blue-600">
                  About Us
                </Link>
              </li>
              <li>
                <Link href="/blog" className="text-slate-600 transition-colors hover:text-blue-600">
                  Blog
                </Link>
              </li>
              <li>
                <Link href="/shipping" className="text-slate-600 transition-colors hover:text-blue-600">
                  Shipping & Returns
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="text-slate-600 transition-colors hover:text-blue-600">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="/terms" className="text-slate-600 transition-colors hover:text-blue-600">
                  Terms & Conditions
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-900">
              Contact Us
            </h3>
            <ul className="space-y-3 text-sm">
              <li className="flex items-start gap-2 text-slate-600">
                <Phone className="mt-0.5 h-4 w-4 flex-shrink-0" />
                <span>+1 (555) 123-4567</span>
              </li>
              <li className="flex items-start gap-2 text-slate-600">
                <Mail className="mt-0.5 h-4 w-4 flex-shrink-0" />
                <span>contact@physiowellness.com</span>
              </li>
              <li className="flex items-start gap-2 text-slate-600">
                <MapPin className="mt-0.5 h-4 w-4 flex-shrink-0" />
                <span>123 Health Street, Wellness City, WC 12345</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-8 border-t pt-8">
          <div className="flex flex-col items-center justify-between gap-4 md:flex-row">
            <p className="text-sm text-slate-600">
              © 2025 PhysioWellness. All rights reserved.
            </p>
            <div className="flex flex-wrap gap-4 text-sm text-slate-600">
              <img src="https://images.pexels.com/photos/164501/pexels-photo-164501.jpeg?auto=compress&cs=tinysrgb&w=100" alt="Secure Payment" className="h-6" />
              <span className="flex items-center gap-1">
                <span className="font-medium">SSL Secured</span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
