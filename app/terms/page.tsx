import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Terms & Conditions | Alpha Medical Care',
  description: 'Terms and conditions for using Alpha Medical Care website and services',
};

export default function TermsPage() {
  return (
    <div className="container mx-auto px-4 py-12 max-w-4xl">
      <h1 className="mb-8 text-4xl font-bold text-slate-900">Terms & Conditions</h1>

      <div className="space-y-8 text-slate-700">
        <section>
          <p className="mb-4 text-sm text-slate-500">
            <strong>Effective Date:</strong> January 1, 2025<br />
            <strong>Last Updated:</strong> January 1, 2025
          </p>

          <p className="mb-4">
            Welcome to Alpha Medical Care. These Terms and Conditions ("Terms") govern your access to and use of our website, products, and services. By accessing or using our website, you agree to be bound by these Terms. If you do not agree to these Terms, please do not use our services.
          </p>

          <p className="mb-4">
            Please read these Terms carefully before making any purchase or using our services.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">1. Acceptance of Terms</h2>
          <p className="mb-4">
            By accessing or using the Alpha Medical Care website ("Website"), placing an order, or using our services, you:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Confirm that you are at least 18 years of age or have parental/guardian consent</li>
            <li>Agree to comply with these Terms and all applicable laws and regulations</li>
            <li>Accept our Privacy Policy, Shipping Policy, and Return Policy</li>
            <li>Consent to receive electronic communications from us</li>
          </ul>
          <p className="mb-4">
            We reserve the right to modify these Terms at any time. Your continued use of the Website after changes are posted constitutes acceptance of the modified Terms.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">2. Definitions</h2>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li><strong>"Alpha Medical Care," "we," "us," "our"</strong> refers to Alpha Medical Care and its affiliates</li>
            <li><strong>"You," "your," "customer"</strong> refers to the person or entity using our Website or services</li>
            <li><strong>"Products"</strong> refers to physiotherapy equipment, medical devices, and wellness products offered for sale</li>
            <li><strong>"Services"</strong> refers to all services provided through our Website including e-commerce functionality</li>
            <li><strong>"Website"</strong> refers to alphamedicalcare.com and all associated subdomains</li>
          </ul>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">3. Use of Website</h2>

          <h3 className="mb-3 text-xl font-medium text-slate-800">3.1 Permitted Use</h3>
          <p className="mb-4">You may use our Website for:</p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Browsing and purchasing products for personal or professional use</li>
            <li>Accessing product information and educational content</li>
            <li>Managing your account and orders</li>
            <li>Contacting customer support</li>
          </ul>

          <h3 className="mb-3 text-xl font-medium text-slate-800">3.2 Prohibited Use</h3>
          <p className="mb-4">You agree NOT to:</p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Use the Website for any unlawful purpose or in violation of these Terms</li>
            <li>Attempt to gain unauthorized access to our systems, accounts, or data</li>
            <li>Use automated systems (bots, scrapers) to access the Website without permission</li>
            <li>Copy, reproduce, or distribute Website content without authorization</li>
            <li>Post or transmit viruses, malware, or harmful code</li>
            <li>Impersonate another person or entity</li>
            <li>Interfere with or disrupt the Website's functionality</li>
            <li>Collect user information without consent</li>
            <li>Use products in a manner inconsistent with their intended purpose</li>
            <li>Resell products for commercial purposes without authorization</li>
          </ul>

          <h3 className="mb-3 text-xl font-medium text-slate-800">3.3 Account Registration</h3>
          <p className="mb-4">
            When creating an account, you agree to:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Provide accurate, current, and complete information</li>
            <li>Maintain and update your account information</li>
            <li>Maintain the security and confidentiality of your password</li>
            <li>Accept responsibility for all activities under your account</li>
            <li>Notify us immediately of any unauthorized access</li>
          </ul>
          <p className="mb-4">
            We reserve the right to suspend or terminate accounts that violate these Terms or engage in fraudulent activity.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">4. Products and Orders</h2>

          <h3 className="mb-3 text-xl font-medium text-slate-800">4.1 Product Information</h3>
          <p className="mb-4">
            We strive to provide accurate product descriptions, specifications, and images. However:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Product colors may vary slightly due to screen display differences</li>
            <li>We do not warrant that product descriptions are error-free or complete</li>
            <li>We reserve the right to correct errors or update product information at any time</li>
            <li>If a product is incorrectly described, we may refuse or cancel orders</li>
          </ul>

          <h3 className="mb-3 text-xl font-medium text-slate-800">4.2 Pricing</h3>
          <p className="mb-4">
            All prices are in U.S. dollars (USD) unless otherwise stated. We reserve the right to:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Change prices at any time without prior notice</li>
            <li>Correct pricing errors, even after an order is placed</li>
            <li>Refuse or cancel orders placed at incorrect prices</li>
          </ul>
          <p className="mb-4">
            Prices displayed do not include applicable taxes, shipping fees, or duties, which will be calculated at checkout.
          </p>

          <h3 className="mb-3 text-xl font-medium text-slate-800">4.3 Order Acceptance</h3>
          <p className="mb-4">
            Your receipt of an order confirmation does not constitute our acceptance of your order. We reserve the right to:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Accept or decline any order for any reason</li>
            <li>Limit quantities purchased per person or per order</li>
            <li>Refuse service to anyone</li>
            <li>Cancel orders that appear fraudulent or suspicious</li>
          </ul>
          <p className="mb-4">
            If we cancel your order after payment has been processed, we will issue a full refund to the original payment method.
          </p>

          <h3 className="mb-3 text-xl font-medium text-slate-800">4.4 Product Availability</h3>
          <p className="mb-4">
            Product availability is subject to change without notice. If a product becomes unavailable after you place an order, we will notify you and offer:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>A substitute product of equal or greater value</li>
            <li>A full refund to your original payment method</li>
            <li>A store credit for future purchases</li>
          </ul>

          <h3 className="mb-3 text-xl font-medium text-slate-800">4.5 Medical Device Disclaimer</h3>
          <div className="rounded-lg border border-amber-200 bg-amber-50 p-4">
            <p className="mb-2 text-amber-900">
              <strong>Important:</strong> Our products are designed for general wellness, pain relief, and rehabilitation support. They are not intended to diagnose, treat, cure, or prevent any disease or medical condition.
            </p>
            <ul className="ml-6 list-disc space-y-2 text-sm text-amber-800">
              <li>Always consult a healthcare professional before using our products, especially if you have pre-existing medical conditions</li>
              <li>Follow all product instructions and safety warnings</li>
              <li>Discontinue use and consult a doctor if you experience adverse effects</li>
              <li>These products are not a substitute for professional medical advice or treatment</li>
            </ul>
          </div>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">5. Payment</h2>

          <h3 className="mb-3 text-xl font-medium text-slate-800">5.1 Payment Methods</h3>
          <p className="mb-4">
            We accept payment through Stripe, which processes major credit cards, debit cards, and other payment methods. By providing payment information, you represent and warrant that:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>You are authorized to use the payment method</li>
            <li>The payment information provided is accurate and current</li>
            <li>You will pay all charges at the prices in effect when incurred</li>
            <li>You will pay applicable taxes</li>
          </ul>

          <h3 className="mb-3 text-xl font-medium text-slate-800">5.2 Payment Processing</h3>
          <p className="mb-4">
            Payment is processed at the time of order placement. Your payment information is securely processed by Stripe and subject to their terms of service. We do not store your complete payment card details on our servers.
          </p>

          <h3 className="mb-3 text-xl font-medium text-slate-800">5.3 Payment Disputes</h3>
          <p className="mb-4">
            If you dispute a charge, please contact us before initiating a chargeback with your payment provider. We will work with you to resolve any billing issues. Fraudulent chargebacks may result in account termination and legal action.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">6. Shipping and Delivery</h2>
          <p className="mb-4">
            Shipping terms are governed by our Shipping & Returns Policy. Key points:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Risk of loss passes to you upon delivery to the carrier</li>
            <li>Delivery dates are estimates and not guaranteed</li>
            <li>We are not liable for delays caused by carriers, customs, or force majeure events</li>
            <li>You are responsible for providing accurate shipping information</li>
          </ul>
          <p className="mb-4">
            For complete shipping information, see our <a href="/shipping" className="text-blue-600 hover:underline">Shipping & Returns Policy</a>.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">7. Returns and Refunds</h2>
          <p className="mb-4">
            Returns are subject to our 30-day return policy. See our <a href="/shipping" className="text-blue-600 hover:underline">Shipping & Returns Policy</a> for complete details.
          </p>
          <p className="mb-4">
            Refunds are processed within 5-7 business days of receiving and inspecting returned items. We reserve the right to refuse returns that do not meet our return criteria.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">8. Intellectual Property</h2>

          <h3 className="mb-3 text-xl font-medium text-slate-800">8.1 Our Rights</h3>
          <p className="mb-4">
            All content on this Website, including but not limited to:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Text, graphics, logos, images, and videos</li>
            <li>Product designs and descriptions</li>
            <li>Software, code, and functionality</li>
            <li>Trademarks, service marks, and trade names</li>
          </ul>
          <p className="mb-4">
            is the property of Alpha Medical Care or its licensors and is protected by U.S. and international copyright, trademark, and other intellectual property laws.
          </p>

          <h3 className="mb-3 text-xl font-medium text-slate-800">8.2 Limited License</h3>
          <p className="mb-4">
            We grant you a limited, non-exclusive, non-transferable license to access and use the Website for personal, non-commercial purposes. You may not:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Modify, copy, distribute, or create derivative works</li>
            <li>Reverse engineer or decompile any software</li>
            <li>Remove copyright or proprietary notices</li>
            <li>Use content for commercial purposes without written permission</li>
          </ul>

          <h3 className="mb-3 text-xl font-medium text-slate-800">8.3 Trademarks</h3>
          <p className="mb-4">
            "Alpha Medical Care" and our logo are trademarks of Alpha Medical Care. You may not use our trademarks without prior written consent.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">9. Privacy and Data Protection</h2>
          <p className="mb-4">
            Your privacy is important to us. Our collection, use, and protection of your personal information is governed by our <a href="/privacy" className="text-blue-600 hover:underline">Privacy Policy</a>, which is incorporated into these Terms by reference.
          </p>
          <p className="mb-4">
            By using our Website, you consent to our Privacy Policy and agree to our collection and use of information as described therein.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">10. Disclaimers and Limitations of Liability</h2>

          <h3 className="mb-3 text-xl font-medium text-slate-800">10.1 Website Disclaimer</h3>
          <div className="rounded-lg border border-slate-300 bg-slate-50 p-4">
            <p className="mb-2 text-sm font-semibold uppercase text-slate-900">
              THE WEBSITE AND ALL CONTENT, PRODUCTS, AND SERVICES ARE PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED.
            </p>
            <p className="text-sm text-slate-700">
              We disclaim all warranties, including but not limited to implied warranties of merchantability, fitness for a particular purpose, and non-infringement. We do not warrant that:
            </p>
            <ul className="mt-2 ml-6 list-disc space-y-1 text-sm text-slate-700">
              <li>The Website will be uninterrupted, secure, or error-free</li>
              <li>Defects will be corrected</li>
              <li>The Website is free of viruses or harmful components</li>
              <li>Results from using the Website will meet your requirements</li>
            </ul>
          </div>

          <h3 className="mb-3 mt-6 text-xl font-medium text-slate-800">10.2 Product Disclaimer</h3>
          <div className="rounded-lg border border-amber-200 bg-amber-50 p-4">
            <p className="mb-2 text-sm font-semibold text-amber-900">
              MEDICAL DISCLAIMER:
            </p>
            <ul className="ml-6 list-disc space-y-2 text-sm text-amber-800">
              <li>Our products are for general wellness and therapeutic support</li>
              <li>They are not intended to diagnose, treat, cure, or prevent disease</li>
              <li>Results may vary from person to person</li>
              <li>Always consult a healthcare professional before use</li>
              <li>We are not liable for misuse, improper use, or failure to follow instructions</li>
            </ul>
          </div>

          <h3 className="mb-3 mt-6 text-xl font-medium text-slate-800">10.3 Limitation of Liability</h3>
          <div className="rounded-lg border border-red-300 bg-red-50 p-4">
            <p className="mb-2 text-sm font-semibold uppercase text-red-900">
              TO THE MAXIMUM EXTENT PERMITTED BY LAW:
            </p>
            <p className="mb-2 text-sm text-red-800">
              Alpha Medical Care and its officers, directors, employees, agents, and affiliates shall not be liable for any indirect, incidental, special, consequential, or punitive damages, including but not limited to:
            </p>
            <ul className="ml-6 list-disc space-y-1 text-sm text-red-800">
              <li>Loss of profits, revenue, data, or use</li>
              <li>Personal injury or property damage</li>
              <li>Business interruption</li>
              <li>Any other pecuniary loss</li>
            </ul>
            <p className="mt-2 text-sm text-red-800">
              Our total liability for any claim arising from your use of the Website or purchase of products shall not exceed the amount you paid for the product(s) in question, or $100, whichever is greater.
            </p>
          </div>

          <h3 className="mb-3 mt-6 text-xl font-medium text-slate-800">10.4 Indemnification</h3>
          <p className="mb-4">
            You agree to indemnify, defend, and hold harmless Alpha Medical Care and its affiliates from any claims, damages, losses, liabilities, and expenses (including legal fees) arising from:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Your violation of these Terms</li>
            <li>Your use or misuse of products</li>
            <li>Your violation of any third-party rights</li>
            <li>Your fraudulent or illegal activities</li>
          </ul>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">11. Dispute Resolution</h2>

          <h3 className="mb-3 text-xl font-medium text-slate-800">11.1 Informal Resolution</h3>
          <p className="mb-4">
            Before initiating formal legal proceedings, you agree to contact us at <a href="mailto:legal@alphamedicalcare.com" className="text-blue-600 hover:underline">legal@alphamedicalcare.com</a> to attempt to resolve any dispute informally. We will work in good faith to resolve disputes within 30 days.
          </p>

          <h3 className="mb-3 text-xl font-medium text-slate-800">11.2 Arbitration Agreement</h3>
          <p className="mb-4">
            If informal resolution fails, you agree that any dispute shall be resolved through binding arbitration in accordance with the American Arbitration Association (AAA) rules. The arbitration shall take place in [Your State/City], and judgment on the award may be entered in any court having jurisdiction.
          </p>
          <p className="mb-4">
            <strong>Class Action Waiver:</strong> You agree to bring claims only in your individual capacity and not as part of any class action or representative proceeding.
          </p>

          <h3 className="mb-3 text-xl font-medium text-slate-800">11.3 Governing Law</h3>
          <p className="mb-4">
            These Terms shall be governed by and construed in accordance with the laws of the United States and the State of [Your State], without regard to conflict of law principles.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">12. Termination</h2>
          <p className="mb-4">
            We reserve the right to suspend or terminate your access to the Website and services at any time, without prior notice, for:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Violation of these Terms</li>
            <li>Fraudulent or illegal activity</li>
            <li>Requests by law enforcement or government agencies</li>
            <li>Unexpected technical issues</li>
            <li>Extended periods of inactivity</li>
          </ul>
          <p className="mb-4">
            Upon termination, your right to use the Website immediately ceases. We may delete your account and all associated data. Termination does not relieve you of obligations incurred prior to termination.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">13. Third-Party Services</h2>
          <p className="mb-4">
            Our Website integrates with third-party services including:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li><strong>Shopify:</strong> E-commerce platform and order management</li>
            <li><strong>Stripe:</strong> Payment processing</li>
            <li>Other service providers for analytics, marketing, and support</li>
          </ul>
          <p className="mb-4">
            These third-party services have their own terms and privacy policies. We are not responsible for third-party content, services, or practices. Your use of third-party services is at your own risk.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">14. Force Majeure</h2>
          <p className="mb-4">
            We shall not be liable for any failure or delay in performance due to circumstances beyond our reasonable control, including but not limited to:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Acts of God, natural disasters, pandemics</li>
            <li>War, terrorism, civil unrest</li>
            <li>Government actions or regulations</li>
            <li>Strikes, labor disputes</li>
            <li>Supply chain disruptions</li>
            <li>Internet or telecommunications failures</li>
          </ul>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">15. Severability</h2>
          <p className="mb-4">
            If any provision of these Terms is found to be invalid, illegal, or unenforceable, the remaining provisions shall continue in full force and effect. The invalid provision shall be modified to the minimum extent necessary to make it valid and enforceable.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">16. Entire Agreement</h2>
          <p className="mb-4">
            These Terms, together with our Privacy Policy and Shipping & Returns Policy, constitute the entire agreement between you and Alpha Medical Care regarding the use of the Website and services, superseding any prior agreements or understandings.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">17. Updates to Terms</h2>
          <p className="mb-4">
            We reserve the right to modify these Terms at any time. Changes will be effective immediately upon posting to the Website. We will update the "Last Updated" date at the top of this page.
          </p>
          <p className="mb-4">
            Material changes will be communicated via email or prominent notice on the Website. Your continued use of the Website after changes are posted constitutes acceptance of the modified Terms.
          </p>
          <p className="mb-4">
            We encourage you to review these Terms periodically to stay informed of any updates.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">18. Contact Information</h2>
          <p className="mb-4">
            If you have questions or concerns about these Terms, please contact us:
          </p>
          <div className="rounded-lg bg-slate-50 p-6 border border-slate-200">
            <p className="mb-2"><strong>Alpha Medical Care</strong></p>
            <p className="mb-2"><strong>Legal Department</strong></p>
            <p className="mb-2">Email: <a href="mailto:legal@alphamedicalcare.com" className="text-blue-600 hover:underline">legal@alphamedicalcare.com</a></p>
            <p className="mb-2">Customer Support: <a href="mailto:support@alphamedicalcare.com" className="text-blue-600 hover:underline">support@alphamedicalcare.com</a></p>
            <p>Phone: <a href="tel:+15551234567" className="text-blue-600 hover:underline">+1 (555) 123-4567</a></p>
          </div>
        </section>

        <div className="mt-12 rounded-lg border border-blue-200 bg-blue-50 p-6">
          <p className="mb-3 text-sm font-semibold text-blue-900">
            By using Alpha Medical Care's website and services, you acknowledge that you have read, understood, and agree to be bound by these Terms and Conditions.
          </p>
          <p className="text-sm text-blue-800">
            If you do not agree to these Terms, please discontinue use of our Website immediately.
          </p>
        </div>
      </div>
    </div>
  );
}
