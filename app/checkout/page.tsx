'use client';

import { useState } from 'react';
import { useCart } from '@/contexts/CartContext';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { CreditCard, Lock, Package } from 'lucide-react';
import { toast } from 'sonner';
import { useRouter } from 'next/navigation';
import dynamic from 'next/dynamic';

const StripeCheckout = dynamic(() => import('@/components/StripeCheckout'), {
  ssr: false,
});

export default function CheckoutPage() {
  const { cart, cartTotal, clearCart } = useCart();
  const router = useRouter();
  const [processing, setProcessing] = useState(false);
  const [activeStep, setActiveStep] = useState<'info' | 'payment'>('info');

  const [formData, setFormData] = useState({
    email: '',
    firstName: '',
    lastName: '',
    address: '',
    city: '',
    state: '',
    zipCode: '',
    phone: ''
  });

  const handleInfoSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Validate form data
    if (!formData.email || !formData.firstName || !formData.lastName || !formData.address || !formData.city || !formData.state || !formData.zipCode || !formData.phone) {
      toast.error('Please fill in all required fields');
      return;
    }
    setActiveStep('payment');
  };

  const handlePaymentSuccess = () => {
    toast.success('Payment successful! Your order has been placed.');
    clearCart();
    router.push('/account/orders');
  };

  const handlePaymentError = (error: string) => {
    toast.error(`Payment failed: ${error}`);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const shippingCost = cartTotal >= 100 ? 0 : 9.99;
  const tax = cartTotal * 0.1;
  const total = cartTotal + shippingCost + tax;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="mb-8 text-3xl font-bold text-slate-900">Checkout</h1>

      <div className="grid gap-8 lg:grid-cols-3">
        <div className="lg:col-span-2">
          {activeStep === 'info' ? (
            <form onSubmit={handleInfoSubmit}>
              <div className="mb-6 flex items-center gap-2">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-600 text-white font-medium">
                  1
                </div>
                <span className="font-medium text-slate-900">Shipping Information</span>
                <div className="ml-4 flex h-8 w-8 items-center justify-center rounded-full bg-slate-200 text-slate-600 font-medium">
                  2
                </div>
                <span className="text-slate-600">Payment</span>
              </div>

              <Card className="mb-6">
                <CardHeader>
                  <CardTitle>Contact Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      name="email"
                      type="email"
                      required
                      value={formData.email}
                      onChange={handleChange}
                      placeholder="your@email.com"
                    />
                  </div>
                </CardContent>
              </Card>

              <Card className="mb-6">
                <CardHeader>
                  <CardTitle>Shipping Address</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <Label htmlFor="firstName">First Name</Label>
                      <Input
                        id="firstName"
                        name="firstName"
                        required
                        value={formData.firstName}
                        onChange={handleChange}
                      />
                    </div>
                    <div>
                      <Label htmlFor="lastName">Last Name</Label>
                      <Input
                        id="lastName"
                        name="lastName"
                        required
                        value={formData.lastName}
                        onChange={handleChange}
                      />
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="address">Address</Label>
                    <Input
                      id="address"
                      name="address"
                      required
                      value={formData.address}
                      onChange={handleChange}
                      placeholder="Street address"
                    />
                  </div>

                  <div className="grid gap-4 md:grid-cols-3">
                    <div>
                      <Label htmlFor="city">City</Label>
                      <Input
                        id="city"
                        name="city"
                        required
                        value={formData.city}
                        onChange={handleChange}
                      />
                    </div>
                    <div>
                      <Label htmlFor="state">State</Label>
                      <Input
                        id="state"
                        name="state"
                        required
                        value={formData.state}
                        onChange={handleChange}
                      />
                    </div>
                    <div>
                      <Label htmlFor="zipCode">ZIP Code</Label>
                      <Input
                        id="zipCode"
                        name="zipCode"
                        required
                        value={formData.zipCode}
                        onChange={handleChange}
                      />
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="phone">Phone Number</Label>
                    <Input
                      id="phone"
                      name="phone"
                      type="tel"
                      required
                      value={formData.phone}
                      onChange={handleChange}
                      placeholder="(555) 123-4567"
                    />
                  </div>

                  <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700" size="lg">
                    Continue to Payment
                  </Button>
                </CardContent>
              </Card>
            </form>
          ) : (
            <div>
              <div className="mb-6 flex items-center gap-2">
                <button
                  onClick={() => setActiveStep('info')}
                  className="flex h-8 w-8 items-center justify-center rounded-full bg-green-600 text-white font-medium"
                >
                  ✓
                </button>
                <button onClick={() => setActiveStep('info')} className="font-medium text-blue-600 hover:underline">
                  Shipping Information
                </button>
                <div className="ml-4 flex h-8 w-8 items-center justify-center rounded-full bg-blue-600 text-white font-medium">
                  2
                </div>
                <span className="font-medium text-slate-900">Payment</span>
              </div>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <CreditCard className="h-5 w-5" />
                    Payment Information
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="mb-6 rounded-lg bg-blue-50 p-4 text-sm text-blue-800">
                    <Lock className="mb-2 h-5 w-5" />
                    <p className="font-medium">Secure Payment Processing</p>
                    <p className="mt-1 text-blue-700">
                      Your payment information is encrypted and secure with Stripe.
                    </p>
                  </div>

                  <StripeCheckout
                    amount={total}
                    metadata={{
                      customerName: `${formData.firstName} ${formData.lastName}`,
                      customerEmail: formData.email,
                      shippingAddress: `${formData.address}, ${formData.city}, ${formData.state} ${formData.zipCode}`,
                      items: cart.map(item => `${item.name} x${item.quantity}`).join(', '),
                    }}
                    onSuccess={handlePaymentSuccess}
                    onError={handlePaymentError}
                  />
                </CardContent>
              </Card>
            </div>
          )}
        </div>

        <div className="lg:col-span-1">
          <Card className="sticky top-20">
            <CardHeader>
              <CardTitle>Order Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="mb-4 space-y-3">
                {cart.map((item) => (
                  <div key={item.id} className="flex gap-3">
                    <div className="relative h-16 w-16 flex-shrink-0 overflow-hidden rounded-lg">
                      <img src={item.image} alt={item.name} className="h-full w-full object-cover" />
                    </div>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-slate-900 line-clamp-1">{item.name}</p>
                      <p className="text-sm text-slate-600">Qty: {item.quantity}</p>
                      <p className="text-sm font-bold text-slate-900">
                        ${(item.price * item.quantity).toFixed(2)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              <Separator className="my-4" />

              <div className="space-y-2 text-sm">
                <div className="flex justify-between text-slate-600">
                  <span>Subtotal</span>
                  <span>${cartTotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-slate-600">
                  <span>Shipping</span>
                  <span>{shippingCost === 0 ? 'FREE' : `$${shippingCost.toFixed(2)}`}</span>
                </div>
                <div className="flex justify-between text-slate-600">
                  <span>Tax</span>
                  <span>${tax.toFixed(2)}</span>
                </div>

                <Separator className="my-2" />

                <div className="flex justify-between text-lg font-bold text-slate-900">
                  <span>Total</span>
                  <span>${total.toFixed(2)}</span>
                </div>
              </div>

              <p className="mt-4 text-center text-xs text-slate-500">
                By placing your order, you agree to our Terms & Conditions
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
