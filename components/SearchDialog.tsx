'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Search } from 'lucide-react';
import Link from 'next/link';

// All products data
const allProducts = [
  { id: 1, name: 'Medical Neck Traction Device', slug: 'medical-neck-traction-device', price: 89.99, category: 'pain-relief', image: 'https://images.pexels.com/photos/6823567/pexels-photo-6823567.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 2, name: 'Neck Traction Device Inflatable', slug: 'neck-traction-device-inflatable', price: 79.99, category: 'pain-relief', image: 'https://images.pexels.com/photos/6823567/pexels-photo-6823567.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 3, name: 'Posture Corrector Back Brace', slug: 'posture-corrector-back-brace', price: 49.99, category: 'pain-relief', image: 'https://images.pexels.com/photos/6823574/pexels-photo-6823574.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 4, name: 'Back Brace for Lower Back Pain', slug: 'back-brace-lower-back-pain', price: 59.99, category: 'pain-relief', image: 'https://images.pexels.com/photos/6823574/pexels-photo-6823574.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 5, name: 'Smart Cupping Massage Instrument', slug: 'smart-cupping-massage-instrument', price: 149.99, category: 'pain-relief', image: 'https://images.pexels.com/photos/5473184/pexels-photo-5473184.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 6, name: '5-in-1 Smart Cupping Therapy Set', slug: '5-in-1-smart-cupping-therapy-set', price: 199.99, category: 'pain-relief', image: 'https://images.pexels.com/photos/5473184/pexels-photo-5473184.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 7, name: 'Electric Foot and Hand Massager', slug: 'electric-foot-hand-massager', price: 129.99, category: 'pain-relief', image: 'https://images.pexels.com/photos/5473184/pexels-photo-5473184.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 8, name: 'Foot Air Pressure Leg Massage', slug: 'foot-air-pressure-leg-massage', price: 189.99, category: 'pain-relief', image: 'https://images.pexels.com/photos/5473184/pexels-photo-5473184.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 9, name: 'Air Pressure Leg Massage Recovery Boots', slug: 'air-pressure-leg-massage-recovery-boots', price: 299.99, category: 'pain-relief', image: 'https://images.pexels.com/photos/8172765/pexels-photo-8172765.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 10, name: 'Thermal Knee Massager', slug: 'thermal-knee-massager', price: 139.99, category: 'pain-relief', image: 'https://images.pexels.com/photos/6823581/pexels-photo-6823581.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 11, name: 'Relax Eye Massage Device', slug: 'relax-eye-massage-device', price: 89.99, category: 'pain-relief', image: 'https://images.pexels.com/photos/5473184/pexels-photo-5473184.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 12, name: 'Heated Rehabilitation Robot Gloves', slug: 'heated-rehabilitation-robot-gloves', price: 249.99, category: 'rehabilitation', image: 'https://images.pexels.com/photos/6823587/pexels-photo-6823587.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 13, name: 'Finger Rehabilitation Exerciser Robot Gloves', slug: 'finger-rehabilitation-exerciser-robot-gloves', price: 229.99, category: 'rehabilitation', image: 'https://images.pexels.com/photos/6823587/pexels-photo-6823587.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 14, name: 'Knee Brace Support for Arthritis Pain', slug: 'knee-brace-support-arthritis-pain', price: 69.99, category: 'rehabilitation', image: 'https://images.pexels.com/photos/6823581/pexels-photo-6823581.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 15, name: 'Achilles Tendon Rehabilitation Boots', slug: 'achilles-tendon-rehabilitation-boots', price: 159.99, category: 'rehabilitation', image: 'https://images.pexels.com/photos/6111619/pexels-photo-6111619.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 16, name: 'Adjust Knee Brace Orthopedic Leg Support', slug: 'adjust-knee-brace-orthopedic-leg-support', price: 119.99, category: 'rehabilitation', image: 'https://images.pexels.com/photos/6111619/pexels-photo-6111619.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 17, name: 'Knee Ankle Foot Orthosis for Hip Fracture', slug: 'knee-ankle-foot-orthosis-hip-fracture', price: 349.99, category: 'rehabilitation', image: 'https://images.pexels.com/photos/6111619/pexels-photo-6111619.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 18, name: 'LED Facial Mask with Neck Treatment', slug: 'led-facial-mask-neck-treatment', price: 199.99, category: 'wellness', image: 'https://images.pexels.com/photos/3865618/pexels-photo-3865618.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 19, name: 'Smart Facial Massager Lifting and Firming', slug: 'smart-facial-massager-lifting-firming', price: 149.99, category: 'wellness', image: 'https://images.pexels.com/photos/3865618/pexels-photo-3865618.jpeg?auto=compress&cs=tinysrgb&w=150' },
  { id: 20, name: '3 In 1 Facial Lifting Device', slug: '3-in-1-facial-lifting-device', price: 179.99, category: 'wellness', image: 'https://images.pexels.com/photos/3865618/pexels-photo-3865618.jpeg?auto=compress&cs=tinysrgb&w=150' },
];

interface SearchDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export default function SearchDialog({ open, onOpenChange }: SearchDialogProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState(allProducts.slice(0, 5));
  const router = useRouter();

  useEffect(() => {
    if (searchQuery.trim() === '') {
      setSearchResults(allProducts.slice(0, 5));
      return;
    }

    const query = searchQuery.toLowerCase();
    const filtered = allProducts.filter(
      (product) =>
        product.name.toLowerCase().includes(query) ||
        product.category.toLowerCase().includes(query)
    );
    setSearchResults(filtered.slice(0, 8));
  }, [searchQuery]);

  const handleProductClick = (slug: string) => {
    onOpenChange(false);
    setSearchQuery('');
    router.push(`/products/${slug}`);
  };

  const handleViewAll = () => {
    onOpenChange(false);
    setSearchQuery('');
    router.push(`/products?search=${encodeURIComponent(searchQuery)}`);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[80vh] p-0">
        <DialogHeader className="border-b p-6">
          <DialogTitle>Search Products</DialogTitle>
        </DialogHeader>

        <div className="p-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
            <Input
              type="text"
              placeholder="Search for products, categories..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 text-base"
              autoFocus
            />
          </div>

          <div className="mt-6">
            <div className="mb-3 flex items-center justify-between">
              <h3 className="text-sm font-semibold text-slate-700">
                {searchQuery ? `Found ${searchResults.length} products` : 'Popular Products'}
              </h3>
              {searchQuery && searchResults.length > 0 && (
                <button
                  onClick={handleViewAll}
                  className="text-sm text-blue-600 hover:text-blue-700"
                >
                  View all results
                </button>
              )}
            </div>

            {searchResults.length > 0 ? (
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {searchResults.map((product) => (
                  <button
                    key={product.id}
                    onClick={() => handleProductClick(product.slug)}
                    className="flex w-full items-center gap-4 rounded-lg p-3 text-left transition-colors hover:bg-slate-100"
                  >
                    <img
                      src={product.image}
                      alt={product.name}
                      className="h-14 w-14 rounded object-cover"
                    />
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-slate-900 line-clamp-1">
                        {product.name}
                      </p>
                      <p className="text-sm text-slate-600 capitalize">
                        {product.category.replace('-', ' ')}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold text-blue-600">
                        ${product.price.toFixed(2)}
                      </p>
                    </div>
                  </button>
                ))}
              </div>
            ) : (
              <div className="py-8 text-center">
                <p className="text-slate-600">No products found for "{searchQuery}"</p>
                <p className="mt-2 text-sm text-slate-500">
                  Try different keywords or browse our categories
                </p>
              </div>
            )}
          </div>

          <div className="mt-6 border-t pt-4">
            <p className="text-xs text-slate-500">
              Quick links:{' '}
              <Link
                href="/products"
                onClick={() => onOpenChange(false)}
                className="text-blue-600 hover:text-blue-700"
              >
                All Products
              </Link>
              {' · '}
              <Link
                href="/categories/pain-relief"
                onClick={() => onOpenChange(false)}
                className="text-blue-600 hover:text-blue-700"
              >
                Pain Relief
              </Link>
              {' · '}
              <Link
                href="/categories/rehabilitation"
                onClick={() => onOpenChange(false)}
                className="text-blue-600 hover:text-blue-700"
              >
                Rehabilitation
              </Link>
              {' · '}
              <Link
                href="/categories/wellness"
                onClick={() => onOpenChange(false)}
                className="text-blue-600 hover:text-blue-700"
              >
                Wellness
              </Link>
            </p>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
