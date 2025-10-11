interface OrganizationSchemaProps {
  name: string;
  url: string;
  logo: string;
  description: string;
  contactPoint?: {
    telephone: string;
    contactType: string;
    email?: string;
  };
  address?: {
    streetAddress: string;
    addressLocality: string;
    addressRegion: string;
    postalCode: string;
    addressCountry: string;
  };
  sameAs?: string[]; // Social media profiles
}

export default function OrganizationSchema({
  name,
  url,
  logo,
  description,
  contactPoint,
  address,
  sameAs = []
}: OrganizationSchemaProps) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name,
    url,
    logo: {
      '@type': 'ImageObject',
      url: logo
    },
    description,
    ...(contactPoint && {
      contactPoint: {
        '@type': 'ContactPoint',
        telephone: contactPoint.telephone,
        contactType: contactPoint.contactType,
        ...(contactPoint.email && { email: contactPoint.email })
      }
    }),
    ...(address && {
      address: {
        '@type': 'PostalAddress',
        streetAddress: address.streetAddress,
        addressLocality: address.addressLocality,
        addressRegion: address.addressRegion,
        postalCode: address.postalCode,
        addressCountry: address.addressCountry
      }
    }),
    ...(sameAs.length > 0 && { sameAs })
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
