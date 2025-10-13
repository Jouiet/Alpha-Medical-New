'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { User, Package, Heart, MapPin, CreditCard, Settings } from 'lucide-react';
import Link from 'next/link';

export default function AccountPage() {
  const recentOrders = [
    {
      id: 'ORD-2025-001',
      date: 'March 15, 2025',
      status: 'Delivered',
      total: 289.97,
      items: 3
    },
    {
      id: 'ORD-2025-002',
      date: 'March 10, 2025',
      status: 'In Transit',
      total: 149.99,
      items: 1
    },
    {
      id: 'ORD-2025-003',
      date: 'March 5, 2025',
      status: 'Delivered',
      total: 199.98,
      items: 2
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="mb-2 text-3xl font-bold text-slate-900">My Account</h1>
        <p className="text-slate-600">Manage your orders, profile, and preferences</p>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <Link href="/account/profile">
            <CardContent className="flex items-center gap-4 p-6">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-100">
                <User className="h-6 w-6 text-blue-600" />
              </div>
              <div>
                <h3 className="font-semibold text-slate-900">Profile</h3>
                <p className="text-sm text-slate-600">Edit your information</p>
              </div>
            </CardContent>
          </Link>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <Link href="/account/orders">
            <CardContent className="flex items-center gap-4 p-6">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
                <Package className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <h3 className="font-semibold text-slate-900">Orders</h3>
                <p className="text-sm text-slate-600">View order history</p>
              </div>
            </CardContent>
          </Link>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <Link href="/account/wishlist">
            <CardContent className="flex items-center gap-4 p-6">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-red-100">
                <Heart className="h-6 w-6 text-red-600" />
              </div>
              <div>
                <h3 className="font-semibold text-slate-900">Wishlist</h3>
                <p className="text-sm text-slate-600">Saved items</p>
              </div>
            </CardContent>
          </Link>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <Link href="/account/addresses">
            <CardContent className="flex items-center gap-4 p-6">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-yellow-100">
                <MapPin className="h-6 w-6 text-yellow-600" />
              </div>
              <div>
                <h3 className="font-semibold text-slate-900">Addresses</h3>
                <p className="text-sm text-slate-600">Manage addresses</p>
              </div>
            </CardContent>
          </Link>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <Link href="/account/payment">
            <CardContent className="flex items-center gap-4 p-6">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-purple-100">
                <CreditCard className="h-6 w-6 text-purple-600" />
              </div>
              <div>
                <h3 className="font-semibold text-slate-900">Payment</h3>
                <p className="text-sm text-slate-600">Payment methods</p>
              </div>
            </CardContent>
          </Link>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <Link href="/account/settings">
            <CardContent className="flex items-center gap-4 p-6">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-slate-100">
                <Settings className="h-6 w-6 text-slate-600" />
              </div>
              <div>
                <h3 className="font-semibold text-slate-900">Settings</h3>
                <p className="text-sm text-slate-600">Account preferences</p>
              </div>
            </CardContent>
          </Link>
        </Card>
      </div>

      <Card className="mt-8">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Recent Orders</CardTitle>
            <Button variant="outline" size="sm" asChild>
              <Link href="/account/orders">View All</Link>
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recentOrders.map((order) => (
              <div key={order.id} className="flex items-center justify-between border-b pb-4 last:border-b-0">
                <div>
                  <p className="font-semibold text-slate-900">{order.id}</p>
                  <p className="text-sm text-slate-600">{order.date}</p>
                  <p className="text-sm text-slate-600">{order.items} items</p>
                </div>
                <div className="text-right">
                  <p className="font-bold text-slate-900">${order.total.toFixed(2)}</p>
                  <Badge
                    className={
                      order.status === 'Delivered'
                        ? 'bg-green-600'
                        : order.status === 'In Transit'
                        ? 'bg-blue-600'
                        : 'bg-yellow-600'
                    }
                  >
                    {order.status}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
