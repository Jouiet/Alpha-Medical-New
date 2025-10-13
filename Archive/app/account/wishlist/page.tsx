'use client';

import Link from 'next/link';
import { ArrowLeft, Heart, ShoppingCart, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { useWishlist } from '@/contexts/WishlistContext';
import { useCart } from '@/contexts/CartContext';
import { toast } from 'sonner';

export default function WishlistPage() {
  const { wishlist, removeFromWishlist } = useWishlist();
  const { addToCart } = useCart();

  const handleAddToCart = (item: any) => {
    addToCart({
      id: item.id,
      name: item.name,
      price: item.price,
      quantity: 1,
      image: item.image,
    });
    toast.success(`${item.name} added to cart!`);
  };

  const handleRemove = (id: number, name: string) => {
    removeFromWishlist(id);
    toast.success(`${name} removed from wishlist`);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <Link href="/account" className="inline-flex items-center text-blue-600 hover:text-blue-700">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Account
        </Link>
      </div>

      <div className="mb-8">
        <h1 className="mb-2 text-3xl font-bold text-slate-900">My Wishlist</h1>
        <p className="text-slate-600">
          {wishlist.length} {wishlist.length === 1 ? 'item' : 'items'} saved
        </p>
      </div>

      {wishlist.length > 0 ? (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {wishlist.map((item) => (
            <Card key={item.id} className="group relative overflow-hidden">
              <button
                onClick={() => handleRemove(item.id, item.name)}
                className="absolute right-2 top-2 z-10 rounded-full bg-white p-2 shadow-md transition-colors hover:bg-red-50"
              >
                <X className="h-4 w-4 text-red-600" />
              </button>

              <Link href={`/products/${item.slug}`}>
                <div className="relative aspect-square overflow-hidden">
                  <img
                    src={item.image}
                    alt={item.name}
                    className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
                  />
                </div>
              </Link>

              <CardContent className="p-4">
                <Link href={`/products/${item.slug}`}>
                  <h3 className="mb-2 font-semibold text-slate-900 line-clamp-2 hover:text-blue-600">
                    {item.name}
                  </h3>
                </Link>

                <div className="mb-4">
                  <span className="text-xl font-bold text-blue-600">
                    ${item.price.toFixed(2)}
                  </span>
                </div>

                <div className="flex gap-2">
                  <Button
                    onClick={() => handleAddToCart(item)}
                    className="flex-1"
                    size="sm"
                  >
                    <ShoppingCart className="mr-2 h-4 w-4" />
                    Add to Cart
                  </Button>
                  <Link href={`/products/${item.slug}`} className="flex-1">
                    <Button variant="outline" size="sm" className="w-full">
                      View
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <div className="py-16 text-center">
          <Heart className="mx-auto h-24 w-24 text-slate-300" />
          <h2 className="mt-6 text-2xl font-semibold text-slate-900">
            Your wishlist is empty
          </h2>
          <p className="mt-2 text-slate-600">
            Save items you love by clicking the heart icon on product pages
          </p>
          <Link href="/products">
            <Button className="mt-6">
              Browse Products
            </Button>
          </Link>
        </div>
      )}

      {wishlist.length > 0 && (
        <div className="mt-8 text-center">
          <Link href="/products">
            <Button variant="outline">
              Continue Shopping
            </Button>
          </Link>
        </div>
      )}
    </div>
  );
}
