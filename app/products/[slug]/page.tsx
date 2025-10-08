'use client';

import { useState } from 'react';
import { useParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Star, Check, Shield, Truck, Heart, Share2, ChevronLeft, ChevronRight } from 'lucide-react';
import { useCart } from '@/contexts/CartContext';
import { toast } from 'sonner';
import Link from 'next/link';

export default function ProductPage() {
  const params = useParams();
  const { addToCart } = useCart();
  const [quantity, setQuantity] = useState(1);
  const [selectedImage, setSelectedImage] = useState(0);

  const product = {
    id: 1,
    name: 'Medical Neck Traction Device',
    slug: 'medical-neck-traction-device',
    price: 89.99,
    comparePrice: 129.99,
    rating: 4.8,
    reviews: 234,
    inStock: true,
    stockQuantity: 45,
    images: [
      'https://images.pexels.com/photos/6823567/pexels-photo-6823567.jpeg?auto=compress&cs=tinysrgb&w=800',
      'https://images.pexels.com/photos/6823574/pexels-photo-6823574.jpeg?auto=compress&cs=tinysrgb&w=800',
      'https://images.pexels.com/photos/6823581/pexels-photo-6823581.jpeg?auto=compress&cs=tinysrgb&w=800'
    ],
    description: 'Professional-grade cervical traction device designed to relieve neck pain, reduce muscle tension, and improve posture. Clinically tested and recommended by physical therapists.',
    shortDescription: 'Relieve neck pain and improve posture with this medical-grade traction device.',
    features: [
      'Adjustable traction force for personalized treatment',
      'Ergonomic design fits all neck sizes',
      'Medical-grade materials ensure safety and comfort',
      'Portable and easy to use at home or office',
      'Helps reduce headaches and muscle tension'
    ],
    benefits: [
      'Immediate relief from neck pain and stiffness',
      'Improves cervical spine alignment',
      'Reduces pressure on nerve roots',
      'Promotes better posture and spinal health',
      'Non-invasive alternative to surgery'
    ],
    specifications: {
      'Material': 'Medical-grade ABS plastic and soft padding',
      'Weight': '0.8 lbs',
      'Dimensions': '10 x 8 x 4 inches',
      'Adjustability': '3 levels of traction',
      'Warranty': '2 years manufacturer warranty'
    },
    faqs: [
      {
        question: 'How long should I use the device each session?',
        answer: 'We recommend starting with 10-15 minutes per session, 2-3 times daily. Gradually increase duration as your neck becomes accustomed to the treatment.'
      },
      {
        question: 'Is this suitable for severe neck pain?',
        answer: 'This device is designed for mild to moderate neck pain. For severe or chronic conditions, please consult with a healthcare professional before use.'
      },
      {
        question: 'Can I use this while sleeping?',
        answer: 'No, this device is designed for active use while sitting upright. Do not use while sleeping or lying down.'
      }
    ]
  };

  const reviews = [
    {
      id: 1,
      author: 'Sarah M.',
      rating: 5,
      date: '2 weeks ago',
      verified: true,
      title: 'Life-changing device!',
      comment: 'After years of chronic neck pain from office work, this device has been a game-changer. I use it every morning and evening, and the relief is immediate.'
    },
    {
      id: 2,
      author: 'John D.',
      rating: 5,
      date: '1 month ago',
      verified: true,
      title: 'Highly recommended',
      comment: 'My physical therapist recommended this, and it works exactly as described. Quality is excellent, and it is very easy to use.'
    },
    {
      id: 3,
      author: 'Emily R.',
      rating: 4,
      date: '3 weeks ago',
      verified: true,
      title: 'Great product',
      comment: 'Very effective for my neck pain. Took a few days to get used to, but now I cannot imagine my routine without it.'
    }
  ];

  const handleAddToCart = () => {
    addToCart({
      id: product.id.toString(),
      variantId: product.id.toString(),
      name: product.name,
      price: product.price,
      quantity: quantity,
      image: product.images[0]
    });
    toast.success('Added to cart!');
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-4">
        <Link href="/products" className="text-sm text-blue-600 hover:underline">
          ← Back to Products
        </Link>
      </div>

      <div className="grid gap-8 lg:grid-cols-2">
        <div>
          <div className="sticky top-20">
            <div className="relative mb-4 aspect-square overflow-hidden rounded-lg bg-slate-100">
              <img
                src={product.images[selectedImage]}
                alt={product.name}
                className="h-full w-full object-cover"
              />
              {product.comparePrice && (
                <Badge className="absolute left-4 top-4 bg-red-600">
                  Save ${(product.comparePrice - product.price).toFixed(2)}
                </Badge>
              )}
            </div>

            <div className="grid grid-cols-3 gap-2">
              {product.images.map((image, index) => (
                <button
                  key={index}
                  onClick={() => setSelectedImage(index)}
                  className={`aspect-square overflow-hidden rounded-lg border-2 transition-all ${
                    selectedImage === index ? 'border-blue-600' : 'border-slate-200'
                  }`}
                >
                  <img src={image} alt={`${product.name} ${index + 1}`} className="h-full w-full object-cover" />
                </button>
              ))}
            </div>
          </div>
        </div>

        <div>
          <div className="mb-4">
            <Badge variant="outline" className="mb-2">Pain Relief & Relaxation</Badge>
            <h1 className="mb-2 text-3xl font-bold text-slate-900">{product.name}</h1>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-1">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    className={`h-5 w-5 ${
                      i < Math.floor(product.rating)
                        ? 'fill-yellow-400 text-yellow-400'
                        : 'text-slate-300'
                    }`}
                  />
                ))}
                <span className="ml-2 font-medium text-slate-900">{product.rating}</span>
              </div>
              <span className="text-slate-600">({product.reviews} reviews)</span>
            </div>
          </div>

          <p className="mb-6 text-slate-600">{product.shortDescription}</p>

          <div className="mb-6">
            <div className="flex items-baseline gap-3">
              <span className="text-4xl font-bold text-blue-600">${product.price}</span>
              {product.comparePrice && (
                <span className="text-xl text-slate-400 line-through">
                  ${product.comparePrice}
                </span>
              )}
            </div>
            {product.inStock ? (
              <p className="mt-2 text-sm text-green-600">
                <Check className="mr-1 inline h-4 w-4" />
                In stock ({product.stockQuantity} available)
              </p>
            ) : (
              <p className="mt-2 text-sm text-red-600">Out of stock</p>
            )}
          </div>

          <Separator className="my-6" />

          <div className="mb-6">
            <label className="mb-2 block text-sm font-medium text-slate-900">Quantity</label>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                >
                  <ChevronLeft className="h-4 w-4" />
                </Button>
                <span className="w-12 text-center font-medium">{quantity}</span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setQuantity(Math.min(product.stockQuantity, quantity + 1))}
                >
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>

          <div className="mb-6 flex gap-3">
            <Button
              size="lg"
              className="flex-1 bg-blue-600 hover:bg-blue-700"
              onClick={handleAddToCart}
              disabled={!product.inStock}
            >
              Add to Cart
            </Button>
            <Button size="lg" variant="outline">
              <Heart className="h-5 w-5" />
            </Button>
            <Button size="lg" variant="outline">
              <Share2 className="h-5 w-5" />
            </Button>
          </div>

          <div className="grid gap-4 rounded-lg bg-slate-50 p-4">
            <div className="flex items-center gap-3">
              <Shield className="h-5 w-5 text-blue-600" />
              <div>
                <p className="font-medium text-slate-900">2-Year Warranty</p>
                <p className="text-sm text-slate-600">Full coverage on all defects</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Truck className="h-5 w-5 text-blue-600" />
              <div>
                <p className="font-medium text-slate-900">Free Shipping</p>
                <p className="text-sm text-slate-600">On orders over $100</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-12">
        <Tabs defaultValue="description" className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="description">Description</TabsTrigger>
            <TabsTrigger value="benefits">Benefits</TabsTrigger>
            <TabsTrigger value="specs">Specifications</TabsTrigger>
            <TabsTrigger value="reviews">Reviews ({product.reviews})</TabsTrigger>
          </TabsList>

          <TabsContent value="description" className="mt-6">
            <Card>
              <CardContent className="p-6">
                <h3 className="mb-4 text-xl font-semibold text-slate-900">Product Description</h3>
                <p className="mb-6 text-slate-600">{product.description}</p>

                <h4 className="mb-3 font-semibold text-slate-900">Key Features:</h4>
                <ul className="space-y-2">
                  {product.features.map((feature, index) => (
                    <li key={index} className="flex items-start gap-2 text-slate-600">
                      <Check className="mt-0.5 h-5 w-5 flex-shrink-0 text-green-600" />
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="benefits" className="mt-6">
            <Card>
              <CardContent className="p-6">
                <h3 className="mb-4 text-xl font-semibold text-slate-900">Health Benefits</h3>
                <ul className="space-y-3">
                  {product.benefits.map((benefit, index) => (
                    <li key={index} className="flex items-start gap-3">
                      <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-blue-100">
                        <Check className="h-5 w-5 text-blue-600" />
                      </div>
                      <div>
                        <p className="font-medium text-slate-900">{benefit}</p>
                      </div>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="specs" className="mt-6">
            <Card>
              <CardContent className="p-6">
                <h3 className="mb-4 text-xl font-semibold text-slate-900">Technical Specifications</h3>
                <div className="space-y-3">
                  {Object.entries(product.specifications).map(([key, value]) => (
                    <div key={key} className="flex justify-between border-b pb-2">
                      <span className="font-medium text-slate-900">{key}</span>
                      <span className="text-slate-600">{value}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="reviews" className="mt-6">
            <Card>
              <CardContent className="p-6">
                <div className="mb-6 flex items-center justify-between">
                  <h3 className="text-xl font-semibold text-slate-900">Customer Reviews</h3>
                  <Button variant="outline">Write a Review</Button>
                </div>

                <div className="space-y-6">
                  {reviews.map((review) => (
                    <div key={review.id} className="border-b pb-6 last:border-b-0">
                      <div className="mb-2 flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <span className="font-medium text-slate-900">{review.author}</span>
                          {review.verified && (
                            <Badge variant="outline" className="text-xs">
                              Verified Purchase
                            </Badge>
                          )}
                        </div>
                        <span className="text-sm text-slate-500">{review.date}</span>
                      </div>

                      <div className="mb-2 flex items-center gap-1">
                        {[...Array(5)].map((_, i) => (
                          <Star
                            key={i}
                            className={`h-4 w-4 ${
                              i < review.rating
                                ? 'fill-yellow-400 text-yellow-400'
                                : 'text-slate-300'
                            }`}
                          />
                        ))}
                      </div>

                      <h4 className="mb-2 font-semibold text-slate-900">{review.title}</h4>
                      <p className="text-slate-600">{review.comment}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
