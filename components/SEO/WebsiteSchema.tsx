interface WebsiteSchemaProps {
  name: string;
  url: string;
  description: string;
  searchUrl?: string;
}

export default function WebsiteSchema({ name, url, description, searchUrl }: WebsiteSchemaProps) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name,
    url,
    description,
    ...(searchUrl && {
      potentialAction: {
        '@type': 'SearchAction',
        target: {
          '@type': 'EntryPoint',
          urlTemplate: `${searchUrl}?q={search_term_string}`
        },
        'query-input': 'required name=search_term_string'
      }
    })
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
