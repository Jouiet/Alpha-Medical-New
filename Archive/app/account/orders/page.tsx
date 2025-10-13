'use client';

import Link from 'next/link';
import { ArrowLeft, Package, Truck, CheckCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

const orders = [
  {
    id: 'ORD-2025-001',
    date: 'March 15, 2025',
    status: 'delivered',
    total: 289.97,
    items: [
      { id: 1, name: 'Medical Neck Traction Device', price: 89.99, quantity: 1, image: 'https://images.pexels.com/photos/6823567/pexels-photo-6823567.jpeg?auto=compress&cs=tinysrgb&w=150' },
      { id: 2, name: 'Smart Cupping Massage Instrument', price: 149.99, quantity: 1, image: 'https://images.pexels.com/photos/5473184/pexels-photo-5473184.jpeg?auto=compress&cs=tinysrgb&w=150' },
      { id: 3, name: 'Posture Corrector Back Brace', price: 49.99, quantity: 1, image: 'https://images.pexels.com/photos/6823574/pexels-photo-6823574.jpeg?auto=compress&cs=tinysrgb&w=150' },
    ],
    tracking: 'TRK789456123',
    deliveryDate: 'March 18, 2025'
  },
  {
    id: 'ORD-2025-002',
    date: 'March 10, 2025',
    status: 'shipped',
    total: 149.99,
    items: [
      { id: 1, name: 'LED Facial Mask with Neck Treatment', price: 149.99, quantity: 1, image: 'https://images.pexels.com/photos/3865618/pexels-photo-3865618.jpeg?auto=compress&cs=tinysrgb&w=150' },
    ],
    tracking: 'TRK123456789',
    estimatedDelivery: 'March 14, 2025'
  },
  {
    id: 'ORD-2025-003',
    date: 'March 5, 2025',
    status: 'delivered',
    total: 199.98,
    items: [
      { id: 1, name: 'Heated Rehabilitation Robot Gloves', price: 99.99, quantity: 2, image: 'https://images.pexels.com/photos/6823587/pexels-photo-6823587.jpeg?auto=compress&cs=tinysrgb&w=150' },
    ],
    tracking: 'TRK987654321',
    deliveryDate: 'March 8, 2025'
  },
  {
    id: 'ORD-2025-004',
    date: 'February 28, 2025',
    status: 'processing',
    total: 79.99,
    items: [
      { id: 1, name: 'Posture Corrector Back Brace', price: 49.99, quantity: 1, image: 'https://images.pexels.com/photos/6823574/pexels-photo-6823574.jpeg?auto=compress&cs=tinysrgb&w=150' },
      { id: 2, name: 'Thermal Knee Massager', price: 30.00, quantity: 1, image: 'https://images.pexels.com/photos/6823581/pexels-photo-6823581.jpeg?auto=compress&cs=tinysrgb&w=150' },
    ],
  },
];

const getStatusBadge = (status: string) => {
  switch (status) {
    case 'delivered':
      return <Badge className="bg-green-600"><CheckCircle className="mr-1 h-3 w-3" /> Delivered</Badge>;
    case 'shipped':
      return <Badge className="bg-blue-600"><Truck className="mr-1 h-3 w-3" /> Shipped</Badge>;
    case 'processing':
      return <Badge className="bg-yellow-600"><Package className="mr-1 h-3 w-3" /> Processing</Badge>;
    default:
      return <Badge>{status}</Badge>;
  }
};

export default function OrdersPage() {
  const filterOrders = (status?: string) => {
    if (!status) return orders;
    return orders.filter(order => order.status === status);
  };

  const OrdersList = ({ filteredOrders }: { filteredOrders: typeof orders }) => (
    <div className="space-y-6">
      {filteredOrders.length > 0 ? (
        filteredOrders.map((order) => (
          <Card key={order.id}>
            <CardContent className="p-6">
              <div className="mb-4 flex items-start justify-between">
                <div>
                  <p className="text-lg font-semibold text-slate-900">{order.id}</p>
                  <p className="text-sm text-slate-600">{order.date}</p>
                </div>
                <div className="text-right">
                  {getStatusBadge(order.status)}
                  <p className="mt-2 text-lg font-bold text-slate-900">${order.total.toFixed(2)}</p>
                </div>
              </div>

              <div className="space-y-3">
                {order.items.map((item, index) => (
                  <div key={index} className="flex gap-4">
                    <img
                      src={item.image}
                      alt={item.name}
                      className="h-16 w-16 rounded object-cover"
                    />
                    <div className="flex-1">
                      <p className="font-medium text-slate-900">{item.name}</p>
                      <p className="text-sm text-slate-600">
                        Qty: {item.quantity} × ${item.price.toFixed(2)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              {order.tracking && (
                <div className="mt-4 border-t pt-4">
                  <p className="text-sm text-slate-600">
                    <strong>Tracking Number:</strong> {order.tracking}
                  </p>
                  {order.deliveryDate && (
                    <p className="text-sm text-slate-600">
                      <strong>Delivered:</strong> {order.deliveryDate}
                    </p>
                  )}
                  {order.estimatedDelivery && (
                    <p className="text-sm text-slate-600">
                      <strong>Estimated Delivery:</strong> {order.estimatedDelivery}
                    </p>
                  )}
                </div>
              )}

              <div className="mt-4 flex gap-2">
                <Button variant="outline" size="sm">
                  View Details
                </Button>
                {order.status === 'delivered' && (
                  <Button variant="outline" size="sm">
                    Buy Again
                  </Button>
                )}
                {order.status === 'shipped' && (
                  <Button variant="outline" size="sm">
                    Track Package
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        ))
      ) : (
        <div className="py-12 text-center">
          <Package className="mx-auto h-16 w-16 text-slate-300" />
          <p className="mt-4 text-lg text-slate-600">No orders found</p>
        </div>
      )}
    </div>
  );

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <Link href="/account" className="inline-flex items-center text-blue-600 hover:text-blue-700">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Account
        </Link>
      </div>

      <div className="mb-8">
        <h1 className="mb-2 text-3xl font-bold text-slate-900">My Orders</h1>
        <p className="text-slate-600">View and track your orders</p>
      </div>

      <Tabs defaultValue="all" className="w-full">
        <TabsList className="mb-6">
          <TabsTrigger value="all">All Orders ({orders.length})</TabsTrigger>
          <TabsTrigger value="processing">Processing ({filterOrders('processing').length})</TabsTrigger>
          <TabsTrigger value="shipped">Shipped ({filterOrders('shipped').length})</TabsTrigger>
          <TabsTrigger value="delivered">Delivered ({filterOrders('delivered').length})</TabsTrigger>
        </TabsList>

        <TabsContent value="all">
          <OrdersList filteredOrders={orders} />
        </TabsContent>
        <TabsContent value="processing">
          <OrdersList filteredOrders={filterOrders('processing')} />
        </TabsContent>
        <TabsContent value="shipped">
          <OrdersList filteredOrders={filterOrders('shipped')} />
        </TabsContent>
        <TabsContent value="delivered">
          <OrdersList filteredOrders={filterOrders('delivered')} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
