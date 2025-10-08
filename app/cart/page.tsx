'use client';

import { useCart } from '@/contexts/CartContext';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Separator } from '@/components/ui/separator';
import { Minus, Plus, X, ShoppingBag } from 'lucide-react';
import Link from 'next/link';
import { toast } from 'sonner';

export default function CartPage() {
  const { cart, removeFromCart, updateQuantity, cartTotal, cartCount } = useCart();

  const handleCheckout = () => {
    toast.success('Redirecting to checkout...');
  };

  if (cart.length === 0) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="mx-auto max-w-md text-center">
          <ShoppingBag className="mx-auto mb-4 h-16 w-16 text-slate-300" />
          <h2 className="mb-2 text-2xl font-bold text-slate-900">Your cart is empty</h2>
          <p className="mb-6 text-slate-600">
            Looks like you haven&apos;t added any products to your cart yet.
          </p>
          <Button asChild>
            <Link href="/products">Continue Shopping</Link>
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="mb-8 text-3xl font-bold text-slate-900">Shopping Cart</h1>

      <div className="grid gap-8 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <Card>
            <CardContent className="p-6">
              <div className="mb-4 flex items-center justify-between">
                <h2 className="text-xl font-semibold text-slate-900">
                  Cart Items ({cartCount})
                </h2>
              </div>

              <div className="space-y-4">
                {cart.map((item) => (
                  <div key={item.id} className="flex gap-4 border-b pb-4 last:border-b-0">
                    <div className="relative h-24 w-24 flex-shrink-0 overflow-hidden rounded-lg">
                      <img
                        src={item.image}
                        alt={item.name}
                        className="h-full w-full object-cover"
                      />
                    </div>

                    <div className="flex flex-1 flex-col">
                      <div className="flex justify-between">
                        <h3 className="font-semibold text-slate-900">{item.name}</h3>
                        <button
                          onClick={() => {
                            removeFromCart(item.id);
                            toast.success('Item removed from cart');
                          }}
                          className="text-slate-400 transition-colors hover:text-red-600"
                        >
                          <X className="h-5 w-5" />
                        </button>
                      </div>

                      <p className="mt-1 text-lg font-bold text-blue-600">
                        ${item.price.toFixed(2)}
                      </p>

                      <div className="mt-auto flex items-center gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => updateQuantity(item.id, item.quantity - 1)}
                          disabled={item.quantity <= 1}
                        >
                          <Minus className="h-4 w-4" />
                        </Button>
                        <span className="w-12 text-center font-medium">{item.quantity}</span>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => updateQuantity(item.id, item.quantity + 1)}
                        >
                          <Plus className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>

                    <div className="flex flex-col items-end justify-between">
                      <p className="font-bold text-slate-900">
                        ${(item.price * item.quantity).toFixed(2)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-1">
          <Card className="sticky top-20">
            <CardContent className="p-6">
              <h2 className="mb-4 text-xl font-semibold text-slate-900">Order Summary</h2>

              <div className="space-y-3">
                <div className="flex justify-between text-slate-600">
                  <span>Subtotal</span>
                  <span>${cartTotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-slate-600">
                  <span>Shipping</span>
                  <span>{cartTotal >= 100 ? 'FREE' : '$9.99'}</span>
                </div>
                <div className="flex justify-between text-slate-600">
                  <span>Tax</span>
                  <span>${(cartTotal * 0.1).toFixed(2)}</span>
                </div>

                <Separator />

                <div className="flex justify-between text-lg font-bold text-slate-900">
                  <span>Total</span>
                  <span>
                    ${(cartTotal + (cartTotal >= 100 ? 0 : 9.99) + cartTotal * 0.1).toFixed(2)}
                  </span>
                </div>
              </div>

              <Button className="mt-6 w-full bg-blue-600 hover:bg-blue-700" size="lg" asChild>
                <Link href="/checkout">Proceed to Checkout</Link>
              </Button>

              <Button variant="outline" className="mt-3 w-full" asChild>
                <Link href="/products">Continue Shopping</Link>
              </Button>

              {cartTotal >= 100 && (
                <div className="mt-4 rounded-lg bg-green-50 p-3 text-center text-sm text-green-700">
                  You qualify for free shipping!
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
