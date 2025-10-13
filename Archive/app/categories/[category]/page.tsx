'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Star, Search } from 'lucide-react';

export default function CategoryPage() {
  const params = useParams();
  const category = params.category as string;
  const [searchQuery, setSearchQuery] = useState('');
  const [priceFilter, setPriceFilter] = useState('all');

  const categoryData: Record<string, { title: string; description: string }> = {
    'pain-relief': {
      title: 'Pain Relief & Relaxation',
      description: 'Professional devices for cervical care, back support, massage therapy, and thermal treatment',
    },
    'rehabilitation': {
      title: 'Rehabilitation & Mobility',
      description: 'Medical-grade equipment for upper and lower limb recovery and mobility support',
    },
    'wellness': {
      title: 'Wellness & Beauty',
      description: 'Advanced facial care devices and beauty technology for skin health',
    },
  };

  const products = [
    {
      id: 1,
      name: 'Medical Neck Traction Device',
      slug: 'medical-neck-traction-device',
      price: 89.99,
      category: 'pain-relief',
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
      category: 'pain-relief',
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
      category: 'pain-relief',
      image: 'https://images.pexels.com/photos/6823574/pexels-photo-6823574.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.6,
      reviews: 342,
      inStock: true
    },
    {
      id: 4,
      name: 'Smart Cupping Massage Instrument',
      slug: 'smart-cupping-massage-instrument',
      price: 149.99,
      category: 'pain-relief',
      image: 'https://images.pexels.com/photos/5473184/pexels-photo-5473184.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.9,
      reviews: 189,
      inStock: true
    },
    {
      id: 5,
      name: 'Air Pressure Leg Massage Recovery Boots',
      slug: 'air-pressure-leg-massage-recovery-boots',
      price: 299.99,
      category: 'pain-relief',
      image: 'https://images.pexels.com/photos/8172765/pexels-photo-8172765.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.7,
      reviews: 156,
      inStock: true
    },
    {
      id: 6,
      name: 'Thermal Knee Massager',
      slug: 'thermal-knee-massager',
      price: 139.99,
      category: 'pain-relief',
      image: 'https://images.pexels.com/photos/6823581/pexels-photo-6823581.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.6,
      reviews: 201,
      inStock: true
    },
    {
      id: 7,
      name: 'Heated Rehabilitation Robot Gloves',
      slug: 'heated-rehabilitation-robot-gloves',
      price: 249.99,
      category: 'rehabilitation',
      image: 'https://images.pexels.com/photos/6823587/pexels-photo-6823587.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.8,
      reviews: 134,
      inStock: true
    },
    {
      id: 8,
      name: 'Finger Rehabilitation Exerciser Robot Gloves',
      slug: 'finger-rehabilitation-exerciser-robot-gloves',
      price: 229.99,
      category: 'rehabilitation',
      image: 'https://images.pexels.com/photos/6823587/pexels-photo-6823587.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.9,
      reviews: 112,
      inStock: true
    },
    {
      id: 9,
      name: 'Knee Brace Support for Arthritis Pain',
      slug: 'knee-brace-support-arthritis-pain',
      price: 69.99,
      category: 'rehabilitation',
      image: 'https://images.pexels.com/photos/6823581/pexels-photo-6823581.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.6,
      reviews: 298,
      inStock: true
    },
    {
      id: 10,
      name: 'Achilles Tendon Rehabilitation Boots',
      slug: 'achilles-tendon-rehabilitation-boots',
      price: 159.99,
      category: 'rehabilitation',
      image: 'https://images.pexels.com/photos/6111619/pexels-photo-6111619.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.7,
      reviews: 145,
      inStock: true
    },
    {
      id: 11,
      name: 'LED Facial Mask with Neck Treatment',
      slug: 'led-facial-mask-neck-treatment',
      price: 199.99,
      category: 'wellness',
      image: 'https://images.pexels.com/photos/3865618/pexels-photo-3865618.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.6,
      reviews: 203,
      inStock: true
    },
    {
      id: 12,
      name: 'Smart Facial Massager Lifting and Firming',
      slug: 'smart-facial-massager-lifting-firming',
      price: 149.99,
      category: 'wellness',
      image: 'https://images.pexels.com/photos/3865618/pexels-photo-3865618.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.7,
      reviews: 176,
      inStock: true
    },
  ];

  const currentCategory = categoryData[category];

  if (!currentCategory) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <h1 className="text-3xl font-bold">Category not found</h1>
        <Link href="/products">
          <Button className="mt-4">View All Products</Button>
        </Link>
      </div>
    );
  }

  const filteredProducts = products
    .filter((product) => product.category === category)
    .filter((product) => product.name.toLowerCase().includes(searchQuery.toLowerCase()))
    .filter((product) => {
      if (priceFilter === 'all') return true;
      if (priceFilter === 'under50') return product.price < 50;
      if (priceFilter === '50-100') return product.price >= 50 && product.price < 100;
      if (priceFilter === '100-200') return product.price >= 100 && product.price < 200;
      if (priceFilter === 'over200') return product.price >= 200;
      return true;
    });

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="mb-4 text-4xl font-bold text-slate-900">{currentCategory.title}</h1>
        <p className="text-lg text-slate-600">{currentCategory.description}</p>
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

      <div className="mb-4 text-sm text-slate-600">
        Showing {filteredProducts.length} products
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
          <Button variant="outline" className="mt-4" onClick={() => { setSearchQuery(''); setPriceFilter('all'); }}>
            Clear Filters
          </Button>
        </div>
      )}
    </div>
  );
}
