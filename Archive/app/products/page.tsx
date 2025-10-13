'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Star, Search, SlidersHorizontal } from 'lucide-react';

export default function ProductsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [priceFilter, setPriceFilter] = useState('all');

  const products = [
    {
      id: 1,
      name: 'Medical Neck Traction Device',
      slug: 'medical-neck-traction-device',
      price: 89.99,
      category: 'Pain Relief',
      image: 'https://images.pexels.com/photos/6823567/pexels-photo-6823567.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.8,
      reviews: 234,
      inStock: true
    },
    {
      id: 2,
      name: 'Neck Traction Device Inflatable',
      slug: 'neck-traction-device-inflatable',
      price: 79.99,
      category: 'Pain Relief',
      image: 'https://images.pexels.com/photos/6823567/pexels-photo-6823567.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.7,
      reviews: 198,
      inStock: true
    },
    {
      id: 3,
      name: 'Posture Corrector Back Brace',
      slug: 'posture-corrector-back-brace',
      price: 49.99,
      category: 'Pain Relief',
      image: 'https://images.pexels.com/photos/6823574/pexels-photo-6823574.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.6,
      reviews: 342,
      inStock: true
    },
    {
      id: 4,
      name: 'Back Brace for Lower Back Pain',
      slug: 'back-brace-lower-back-pain',
      price: 59.99,
      category: 'Pain Relief',
      image: 'https://images.pexels.com/photos/6823574/pexels-photo-6823574.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.7,
      reviews: 289,
      inStock: true
    },
    {
      id: 5,
      name: 'Smart Cupping Massage Instrument',
      slug: 'smart-cupping-massage-instrument',
      price: 149.99,
      category: 'Pain Relief',
      image: 'https://images.pexels.com/photos/5473184/pexels-photo-5473184.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.9,
      reviews: 189,
      inStock: true
    },
    {
      id: 6,
      name: '5-in-1 Smart Cupping Therapy Set',
      slug: '5-in-1-smart-cupping-therapy-set',
      price: 199.99,
      category: 'Pain Relief',
      image: 'https://images.pexels.com/photos/5473184/pexels-photo-5473184.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.8,
      reviews: 156,
      inStock: true
    },
    {
      id: 7,
      name: 'Electric Foot and Hand Massager',
      slug: 'electric-foot-hand-massager',
      price: 129.99,
      category: 'Pain Relief',
      image: 'https://images.pexels.com/photos/3771110/pexels-photo-3771110.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.7,
      reviews: 223,
      inStock: true
    },
    {
      id: 8,
      name: 'Foot Air Pressure Leg Massage',
      slug: 'foot-air-pressure-leg-massage',
      price: 189.99,
      category: 'Pain Relief',
      image: 'https://images.pexels.com/photos/3771110/pexels-photo-3771110.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.8,
      reviews: 178,
      inStock: true
    },
    {
      id: 9,
      name: 'Air Pressure Leg Massage Recovery Boots',
      slug: 'air-pressure-leg-massage-recovery-boots',
      price: 299.99,
      category: 'Pain Relief',
      image: 'https://images.pexels.com/photos/8172765/pexels-photo-8172765.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.7,
      reviews: 156,
      inStock: true
    },
    {
      id: 10,
      name: 'Thermal Knee Massager',
      slug: 'thermal-knee-massager',
      price: 139.99,
      category: 'Pain Relief',
      image: 'https://images.pexels.com/photos/6823581/pexels-photo-6823581.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.6,
      reviews: 201,
      inStock: true
    },
    {
      id: 11,
      name: 'Heated Rehabilitation Robot Gloves',
      slug: 'heated-rehabilitation-robot-gloves',
      price: 249.99,
      category: 'Rehabilitation',
      image: 'https://images.pexels.com/photos/6823587/pexels-photo-6823587.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.8,
      reviews: 134,
      inStock: true
    },
    {
      id: 12,
      name: 'Relax Eye Massage Device',
      slug: 'relax-eye-massage-device',
      price: 89.99,
      category: 'Pain Relief',
      image: 'https://images.pexels.com/photos/3757952/pexels-photo-3757952.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.7,
      reviews: 267,
      inStock: true
    },
    {
      id: 13,
      name: 'Finger Rehabilitation Exerciser Robot Gloves',
      slug: 'finger-rehabilitation-exerciser-robot-gloves',
      price: 229.99,
      category: 'Rehabilitation',
      image: 'https://images.pexels.com/photos/6823587/pexels-photo-6823587.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.9,
      reviews: 112,
      inStock: true
    },
    {
      id: 14,
      name: 'Knee Brace Support for Arthritis Pain',
      slug: 'knee-brace-support-arthritis-pain',
      price: 69.99,
      category: 'Rehabilitation',
      image: 'https://images.pexels.com/photos/6823581/pexels-photo-6823581.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.6,
      reviews: 298,
      inStock: true
    },
    {
      id: 15,
      name: 'Achilles Tendon Rehabilitation Boots',
      slug: 'achilles-tendon-rehabilitation-boots',
      price: 159.99,
      category: 'Rehabilitation',
      image: 'https://images.pexels.com/photos/6111619/pexels-photo-6111619.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.7,
      reviews: 145,
      inStock: true
    },
    {
      id: 16,
      name: 'Adjust Knee Brace Orthopedic Leg Support',
      slug: 'adjust-knee-brace-orthopedic-leg-support',
      price: 119.99,
      category: 'Rehabilitation',
      image: 'https://images.pexels.com/photos/6111619/pexels-photo-6111619.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.8,
      reviews: 187,
      inStock: true
    },
    {
      id: 17,
      name: 'Knee Ankle Foot Orthosis for Hip Fracture',
      slug: 'knee-ankle-foot-orthosis-hip-fracture',
      price: 349.99,
      category: 'Rehabilitation',
      image: 'https://images.pexels.com/photos/6111619/pexels-photo-6111619.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.9,
      reviews: 98,
      inStock: true
    },
    {
      id: 18,
      name: 'LED Facial Mask with Neck Treatment',
      slug: 'led-facial-mask-neck-treatment',
      price: 199.99,
      category: 'Wellness',
      image: 'https://images.pexels.com/photos/3865618/pexels-photo-3865618.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.6,
      reviews: 203,
      inStock: true
    },
    {
      id: 19,
      name: 'Smart Facial Massager Lifting and Firming',
      slug: 'smart-facial-massager-lifting-firming',
      price: 149.99,
      category: 'Wellness',
      image: 'https://images.pexels.com/photos/3865618/pexels-photo-3865618.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.7,
      reviews: 176,
      inStock: true
    },
    {
      id: 20,
      name: '3 In 1 Facial Lifting Device',
      slug: '3-in-1-facial-lifting-device',
      price: 179.99,
      category: 'Wellness',
      image: 'https://images.pexels.com/photos/3757952/pexels-photo-3757952.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.8,
      reviews: 192,
      inStock: true
    }
  ];

  const filteredProducts = products.filter((product) => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = categoryFilter === 'all' || product.category === categoryFilter;
    const matchesPrice =
      priceFilter === 'all' ||
      (priceFilter === 'under50' && product.price < 50) ||
      (priceFilter === '50-100' && product.price >= 50 && product.price < 100) ||
      (priceFilter === '100-200' && product.price >= 100 && product.price < 200) ||
      (priceFilter === 'over200' && product.price >= 200);

    return matchesSearch && matchesCategory && matchesPrice;
  });

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="mb-4 text-4xl font-bold text-slate-900">All Products</h1>
        <p className="text-lg text-slate-600">
          Browse our complete collection of professional physiotherapy and wellness equipment
        </p>
      </div>

      <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div className="relative flex-1 md:max-w-md">
          <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
          <Input
            type="text"
            placeholder="Search products..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>

        <div className="flex flex-wrap gap-4">
          <Select value={categoryFilter} onValueChange={setCategoryFilter}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Category" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Categories</SelectItem>
              <SelectItem value="Pain Relief">Pain Relief</SelectItem>
              <SelectItem value="Rehabilitation">Rehabilitation</SelectItem>
              <SelectItem value="Wellness">Wellness</SelectItem>
            </SelectContent>
          </Select>

          <Select value={priceFilter} onValueChange={setPriceFilter}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Price Range" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Prices</SelectItem>
              <SelectItem value="under50">Under $50</SelectItem>
              <SelectItem value="50-100">$50 - $100</SelectItem>
              <SelectItem value="100-200">$100 - $200</SelectItem>
              <SelectItem value="over200">Over $200</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="mb-4 text-sm text-slate-600">
        Showing {filteredProducts.length} of {products.length} products
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {filteredProducts.map((product) => (
          <Link key={product.id} href={`/products/${product.slug}`}>
            <Card className="group h-full overflow-hidden transition-all hover:shadow-lg">
              <div className="relative aspect-square overflow-hidden">
                <img
                  src={product.image}
                  alt={product.name}
                  className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
                />
                {product.inStock ? (
                  <Badge className="absolute right-3 top-3 bg-green-600">In Stock</Badge>
                ) : (
                  <Badge className="absolute right-3 top-3 bg-red-600">Out of Stock</Badge>
                )}
              </div>
              <CardContent className="p-4">
                <Badge variant="outline" className="mb-2">
                  {product.category}
                </Badge>
                <h3 className="mb-2 font-semibold text-slate-900 line-clamp-2">
                  {product.name}
                </h3>
                <div className="mb-3 flex items-center gap-1">
                  <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                  <span className="text-sm font-medium text-slate-900">{product.rating}</span>
                  <span className="text-sm text-slate-500">({product.reviews})</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xl font-bold text-blue-600">${product.price}</span>
                  <Button size="sm" variant="outline">
                    View Details
                  </Button>
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>

      {filteredProducts.length === 0 && (
        <div className="py-16 text-center">
          <p className="text-lg text-slate-600">No products found matching your criteria.</p>
          <Button
            variant="outline"
            className="mt-4"
            onClick={() => {
              setSearchQuery('');
              setCategoryFilter('all');
              setPriceFilter('all');
            }}
          >
            Clear Filters
          </Button>
        </div>
      )}
    </div>
  );
}
