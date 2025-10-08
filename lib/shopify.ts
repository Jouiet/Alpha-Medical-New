const domain = process.env.NEXT_PUBLIC_SHOPIFY_STORE_DOMAIN;
const storefrontAccessToken = process.env.NEXT_PUBLIC_SHOPIFY_STOREFRONT_ACCESS_TOKEN;

async function ShopifyData(query: string, variables = {}) {
  const URL = `https://${domain}/api/2024-01/graphql.json`;

  const options = {
    method: 'POST',
    headers: {
      'X-Shopify-Storefront-Access-Token': storefrontAccessToken!,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query, variables }),
  };

  try {
    const response = await fetch(URL, options);
    return await response.json();
  } catch (error) {
    throw new Error('Products not fetched');
  }
}

export async function getProductsInCollection() {
  const query = `
    {
      products(first: 25) {
        edges {
          node {
            id
            title
            handle
            description
            priceRange {
              minVariantPrice {
                amount
                currencyCode
              }
            }
            images(first: 5) {
              edges {
                node {
                  url
                  altText
                }
              }
            }
          }
        }
      }
    }
  `;

  const response = await ShopifyData(query);
  return response.data.products.edges ? response.data.products.edges : [];
}

export async function getProduct(handle: string) {
  const query = `
    query getProduct($handle: String!) {
      productByHandle(handle: $handle) {
        id
        title
        handle
        description
        priceRange {
          minVariantPrice {
            amount
            currencyCode
          }
        }
        images(first: 10) {
          edges {
            node {
              url
              altText
            }
          }
        }
        variants(first: 25) {
          edges {
            node {
              id
              title
              quantityAvailable
              priceV2 {
                amount
                currencyCode
              }
            }
          }
        }
      }
    }
  `;

  const response = await ShopifyData(query, { handle });
  return response.data.productByHandle ? response.data.productByHandle : {};
}

export async function createCheckout(lineItems: any[]) {
  const query = `
    mutation checkoutCreate($input: CheckoutCreateInput!) {
      checkoutCreate(input: $input) {
        checkout {
          id
          webUrl
        }
      }
    }
  `;

  const variables = {
    input: {
      lineItems,
    },
  };

  const response = await ShopifyData(query, variables);
  return response.data.checkoutCreate.checkout ? response.data.checkoutCreate.checkout : {};
}

export async function updateCheckout(checkoutId: string, lineItems: any[]) {
  const query = `
    mutation checkoutLineItemsReplace($checkoutId: ID!, $lineItems: [CheckoutLineItemInput!]!) {
      checkoutLineItemsReplace(checkoutId: $checkoutId, lineItems: $lineItems) {
        checkout {
          id
          webUrl
        }
      }
    }
  `;

  const variables = {
    checkoutId,
    lineItems,
  };

  const response = await ShopifyData(query, variables);
  return response.data.checkoutLineItemsReplace.checkout;
}
