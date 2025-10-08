import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Check, Heart, Shield, Users, Award, Globe } from 'lucide-react';
import Link from 'next/link';

export default function AboutPage() {
  return (
    <div className="flex flex-col">
      <section className="relative bg-gradient-to-br from-blue-50 to-teal-50 py-20">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-3xl text-center">
            <Badge className="mb-4 bg-blue-600">About PhysioWellness</Badge>
            <h1 className="mb-6 text-4xl font-bold text-slate-900 md:text-5xl">
              Your Trusted Partner in Health & Recovery
            </h1>
            <p className="text-lg text-slate-600">
              For over a decade, we've been dedicated to providing professional-grade physiotherapy and wellness equipment to help people recover, heal, and thrive.
            </p>
          </div>
        </div>
      </section>

      <section className="bg-white py-16">
        <div className="container mx-auto px-4">
          <div className="grid gap-12 lg:grid-cols-2">
            <div>
              <h2 className="mb-6 text-3xl font-bold text-slate-900">Our Mission</h2>
              <p className="mb-4 text-lg text-slate-600">
                At PhysioWellness, we believe that everyone deserves access to high-quality rehabilitation and wellness equipment. Our mission is to bridge the gap between professional healthcare and home care by offering medical-grade devices that are both effective and accessible.
              </p>
              <p className="mb-6 text-lg text-slate-600">
                We work closely with physical therapists, doctors, and healthcare professionals to curate a selection of products that meet the highest standards of quality and effectiveness.
              </p>
              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <Check className="mt-1 h-5 w-5 flex-shrink-0 text-green-600" />
                  <span className="text-slate-700">Medical-grade quality certified by healthcare professionals</span>
                </div>
                <div className="flex items-start gap-3">
                  <Check className="mt-1 h-5 w-5 flex-shrink-0 text-green-600" />
                  <span className="text-slate-700">Clinically tested and proven effective</span>
                </div>
                <div className="flex items-start gap-3">
                  <Check className="mt-1 h-5 w-5 flex-shrink-0 text-green-600" />
                  <span className="text-slate-700">Comprehensive warranty and customer support</span>
                </div>
              </div>
            </div>
            <div className="relative">
              <img
                src="https://images.pexels.com/photos/3768582/pexels-photo-3768582.jpeg?auto=compress&cs=tinysrgb&w=800"
                alt="Healthcare Professional"
                className="h-full w-full rounded-2xl object-cover shadow-xl"
              />
            </div>
          </div>
        </div>
      </section>

      <section className="bg-slate-50 py-16">
        <div className="container mx-auto px-4">
          <div className="mb-12 text-center">
            <h2 className="mb-4 text-3xl font-bold text-slate-900">Why Choose PhysioWellness</h2>
            <p className="text-lg text-slate-600">
              We're more than just a store – we're your partners in health and recovery
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            <Card>
              <CardContent className="p-6">
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-blue-100">
                  <Shield className="h-6 w-6 text-blue-600" />
                </div>
                <h3 className="mb-2 text-xl font-semibold text-slate-900">Quality Assurance</h3>
                <p className="text-slate-600">
                  Every product undergoes rigorous testing and meets international medical device standards. We only sell what we would use ourselves.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
                  <Heart className="h-6 w-6 text-green-600" />
                </div>
                <h3 className="mb-2 text-xl font-semibold text-slate-900">Expert Guidance</h3>
                <p className="text-slate-600">
                  Our team includes licensed physical therapists who can help you choose the right equipment for your specific needs.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-purple-100">
                  <Users className="h-6 w-6 text-purple-600" />
                </div>
                <h3 className="mb-2 text-xl font-semibold text-slate-900">Customer First</h3>
                <p className="text-slate-600">
                  Your satisfaction is our priority. We offer comprehensive support, easy returns, and a 2-year warranty on all products.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-yellow-100">
                  <Award className="h-6 w-6 text-yellow-600" />
                </div>
                <h3 className="mb-2 text-xl font-semibold text-slate-900">Trusted by Professionals</h3>
                <p className="text-slate-600">
                  Used and recommended by physical therapists, chiropractors, and healthcare facilities worldwide.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-red-100">
                  <Globe className="h-6 w-6 text-red-600" />
                </div>
                <h3 className="mb-2 text-xl font-semibold text-slate-900">Global Reach</h3>
                <p className="text-slate-600">
                  Serving customers in over 50 countries with fast, reliable shipping and local support teams.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-teal-100">
                  <Check className="h-6 w-6 text-teal-600" />
                </div>
                <h3 className="mb-2 text-xl font-semibold text-slate-900">Proven Results</h3>
                <p className="text-slate-600">
                  Over 10,000 satisfied customers have achieved their recovery goals with our products.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      <section className="bg-white py-16">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-3xl text-center">
            <h2 className="mb-6 text-3xl font-bold text-slate-900">Our Commitment to You</h2>
            <p className="mb-8 text-lg text-slate-600">
              We understand that dealing with pain or recovering from an injury can be challenging. That's why we're committed to providing not just products, but a complete support system. From expert product recommendations to post-purchase guidance, we're here for you every step of the way.
            </p>
            <div className="grid gap-6 md:grid-cols-3">
              <div className="text-center">
                <div className="mb-2 text-4xl font-bold text-blue-600">10K+</div>
                <div className="text-slate-600">Happy Customers</div>
              </div>
              <div className="text-center">
                <div className="mb-2 text-4xl font-bold text-blue-600">4.8/5</div>
                <div className="text-slate-600">Average Rating</div>
              </div>
              <div className="text-center">
                <div className="mb-2 text-4xl font-bold text-blue-600">500+</div>
                <div className="text-slate-600">5-Star Reviews</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="bg-gradient-to-br from-blue-600 to-teal-500 py-16 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="mb-4 text-3xl font-bold">Ready to Start Your Recovery Journey?</h2>
          <p className="mb-8 text-lg text-blue-50">
            Browse our collection of professional-grade equipment and find the perfect solution for your needs
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
      </section>
    </div>
  );
}
