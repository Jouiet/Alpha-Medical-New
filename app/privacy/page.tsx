import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Privacy Policy | Alpha Medical Care',
  description: 'Privacy Policy for Alpha Medical Care - How we collect, use, and protect your personal information',
};

export default function PrivacyPage() {
  return (
    <div className="container mx-auto px-4 py-12 max-w-4xl">
      <h1 className="mb-8 text-4xl font-bold text-slate-900">Privacy Policy</h1>

      <div className="space-y-8 text-slate-700">
        <section>
          <p className="mb-4 text-sm text-slate-500">
            <strong>Effective Date:</strong> January 1, 2025<br />
            <strong>Last Updated:</strong> January 1, 2025
          </p>

          <p className="mb-4">
            Alpha Medical Care ("we," "us," or "our") respects your privacy and is committed to protecting your personal information. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our website and use our services.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">1. Information We Collect</h2>

          <h3 className="mb-3 text-xl font-medium text-slate-800">1.1 Personal Information</h3>
          <p className="mb-4">
            We collect personal information that you voluntarily provide to us when you:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Create an account or place an order</li>
            <li>Subscribe to our newsletter</li>
            <li>Contact customer support</li>
            <li>Participate in surveys or promotions</li>
          </ul>
          <p className="mb-4">
            This information may include:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Name and contact information (email address, phone number, shipping address)</li>
            <li>Payment information (processed securely through Stripe)</li>
            <li>Order history and preferences</li>
            <li>Communication preferences</li>
          </ul>

          <h3 className="mb-3 text-xl font-medium text-slate-800">1.2 Automatically Collected Information</h3>
          <p className="mb-4">
            When you visit our website, we automatically collect certain information about your device and browsing behavior, including:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>IP address and browser type</li>
            <li>Operating system and device information</li>
            <li>Pages visited and time spent on our site</li>
            <li>Referring website addresses</li>
            <li>Cookies and similar tracking technologies</li>
          </ul>

          <h3 className="mb-3 text-xl font-medium text-slate-800">1.3 Health Information</h3>
          <p className="mb-4">
            We do not collect detailed health information or medical records. However, product purchases may indicate health-related interests. This information is treated with strict confidentiality and used only to improve our product offerings.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">2. How We Use Your Information</h2>
          <p className="mb-4">We use the information we collect to:</p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li><strong>Process and fulfill orders:</strong> Including payment processing, shipping, and customer service</li>
            <li><strong>Communicate with you:</strong> Send order confirmations, shipping updates, and respond to inquiries</li>
            <li><strong>Improve our services:</strong> Analyze usage patterns to enhance website functionality and user experience</li>
            <li><strong>Marketing:</strong> Send promotional emails about new products and special offers (with your consent)</li>
            <li><strong>Fraud prevention:</strong> Detect and prevent fraudulent transactions and protect against security threats</li>
            <li><strong>Legal compliance:</strong> Comply with applicable laws, regulations, and legal processes</li>
          </ul>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">3. Information Sharing and Disclosure</h2>
          <p className="mb-4">We do not sell your personal information. We may share your information with:</p>

          <h3 className="mb-3 text-xl font-medium text-slate-800">3.1 Service Providers</h3>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li><strong>Payment processors (Stripe):</strong> To process transactions securely</li>
            <li><strong>Shopify:</strong> For e-commerce platform services and order management</li>
            <li><strong>Shipping carriers:</strong> To deliver your orders</li>
            <li><strong>Email service providers:</strong> To send transactional and marketing emails</li>
            <li><strong>Analytics providers:</strong> To understand website usage and improve our services</li>
          </ul>

          <h3 className="mb-3 text-xl font-medium text-slate-800">3.2 Legal Requirements</h3>
          <p className="mb-4">
            We may disclose your information if required by law, court order, or governmental authority, or to protect our rights, property, or safety, or that of others.
          </p>

          <h3 className="mb-3 text-xl font-medium text-slate-800">3.3 Business Transfers</h3>
          <p className="mb-4">
            In the event of a merger, acquisition, or sale of assets, your information may be transferred to the acquiring entity.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">4. Data Security</h2>
          <p className="mb-4">
            We implement industry-standard security measures to protect your personal information:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>SSL/TLS encryption for data transmission</li>
            <li>PCI DSS compliant payment processing through Stripe</li>
            <li>Secure servers with regular security updates</li>
            <li>Access controls and authentication mechanisms</li>
            <li>Regular security audits and monitoring</li>
          </ul>
          <p className="mb-4">
            However, no method of transmission over the internet or electronic storage is 100% secure. While we strive to protect your information, we cannot guarantee absolute security.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">5. Cookies and Tracking Technologies</h2>
          <p className="mb-4">
            We use cookies and similar tracking technologies to enhance your browsing experience:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li><strong>Essential cookies:</strong> Required for website functionality (e.g., shopping cart)</li>
            <li><strong>Analytics cookies:</strong> Help us understand how visitors use our site</li>
            <li><strong>Marketing cookies:</strong> Used to deliver relevant advertisements</li>
          </ul>
          <p className="mb-4">
            You can control cookies through your browser settings. However, disabling cookies may affect website functionality.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">6. Your Privacy Rights</h2>
          <p className="mb-4">Depending on your location, you may have the following rights:</p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li><strong>Access:</strong> Request a copy of the personal information we hold about you</li>
            <li><strong>Correction:</strong> Request correction of inaccurate or incomplete information</li>
            <li><strong>Deletion:</strong> Request deletion of your personal information (subject to legal obligations)</li>
            <li><strong>Objection:</strong> Object to processing of your information for marketing purposes</li>
            <li><strong>Portability:</strong> Request transfer of your information to another service provider</li>
            <li><strong>Withdrawal of consent:</strong> Withdraw consent for data processing at any time</li>
          </ul>
          <p className="mb-4">
            To exercise these rights, please contact us at <a href="mailto:privacy@alphamedicalcare.com" className="text-blue-600 hover:underline">privacy@alphamedicalcare.com</a>.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">7. Data Retention</h2>
          <p className="mb-4">
            We retain your personal information for as long as necessary to:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Fulfill the purposes described in this Privacy Policy</li>
            <li>Comply with legal, accounting, or reporting requirements</li>
            <li>Resolve disputes and enforce our agreements</li>
          </ul>
          <p className="mb-4">
            After this period, we will securely delete or anonymize your information.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">8. Third-Party Links</h2>
          <p className="mb-4">
            Our website may contain links to third-party websites. We are not responsible for the privacy practices of these external sites. We encourage you to review their privacy policies before providing any personal information.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">9. Children's Privacy</h2>
          <p className="mb-4">
            Our services are not directed to individuals under the age of 18. We do not knowingly collect personal information from children. If you believe we have inadvertently collected information from a child, please contact us immediately.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">10. International Data Transfers</h2>
          <p className="mb-4">
            Your information may be transferred to and processed in countries other than your country of residence. These countries may have different data protection laws. By using our services, you consent to such transfers.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">11. Marketing Communications</h2>
          <p className="mb-4">
            With your consent, we may send you marketing emails about products, special offers, and promotions. You can opt out at any time by:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Clicking the "unsubscribe" link in any marketing email</li>
            <li>Updating your communication preferences in your account settings</li>
            <li>Contacting us at <a href="mailto:support@alphamedicalcare.com" className="text-blue-600 hover:underline">support@alphamedicalcare.com</a></li>
          </ul>
          <p className="mb-4">
            Note: You will still receive transactional emails related to your orders even if you opt out of marketing communications.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">12. Changes to This Privacy Policy</h2>
          <p className="mb-4">
            We may update this Privacy Policy from time to time to reflect changes in our practices or legal requirements. We will notify you of any material changes by:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Posting the updated policy on our website</li>
            <li>Updating the "Last Updated" date at the top of this page</li>
            <li>Sending you an email notification for significant changes</li>
          </ul>
          <p className="mb-4">
            Your continued use of our services after changes are posted constitutes acceptance of the updated Privacy Policy.
          </p>
        </section>

        <section>
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">13. Contact Us</h2>
          <p className="mb-4">
            If you have any questions, concerns, or requests regarding this Privacy Policy or our data practices, please contact us:
          </p>
          <div className="rounded-lg bg-slate-50 p-6">
            <p className="mb-2"><strong>Alpha Medical Care</strong></p>
            <p className="mb-2">Email: <a href="mailto:privacy@alphamedicalcare.com" className="text-blue-600 hover:underline">privacy@alphamedicalcare.com</a></p>
            <p className="mb-2">Phone: <a href="tel:+15551234567" className="text-blue-600 hover:underline">+1 (555) 123-4567</a></p>
            <p>Customer Support: <a href="mailto:support@alphamedicalcare.com" className="text-blue-600 hover:underline">support@alphamedicalcare.com</a></p>
          </div>
        </section>

        <section className="mt-12 border-t pt-8">
          <h2 className="mb-4 text-2xl font-semibold text-slate-900">Region-Specific Privacy Rights</h2>

          <h3 className="mb-3 text-xl font-medium text-slate-800">For California Residents (CCPA)</h3>
          <p className="mb-4">
            California residents have additional rights under the California Consumer Privacy Act (CCPA):
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Right to know what personal information is collected, used, shared, or sold</li>
            <li>Right to delete personal information</li>
            <li>Right to opt-out of the sale of personal information (we do not sell personal information)</li>
            <li>Right to non-discrimination for exercising CCPA rights</li>
          </ul>

          <h3 className="mb-3 text-xl font-medium text-slate-800">For European Union Residents (GDPR)</h3>
          <p className="mb-4">
            EU residents have rights under the General Data Protection Regulation (GDPR), including:
          </p>
          <ul className="mb-4 ml-6 list-disc space-y-2">
            <li>Right to access, rectification, and erasure</li>
            <li>Right to restriction of processing and data portability</li>
            <li>Right to object to processing</li>
            <li>Right to lodge a complaint with a supervisory authority</li>
          </ul>
        </section>

        <div className="mt-12 rounded-lg border border-blue-200 bg-blue-50 p-6">
          <p className="text-sm text-slate-700">
            <strong>Note:</strong> This Privacy Policy is designed to comply with applicable privacy laws including GDPR, CCPA, and other regional regulations. We are committed to protecting your privacy and maintaining transparency in our data practices.
          </p>
        </div>
      </div>
    </div>
  );
}
