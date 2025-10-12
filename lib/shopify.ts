/**
 * Shopify Storefront API Integration
 * Updated to use 2025-10 API and Cart API (replaces deprecated Checkout API)
 * Documentation: https://shopify.dev/docs/api/storefront
 */

const domain = process.env.NEXT_PUBLIC_SHOPIFY_STORE_DOMAIN;
const storefrontAccessToken = process.env.NEXT_PUBLIC_SHOPIFY_STOREFRONT_ACCESS_TOKEN;

async function ShopifyData(query: string, variables = {}) {
  const URL = `https://${domain}/api/2025-10/graphql.json`;

  if (!domain || !storefrontAccessToken) {
    console.warn('Shopify credentials missing. Using placeholder data.');
    return { data: null, errors: ['Missing credentials'] };
  }

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
    const json = await response.json();

    if (json.errors) {
      console.error('Shopify API errors:', json.errors);
    }

    return json;
  } catch (error) {
    console.error('Shopify fetch error:', error);
    throw new Error('Failed to fetch from Shopify');
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

/**
 * Create a new shopping cart
 * Replaces the deprecated createCheckout function
 */
export async function createCart() {
  const query = `
    mutation CreateCart {
      cartCreate {
        cart {
          id
          checkoutUrl
          lines(first: 100) {
            edges {
              node {
                id
                quantity
                merchandise {
                  ... on ProductVariant {
                    id
                  }
                }
              }
            }
          }
          cost {
            totalAmount {
              amount
              currencyCode
            }
          }
        }
        userErrors {
          field
          message
        }
      }
    }
  `;

  const response = await ShopifyData(query);

  if (response.data?.cartCreate?.userErrors?.length > 0) {
    console.error('Cart creation errors:', response.data.cartCreate.userErrors);
  }

  return response.data?.cartCreate?.cart || {};
}

/**
 * Add items to an existing cart
 */
export async function addToCart(cartId: string, merchandiseId: string, quantity: number = 1) {
  const query = `
    mutation AddToCart($cartId: ID!, $lines: [CartLineInput!]!) {
      cartLinesAdd(cartId: $cartId, lines: $lines) {
        cart {
          id
          checkoutUrl
          lines(first: 100) {
            edges {
              node {
                id
                quantity
                merchandise {
                  ... on ProductVariant {
                    id
                    title
                    priceV2 {
                      amount
                      currencyCode
                    }
                    product {
                      title
                      handle
                      images(first: 1) {
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
            }
          }
          cost {
            totalAmount {
              amount
              currencyCode
            }
            subtotalAmount {
              amount
              currencyCode
            }
          }
        }
        userErrors {
          field
          message
        }
      }
    }
  `;

  const variables = {
    cartId,
    lines: [{ merchandiseId, quantity }],
  };

  const response = await ShopifyData(query, variables);

  if (response.data?.cartLinesAdd?.userErrors?.length > 0) {
    console.error('Add to cart errors:', response.data.cartLinesAdd.userErrors);
  }

  return response.data?.cartLinesAdd?.cart || {};
}

/**
 * Update cart line quantity
 */
export async function updateCartLine(cartId: string, lineId: string, quantity: number) {
  const query = `
    mutation UpdateCartLine($cartId: ID!, $lines: [CartLineUpdateInput!]!) {
      cartLinesUpdate(cartId: $cartId, lines: $lines) {
        cart {
          id
          checkoutUrl
          lines(first: 100) {
            edges {
              node {
                id
                quantity
                merchandise {
                  ... on ProductVariant {
                    id
                  }
                }
              }
            }
          }
          cost {
            totalAmount {
              amount
              currencyCode
            }
          }
        }
        userErrors {
          field
          message
        }
      }
    }
  `;

  const variables = {
    cartId,
    lines: [{ id: lineId, quantity }],
  };

  const response = await ShopifyData(query, variables);

  if (response.data?.cartLinesUpdate?.userErrors?.length > 0) {
    console.error('Update cart errors:', response.data.cartLinesUpdate.userErrors);
  }

  return response.data?.cartLinesUpdate?.cart || {};
}

/**
 * Remove item from cart
 */
export async function removeFromCart(cartId: string, lineId: string) {
  const query = `
    mutation RemoveFromCart($cartId: ID!, $lineIds: [ID!]!) {
      cartLinesRemove(cartId: $cartId, lineIds: $lineIds) {
        cart {
          id
          checkoutUrl
          lines(first: 100) {
            edges {
              node {
                id
                quantity
                merchandise {
                  ... on ProductVariant {
                    id
                  }
                }
              }
            }
          }
          cost {
            totalAmount {
              amount
              currencyCode
            }
          }
        }
        userErrors {
          field
          message
        }
      }
    }
  `;

  const variables = {
    cartId,
    lineIds: [lineId],
  };

  const response = await ShopifyData(query, variables);

  if (response.data?.cartLinesRemove?.userErrors?.length > 0) {
    console.error('Remove from cart errors:', response.data.cartLinesRemove.userErrors);
  }

  return response.data?.cartLinesRemove?.cart || {};
}

/**
 * Get cart by ID
 */
export async function getCart(cartId: string) {
  const query = `
    query GetCart($cartId: ID!) {
      cart(id: $cartId) {
        id
        checkoutUrl
        lines(first: 100) {
          edges {
            node {
              id
              quantity
              merchandise {
                ... on ProductVariant {
                  id
                  title
                  priceV2 {
                    amount
                    currencyCode
                  }
                  product {
                    title
                    handle
                    images(first: 1) {
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
          }
        }
        cost {
          totalAmount {
            amount
            currencyCode
          }
          subtotalAmount {
            amount
            currencyCode
          }
        }
      }
    }
  `;

  const response = await ShopifyData(query, { cartId });
  return response.data?.cart || {};
}

/**
 * Get all collections
 */
export async function getAllCollections(limit = 50) {
  const query = `
    query GetCollections($limit: Int!) {
      collections(first: $limit) {
        edges {
          node {
            id
            title
            handle
            description
            image {
              url
              altText
            }
          }
        }
      }
    }
  `;

  const response = await ShopifyData(query, { limit });
  return response.data?.collections?.edges || [];
}

/**
 * Get products by collection handle
 */
export async function getProductsByCollection(collectionHandle: string, limit = 50) {
  const query = `
    query GetProductsByCollection($handle: String!, $limit: Int!) {
      collection(handle: $handle) {
        id
        title
        products(first: $limit) {
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
              images(first: 1) {
                edges {
                  node {
                    url
                    altText
                  }
                }
              }
              availableForSale
            }
          }
        }
      }
    }
  `;

  const response = await ShopifyData(query, { handle: collectionHandle, limit });
  return response.data?.collection?.products?.edges || [];
}

/**
 * Search products by query
 */
export async function searchProducts(searchQuery: string, limit = 20) {
  const query = `
    query SearchProducts($query: String!, $limit: Int!) {
      products(first: $limit, query: $query) {
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
            images(first: 1) {
              edges {
                node {
                  url
                  altText
                }
              }
            }
            availableForSale
          }
        }
      }
    }
  `;

  const response = await ShopifyData(query, { query: searchQuery, limit });
  return response.data?.products?.edges || [];
}
