'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, Plus, CreditCard, Trash2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';

interface PaymentMethod {
  id: number;
  type: 'card' | 'paypal';
  last4?: string;
  brand?: string;
  expiryMonth?: number;
  expiryYear?: number;
  email?: string;
  isDefault: boolean;
}

export default function PaymentPage() {
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([
    {
      id: 1,
      type: 'card',
      last4: '4242',
      brand: 'Visa',
      expiryMonth: 12,
      expiryYear: 2026,
      isDefault: true,
    },
    {
      id: 2,
      type: 'card',
      last4: '5555',
      brand: 'Mastercard',
      expiryMonth: 8,
      expiryYear: 2027,
      isDefault: false,
    },
  ]);

  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const handleSetDefault = (id: number) => {
    setPaymentMethods(
      paymentMethods.map((method) => ({
        ...method,
        isDefault: method.id === id,
      }))
    );
    toast.success('Default payment method updated');
  };

  const handleDelete = (id: number) => {
    if (paymentMethods.find((m) => m.id === id)?.isDefault) {
      toast.error('Cannot delete default payment method');
      return;
    }
    setPaymentMethods(paymentMethods.filter((method) => method.id !== id));
    toast.success('Payment method removed');
  };

  const getCardBrandLogo = (brand: string) => {
    const logos: Record<string, string> = {
      Visa: '💳',
      Mastercard: '💳',
      'American Express': '💳',
      Discover: '💳',
    };
    return logos[brand] || '💳';
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <Link href="/account" className="inline-flex items-center text-blue-600 hover:text-blue-700">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Account
        </Link>
      </div>

      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="mb-2 text-3xl font-bold text-slate-900">Payment Methods</h1>
          <p className="text-slate-600">Manage your saved payment methods</p>
        </div>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Add Payment Method
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle>Add Payment Method</DialogTitle>
            </DialogHeader>
            <form className="space-y-4">
              <div>
                <Label htmlFor="cardNumber">Card Number</Label>
                <Input
                  id="cardNumber"
                  placeholder="1234 5678 9012 3456"
                  maxLength={19}
                />
              </div>

              <div>
                <Label htmlFor="cardName">Cardholder Name</Label>
                <Input id="cardName" placeholder="John Doe" />
              </div>

              <div className="grid gap-4 grid-cols-2">
                <div>
                  <Label htmlFor="expiry">Expiry Date</Label>
                  <Input id="expiry" placeholder="MM/YY" maxLength={5} />
                </div>
                <div>
                  <Label htmlFor="cvv">CVV</Label>
                  <Input
                    id="cvv"
                    type="password"
                    placeholder="123"
                    maxLength={4}
                  />
                </div>
              </div>

              <div className="flex gap-2">
                <Button type="submit" className="flex-1">
                  Add Card
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setIsDialogOpen(false)}
                >
                  Cancel
                </Button>
              </div>
            </form>

            <div className="border-t pt-4 mt-4">
              <p className="text-xs text-slate-600 text-center">
                🔒 Your payment information is encrypted and secure
              </p>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {paymentMethods.length > 0 ? (
        <div className="space-y-4">
          {paymentMethods.map((method) => (
            <Card key={method.id}>
              <CardContent className="flex items-center justify-between p-6">
                <div className="flex items-center gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-full bg-slate-100 text-2xl">
                    {method.type === 'card' ? getCardBrandLogo(method.brand!) : '📧'}
                  </div>
                  <div>
                    {method.type === 'card' ? (
                      <>
                        <div className="flex items-center gap-2">
                          <p className="font-semibold text-slate-900">
                            {method.brand} •••• {method.last4}
                          </p>
                          {method.isDefault && (
                            <Badge variant="default" className="bg-green-600">
                              Default
                            </Badge>
                          )}
                        </div>
                        <p className="text-sm text-slate-600">
                          Expires {method.expiryMonth}/{method.expiryYear}
                        </p>
                      </>
                    ) : (
                      <>
                        <div className="flex items-center gap-2">
                          <p className="font-semibold text-slate-900">PayPal</p>
                          {method.isDefault && (
                            <Badge variant="default" className="bg-green-600">
                              Default
                            </Badge>
                          )}
                        </div>
                        <p className="text-sm text-slate-600">{method.email}</p>
                      </>
                    )}
                  </div>
                </div>

                <div className="flex gap-2">
                  {!method.isDefault && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleSetDefault(method.id)}
                    >
                      Set Default
                    </Button>
                  )}
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDelete(method.id)}
                    disabled={method.isDefault}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <div className="py-16 text-center">
          <CreditCard className="mx-auto h-24 w-24 text-slate-300" />
          <h2 className="mt-6 text-2xl font-semibold text-slate-900">
            No payment methods saved
          </h2>
          <p className="mt-2 text-slate-600">
            Add a payment method for faster checkout
          </p>
          <Button className="mt-6" onClick={() => setIsDialogOpen(true)}>
            <Plus className="mr-2 h-4 w-4" />
            Add Payment Method
          </Button>
        </div>
      )}

      <Card className="mt-8">
        <CardContent className="p-6">
          <h3 className="mb-4 font-semibold text-slate-900">Security Information</h3>
          <div className="space-y-3 text-sm text-slate-600">
            <p>
              🔒 All payment information is encrypted using industry-standard SSL technology
            </p>
            <p>
              💳 We never store your complete card details on our servers
            </p>
            <p>
              ✓ Payment processing is PCI DSS compliant through Stripe
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
