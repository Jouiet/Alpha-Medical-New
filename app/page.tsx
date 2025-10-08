import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Heart, Zap, Shield, Truck, CircleCheck as CheckCircle2, ArrowRight, Star } from 'lucide-react';

export default function Home() {
  const categories = [
    {
      name: 'Pain Relief & Relaxation',
      slug: 'pain-relief',
      image: 'https://images.pexels.com/photos/3768582/pexels-photo-3768582.jpeg?auto=compress&cs=tinysrgb&w=800',
      description: 'Cervical, back support & massage therapy',
      productCount: 12
    },
    {
      name: 'Rehabilitation & Mobility',
      slug: 'rehabilitation',
      image: 'https://images.pexels.com/photos/6111619/pexels-photo-6111619.jpeg?auto=compress&cs=tinysrgb&w=800',
      description: 'Upper & lower limb recovery',
      productCount: 8
    },
    {
      name: 'Wellness & Beauty',
      slug: 'wellness',
      image: 'https://images.pexels.com/photos/3757952/pexels-photo-3757952.jpeg?auto=compress&cs=tinysrgb&w=800',
      description: 'Facial care & beauty devices',
      productCount: 6
    }
  ];

  const featuredProducts = [
    {
      id: 1,
      name: 'Medical Neck Traction Device',
      price: 89.99,
      image: 'https://images.pexels.com/photos/6823567/pexels-photo-6823567.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.8,
      reviews: 234,
      badge: 'Best Seller'
    },
    {
      id: 2,
      name: 'Smart Cupping Massage Instrument',
      price: 149.99,
      image: 'https://images.pexels.com/photos/5473184/pexels-photo-5473184.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.9,
      reviews: 189,
      badge: 'New'
    },
    {
      id: 3,
      name: 'Air Pressure Leg Massage Recovery Boots',
      price: 299.99,
      image: 'https://images.pexels.com/photos/8172765/pexels-photo-8172765.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.7,
      reviews: 156,
      badge: 'Popular'
    },
    {
      id: 4,
      name: 'LED Facial Mask with Neck Treatment',
      price: 199.99,
      image: 'https://images.pexels.com/photos/3865618/pexels-photo-3865618.jpeg?auto=compress&cs=tinysrgb&w=600',
      rating: 4.6,
      reviews: 203,
      badge: 'Trending'
    }
  ];

  const benefits = [
    {
      icon: Shield,
      title: 'Medical Grade Quality',
      description: 'All products meet professional healthcare standards'
    },
    {
      icon: Truck,
      title: 'Free Shipping',
      description: 'On orders over $100 with tracking'
    },
    {
      icon: CheckCircle2,
      title: '2-Year Warranty',
      description: 'Complete protection on all devices'
    },
    {
      icon: Heart,
      title: 'Expert Support',
      description: '24/7 professional customer service'
    }
  ];

  return (
    <div className="flex flex-col">
      <section className="relative bg-gradient-to-br from-blue-50 via-teal-50 to-cyan-50 py-20 md:py-32">
        <div className="container mx-auto px-4">
          <div className="grid gap-12 lg:grid-cols-2 lg:gap-8">
            <div className="flex flex-col justify-center">
              <Badge className="mb-4 w-fit bg-blue-600 hover:bg-blue-700">
                Trusted by Healthcare Professionals
              </Badge>
              <h1 className="mb-6 text-4xl font-bold leading-tight tracking-tight text-slate-900 md:text-5xl lg:text-6xl">
                Professional Physiotherapy Equipment for Your Recovery
              </h1>
              <p className="mb-8 text-lg text-slate-600 md:text-xl">
                Discover premium medical-grade devices designed to relieve pain, accelerate rehabilitation, and enhance your well-being.
              </p>
              <div className="flex flex-col gap-4 sm:flex-row">
                <Button size="lg" className="bg-blue-600 hover:bg-blue-700" asChild>
                  <Link href="/products">
                    Shop Now
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Link>
                </Button>
                <Button size="lg" variant="outline" asChild>
                  <Link href="/about">Learn More</Link>
                </Button>
              </div>
              <div className="mt-8 flex items-center gap-8">
                <div>
                  <div className="text-3xl font-bold text-slate-900">10K+</div>
                  <div className="text-sm text-slate-600">Happy Customers</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-slate-900">4.8/5</div>
                  <div className="text-sm text-slate-600">Average Rating</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-slate-900">500+</div>
                  <div className="text-sm text-slate-600">5-Star Reviews</div>
                </div>
              </div>
            </div>
            <div className="relative">
              <div className="relative aspect-square overflow-hidden rounded-2xl bg-white shadow-2xl">
                <img
                  src="https://images.pexels.com/photos/6823567/pexels-photo-6823567.jpeg?auto=compress&cs=tinysrgb&w=800"
                  alt="Physiotherapy Equipment"
                  className="h-full w-full object-cover"
                />
              </div>
              <div className="absolute -bottom-6 -left-6 rounded-lg bg-white p-4 shadow-lg">
                <div className="flex items-center gap-2">
                  <Zap className="h-5 w-5 text-yellow-500" />
                  <span className="font-semibold">Fast Relief Guaranteed</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="border-b bg-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
            {benefits.map((benefit, index) => (
              <div key={index} className="flex flex-col items-center text-center">
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-blue-100">
                  <benefit.icon className="h-6 w-6 text-blue-600" />
                </div>
                <h3 className="mb-2 font-semibold text-slate-900">{benefit.title}</h3>
                <p className="text-sm text-slate-600">{benefit.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-slate-50 py-16 md:py-24">
        <div className="container mx-auto px-4">
          <div className="mb-12 text-center">
            <h2 className="mb-4 text-3xl font-bold text-slate-900 md:text-4xl">
              Shop by Category
            </h2>
            <p className="text-lg text-slate-600">
              Find the perfect equipment for your specific needs
            </p>
          </div>
          <div className="grid gap-6 md:grid-cols-3">
            {categories.map((category) => (
              <Link key={category.slug} href={`/categories/${category.slug}`}>
                <Card className="group overflow-hidden transition-all hover:shadow-lg">
                  <div className="relative aspect-[4/3] overflow-hidden">
                    <img
                      src={category.image}
                      alt={category.name}
                      className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                    <div className="absolute bottom-0 left-0 right-0 p-6 text-white">
                      <h3 className="mb-2 text-xl font-bold">{category.name}</h3>
                      <p className="text-sm text-white/90">{category.description}</p>
                      <p className="mt-2 text-sm font-medium">{category.productCount} products</p>
                    </div>
                  </div>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-white py-16 md:py-24">
        <div className="container mx-auto px-4">
          <div className="mb-12 flex items-end justify-between">
            <div>
              <h2 className="mb-4 text-3xl font-bold text-slate-900 md:text-4xl">
                Featured Products
              </h2>
              <p className="text-lg text-slate-600">
                Our most popular and highly-rated devices
              </p>
            </div>
            <Button variant="outline" asChild className="hidden md:inline-flex">
              <Link href="/products">
                View All
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </div>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {featuredProducts.map((product) => (
              <Card key={product.id} className="group overflow-hidden transition-all hover:shadow-lg">
                <div className="relative aspect-square overflow-hidden">
                  <img
                    src={product.image}
                    alt={product.name}
                    className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
                  />
                  <Badge className="absolute left-3 top-3 bg-blue-600">
                    {product.badge}
                  </Badge>
                </div>
                <CardContent className="p-4">
                  <div className="mb-2 flex items-center gap-1">
                    <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                    <span className="text-sm font-medium text-slate-900">{product.rating}</span>
                    <span className="text-sm text-slate-500">({product.reviews})</span>
                  </div>
                  <h3 className="mb-2 font-semibold text-slate-900 line-clamp-2">
                    {product.name}
                  </h3>
                  <div className="flex items-center justify-between">
                    <span className="text-xl font-bold text-blue-600">
                      ${product.price}
                    </span>
                    <Button size="sm" variant="outline">
                      View
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
          <div className="mt-8 text-center md:hidden">
            <Button variant="outline" asChild>
              <Link href="/products">
                View All Products
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </div>
      </section>

      <section className="bg-gradient-to-br from-blue-600 to-teal-500 py-16 text-white md:py-20">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-3xl text-center">
            <h2 className="mb-4 text-3xl font-bold md:text-4xl">
              Start Your Recovery Journey Today
            </h2>
            <p className="mb-8 text-lg text-blue-50">
              Join thousands of satisfied customers who trust PhysioWellness for their health and recovery needs. Professional equipment, expert support, guaranteed results.
            </p>
            <div className="flex flex-col gap-4 sm:flex-row sm:justify-center">
              <Button size="lg" variant="secondary" asChild>
                <Link href="/products">Shop All Products</Link>
              </Button>
              <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-blue-600" asChild>
                <Link href="/contact">Contact Us</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      <section className="bg-slate-50 py-16 md:py-20">
        <div className="container mx-auto px-4">
          <div className="mb-12 text-center">
            <h2 className="mb-4 text-3xl font-bold text-slate-900 md:text-4xl">
              What Our Customers Say
            </h2>
            <p className="text-lg text-slate-600">
              Real stories from real people
            </p>
          </div>
          <div className="grid gap-6 md:grid-cols-3">
            {[
              {
                name: 'Sarah Johnson',
                role: 'Physical Therapist',
                text: 'The neck traction device has been a game-changer for my patients. Quality is outstanding and results are immediate.',
                rating: 5
              },
              {
                name: 'Michael Chen',
                role: 'Athlete',
                text: 'Recovery boots are incredible. I use them after every training session. My legs feel fresh and ready for the next day.',
                rating: 5
              },
              {
                name: 'Emily Roberts',
                role: 'Office Worker',
                text: 'After years of back pain, the posture corrector has transformed my daily comfort. Highly recommend!',
                rating: 5
              }
            ].map((testimonial, index) => (
              <Card key={index}>
                <CardContent className="p-6">
                  <div className="mb-4 flex">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                    ))}
                  </div>
                  <p className="mb-4 text-slate-600">{testimonial.text}</p>
                  <div>
                    <div className="font-semibold text-slate-900">{testimonial.name}</div>
                    <div className="text-sm text-slate-500">{testimonial.role}</div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
