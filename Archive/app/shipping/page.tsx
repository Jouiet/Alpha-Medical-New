import { Metadata } from 'next';
import { Truck, Package, RotateCcw, Clock, MapPin, DollarSign } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Shipping & Returns | Alpha Medical Care',
  description: 'Shipping information, delivery times, and return policy for Alpha Medical Care products',
};

export default function ShippingPage() {
  return (
    <div className="container mx-auto px-4 py-12 max-w-4xl">
      <h1 className="mb-8 text-4xl font-bold text-slate-900">Shipping & Returns</h1>

      <div className="space-y-12 text-slate-700">
        {/* Shipping Information */}
        <section>
          <div className="mb-6 flex items-center gap-3">
            <Truck className="h-8 w-8 text-blue-600" />
            <h2 className="text-3xl font-semibold text-slate-900">Shipping Information</h2>
          </div>

          <div className="space-y-6">
            <div>
              <h3 className="mb-3 text-xl font-medium text-slate-800">Free Shipping</h3>
              <p className="mb-4">
                We offer <strong>FREE standard shipping</strong> on all orders over <strong>$100</strong> within the continental United States. No coupon code required—the discount is automatically applied at checkout.
              </p>
            </div>

            <div className="rounded-lg bg-blue-50 p-6 border border-blue-200">
              <h3 className="mb-4 text-xl font-medium text-blue-900 flex items-center gap-2">
                <DollarSign className="h-5 w-5" />
                Shipping Rates
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between border-b border-blue-200 pb-2">
                  <span className="font-medium">Standard Shipping (5-7 business days)</span>
                  <span>$9.99</span>
                </div>
                <div className="flex justify-between border-b border-blue-200 pb-2">
                  <span className="font-medium">Express Shipping (2-3 business days)</span>
                  <span>$19.99</span>
                </div>
                <div className="flex justify-between border-b border-blue-200 pb-2">
                  <span className="font-medium">Overnight Shipping (1 business day)</span>
                  <span>$39.99</span>
                </div>
                <div className="flex justify-between pt-2">
                  <span className="font-medium text-green-700">Orders over $100</span>
                  <span className="font-bold text-green-700">FREE Standard Shipping</span>
                </div>
              </div>
            </div>

            <div>
              <h3 className="mb-3 text-xl font-medium text-slate-800 flex items-center gap-2">
                <MapPin className="h-5 w-5 text-blue-600" />
                Shipping Destinations
              </h3>
              <p className="mb-4">
                We currently ship to all 50 United States, including Alaska and Hawaii. International shipping is available to select countries:
              </p>
              <div className="grid gap-3 sm:grid-cols-2">
                <div className="rounded-lg border border-slate-200 p-4">
                  <h4 className="mb-2 font-semibold text-slate-800">United States</h4>
                  <ul className="space-y-1 text-sm">
                    <li>• All 50 states</li>
                    <li>• Standard, Express, and Overnight options</li>
                    <li>• Free shipping over $100</li>
                  </ul>
                </div>
                <div className="rounded-lg border border-slate-200 p-4">
                  <h4 className="mb-2 font-semibold text-slate-800">International</h4>
                  <ul className="space-y-1 text-sm">
                    <li>• Canada</li>
                    <li>• United Kingdom</li>
                    <li>• European Union countries</li>
                    <li>• Rates calculated at checkout</li>
                  </ul>
                </div>
              </div>
              <p className="mt-4 text-sm text-slate-600">
                <strong>Note:</strong> International orders may be subject to customs duties and import taxes, which are the responsibility of the recipient.
              </p>
            </div>
          </div>
        </section>

        {/* Processing & Delivery Times */}
        <section>
          <div className="mb-6 flex items-center gap-3">
            <Clock className="h-8 w-8 text-blue-600" />
            <h2 className="text-3xl font-semibold text-slate-900">Processing & Delivery Times</h2>
          </div>

          <div className="space-y-6">
            <div>
              <h3 className="mb-3 text-xl font-medium text-slate-800">Order Processing</h3>
              <p className="mb-4">
                Orders are typically processed within <strong>1-2 business days</strong> (Monday-Friday, excluding holidays). You will receive an email confirmation when your order is placed and another email with tracking information when your order ships.
              </p>
              <div className="rounded-lg bg-slate-50 p-4 border border-slate-200">
                <p className="text-sm">
                  <strong>Processing Time:</strong> 1-2 business days<br />
                  <strong>Cutoff Time:</strong> Orders placed before 2:00 PM EST are processed the same business day<br />
                  <strong>Weekend Orders:</strong> Orders placed on weekends are processed on the next business day
                </p>
              </div>
            </div>

            <div>
              <h3 className="mb-3 text-xl font-medium text-slate-800">Estimated Delivery Times</h3>
              <p className="mb-4">
                Delivery times are calculated from the ship date, not the order date:
              </p>
              <div className="space-y-3">
                <div className="flex items-start gap-3 rounded-lg border border-slate-200 p-4">
                  <Package className="mt-1 h-5 w-5 flex-shrink-0 text-blue-600" />
                  <div>
                    <h4 className="mb-1 font-semibold text-slate-800">Standard Shipping</h4>
                    <p className="text-sm">5-7 business days after shipping</p>
                  </div>
                </div>
                <div className="flex items-start gap-3 rounded-lg border border-slate-200 p-4">
                  <Package className="mt-1 h-5 w-5 flex-shrink-0 text-blue-600" />
                  <div>
                    <h4 className="mb-1 font-semibold text-slate-800">Express Shipping</h4>
                    <p className="text-sm">2-3 business days after shipping</p>
                  </div>
                </div>
                <div className="flex items-start gap-3 rounded-lg border border-slate-200 p-4">
                  <Package className="mt-1 h-5 w-5 flex-shrink-0 text-blue-600" />
                  <div>
                    <h4 className="mb-1 font-semibold text-slate-800">Overnight Shipping</h4>
                    <p className="text-sm">1 business day after shipping (orders must be placed before 12:00 PM EST)</p>
                  </div>
                </div>
              </div>
              <p className="mt-4 text-sm text-slate-600">
                <strong>Note:</strong> Delivery times are estimates and not guaranteed. Delays may occur due to weather, carrier issues, or other unforeseen circumstances.
              </p>
            </div>

            <div>
              <h3 className="mb-3 text-xl font-medium text-slate-800">Order Tracking</h3>
              <p className="mb-4">
                Once your order ships, you will receive an email with a tracking number. You can track your package by:
              </p>
              <ul className="mb-4 ml-6 list-disc space-y-2">
                <li>Clicking the tracking link in your shipping confirmation email</li>
                <li>Logging into your account and viewing order history</li>
                <li>Visiting the carrier's website directly with your tracking number</li>
              </ul>
              <p className="text-sm text-slate-600">
                Tracking information may take 24-48 hours to become active after receiving your shipping notification.
              </p>
            </div>
          </div>
        </section>

        {/* Returns & Exchanges */}
        <section>
          <div className="mb-6 flex items-center gap-3">
            <RotateCcw className="h-8 w-8 text-blue-600" />
            <h2 className="text-3xl font-semibold text-slate-900">Returns & Exchanges</h2>
          </div>

          <div className="space-y-6">
            <div className="rounded-lg bg-green-50 p-6 border border-green-200">
              <h3 className="mb-3 text-xl font-medium text-green-900">30-Day Money-Back Guarantee</h3>
              <p className="text-green-800">
                We stand behind the quality of our products. If you're not completely satisfied with your purchase, you can return it within <strong>30 days</strong> of delivery for a full refund or exchange.
              </p>
            </div>

            <div>
              <h3 className="mb-3 text-xl font-medium text-slate-800">Return Eligibility</h3>
              <p className="mb-4">To be eligible for a return, items must meet the following conditions:</p>
              <ul className="mb-4 ml-6 list-disc space-y-2">
                <li>Item must be unused and in the same condition as received</li>
                <li>Item must be in original packaging with all tags and accessories</li>
                <li>Return must be initiated within 30 days of delivery</li>
                <li>Proof of purchase (order confirmation or receipt) required</li>
              </ul>

              <div className="rounded-lg border border-red-200 bg-red-50 p-4">
                <h4 className="mb-2 font-semibold text-red-900">Non-Returnable Items</h4>
                <p className="mb-2 text-sm text-red-800">For health and safety reasons, the following items cannot be returned:</p>
                <ul className="ml-6 list-disc space-y-1 text-sm text-red-800">
                  <li>Items marked as "Final Sale"</li>
                  <li>Opened or used personal care items (unless defective)</li>
                  <li>Items without original packaging or tags</li>
                  <li>Gift cards and promotional items</li>
                </ul>
              </div>
            </div>

            <div>
              <h3 className="mb-3 text-xl font-medium text-slate-800">How to Initiate a Return</h3>
              <div className="space-y-4">
                <div className="flex gap-4">
                  <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-blue-600 text-white font-bold">1</div>
                  <div>
                    <h4 className="mb-1 font-semibold">Contact Us</h4>
                    <p className="text-sm">Email <a href="mailto:returns@alphamedicalcare.com" className="text-blue-600 hover:underline">returns@alphamedicalcare.com</a> with your order number and reason for return.</p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-blue-600 text-white font-bold">2</div>
                  <div>
                    <h4 className="mb-1 font-semibold">Receive Authorization</h4>
                    <p className="text-sm">We'll provide a Return Authorization (RA) number and return shipping instructions within 24 hours.</p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-blue-600 text-white font-bold">3</div>
                  <div>
                    <h4 className="mb-1 font-semibold">Pack Your Item</h4>
                    <p className="text-sm">Securely pack the item in its original packaging. Include the RA number inside the box.</p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-blue-600 text-white font-bold">4</div>
                  <div>
                    <h4 className="mb-1 font-semibold">Ship the Item</h4>
                    <p className="text-sm">Ship the item using a trackable shipping method. We recommend insuring valuable items.</p>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h3 className="mb-3 text-xl font-medium text-slate-800">Return Shipping Costs</h3>
              <div className="space-y-3">
                <div className="rounded-lg border border-slate-200 p-4">
                  <h4 className="mb-2 font-semibold text-slate-800">Defective or Incorrect Items</h4>
                  <p className="text-sm">We will provide a prepaid return label at no cost to you.</p>
                </div>
                <div className="rounded-lg border border-slate-200 p-4">
                  <h4 className="mb-2 font-semibold text-slate-800">Change of Mind Returns</h4>
                  <p className="text-sm">Customer is responsible for return shipping costs. We recommend using a trackable shipping method.</p>
                </div>
              </div>
            </div>

            <div>
              <h3 className="mb-3 text-xl font-medium text-slate-800">Refund Processing</h3>
              <p className="mb-4">Once we receive and inspect your return:</p>
              <ul className="mb-4 ml-6 list-disc space-y-2">
                <li>You will receive an email confirmation that we've received your return</li>
                <li>Refunds are processed within <strong>5-7 business days</strong> of receiving the return</li>
                <li>Refunds are issued to the original payment method</li>
                <li>Depending on your bank or credit card company, it may take an additional 5-10 business days for the refund to appear in your account</li>
                <li>Original shipping charges are non-refundable (except for defective or incorrect items)</li>
              </ul>
            </div>

            <div>
              <h3 className="mb-3 text-xl font-medium text-slate-800">Exchanges</h3>
              <p className="mb-4">
                We currently do not offer direct exchanges. If you need a different item, please return the original item for a refund and place a new order. This ensures you receive your replacement as quickly as possible.
              </p>
            </div>

            <div>
              <h3 className="mb-3 text-xl font-medium text-slate-800">Damaged or Defective Items</h3>
              <p className="mb-4">
                If you receive a damaged or defective item:
              </p>
              <ul className="mb-4 ml-6 list-disc space-y-2">
                <li>Contact us immediately at <a href="mailto:support@alphamedicalcare.com" className="text-blue-600 hover:underline">support@alphamedicalcare.com</a></li>
                <li>Include photos of the damage or defect</li>
                <li>We will arrange a replacement or full refund at no cost to you</li>
                <li>We will provide a prepaid return label for defective items</li>
              </ul>
              <p className="text-sm text-slate-600">
                Please report damaged or defective items within <strong>7 days</strong> of delivery.
              </p>
            </div>
          </div>
        </section>

        {/* International Orders */}
        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">International Orders</h2>
          <div className="space-y-4">
            <div>
              <h3 className="mb-3 text-xl font-medium text-slate-800">Customs and Duties</h3>
              <p className="mb-4">
                International customers are responsible for all customs duties, taxes, and brokerage fees imposed by their country. These charges are not included in the product price or shipping cost and are collected by the carrier upon delivery.
              </p>
            </div>
            <div>
              <h3 className="mb-3 text-xl font-medium text-slate-800">International Returns</h3>
              <p className="mb-4">
                International returns are accepted under the same 30-day policy. However, customers are responsible for return shipping costs and any customs fees. We recommend purchasing international shipping insurance for returns.
              </p>
            </div>
            <div>
              <h3 className="mb-3 text-xl font-medium text-slate-800">Delivery Times</h3>
              <p className="mb-4">
                International shipping typically takes <strong>7-21 business days</strong> depending on the destination country. Delays may occur due to customs processing.
              </p>
            </div>
          </div>
        </section>

        {/* Contact Section */}
        <section className="rounded-lg bg-slate-50 p-8 border border-slate-200">
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">Questions About Your Order?</h2>
          <p className="mb-6">
            Our customer service team is here to help with any shipping or return questions.
          </p>
          <div className="space-y-3">
            <p>
              <strong>Email:</strong> <a href="mailto:support@alphamedicalcare.com" className="text-blue-600 hover:underline">support@alphamedicalcare.com</a>
            </p>
            <p>
              <strong>Phone:</strong> <a href="tel:+15551234567" className="text-blue-600 hover:underline">+1 (555) 123-4567</a>
            </p>
            <p>
              <strong>Hours:</strong> Monday-Friday, 9:00 AM - 6:00 PM EST
            </p>
            <p>
              <strong>Returns:</strong> <a href="mailto:returns@alphamedicalcare.com" className="text-blue-600 hover:underline">returns@alphamedicalcare.com</a>
            </p>
          </div>
        </section>

        <div className="rounded-lg border border-blue-200 bg-blue-50 p-6">
          <p className="text-sm text-slate-700">
            <strong>Note:</strong> This shipping and returns policy is effective as of January 1, 2025. We reserve the right to update this policy at any time. Changes will be posted on this page with an updated effective date.
          </p>
        </div>
      </div>
    </div>
  );
}
