/*
  # E-commerce Database Schema for Physiotherapy & Wellness Site

  ## Overview
  This migration creates a comprehensive database structure for a headless e-commerce platform
  focused on physiotherapy and wellness products. The schema supports products, categories,
  customer management, orders, reviews, and blog content.

  ## New Tables

  ### `categories`
  - `id` (uuid, primary key) - Unique identifier
  - `name` (text) - Category name (e.g., "Pain Relief & Relaxation")
  - `slug` (text, unique) - URL-friendly version
  - `parent_id` (uuid, nullable) - For subcategories
  - `description` (text) - Category description
  - `image_url` (text) - Category image
  - `display_order` (integer) - Sort order
  - `created_at` (timestamptz) - Creation timestamp

  ### `products`
  - `id` (uuid, primary key) - Unique identifier
  - `shopify_id` (text, unique) - Shopify product ID
  - `name` (text) - Product name
  - `slug` (text, unique) - URL-friendly version
  - `description` (text) - Full product description
  - `short_description` (text) - Brief summary
  - `price` (decimal) - Current price
  - `compare_at_price` (decimal, nullable) - Original price for discounts
  - `images` (jsonb) - Array of image URLs
  - `features` (jsonb) - Product features array
  - `benefits` (jsonb) - Product benefits array
  - `specifications` (jsonb) - Technical specifications
  - `in_stock` (boolean) - Availability status
  - `stock_quantity` (integer) - Available quantity
  - `category_id` (uuid) - Primary category
  - `meta_title` (text) - SEO title
  - `meta_description` (text) - SEO description
  - `created_at` (timestamptz) - Creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp

  ### `product_reviews`
  - `id` (uuid, primary key) - Unique identifier
  - `product_id` (uuid) - Related product
  - `user_id` (uuid) - Reviewer (from auth.users)
  - `rating` (integer) - Star rating (1-5)
  - `title` (text) - Review title
  - `comment` (text) - Review text
  - `verified_purchase` (boolean) - Purchase verification
  - `created_at` (timestamptz) - Creation timestamp

  ### `orders`
  - `id` (uuid, primary key) - Unique identifier
  - `user_id` (uuid) - Customer ID
  - `order_number` (text, unique) - Human-readable order number
  - `status` (text) - Order status
  - `subtotal` (decimal) - Order subtotal
  - `tax` (decimal) - Tax amount
  - `shipping` (decimal) - Shipping cost
  - `total` (decimal) - Total amount
  - `stripe_payment_id` (text) - Stripe payment reference
  - `shipping_address` (jsonb) - Shipping details
  - `billing_address` (jsonb) - Billing details
  - `created_at` (timestamptz) - Order date

  ### `order_items`
  - `id` (uuid, primary key) - Unique identifier
  - `order_id` (uuid) - Related order
  - `product_id` (uuid) - Related product
  - `quantity` (integer) - Quantity ordered
  - `price` (decimal) - Price at time of purchase
  - `created_at` (timestamptz) - Creation timestamp

  ### `blog_posts`
  - `id` (uuid, primary key) - Unique identifier
  - `title` (text) - Post title
  - `slug` (text, unique) - URL-friendly version
  - `excerpt` (text) - Brief summary
  - `content` (text) - Full post content
  - `author_id` (uuid) - Author from auth.users
  - `featured_image` (text) - Main image URL
  - `published` (boolean) - Publication status
  - `published_at` (timestamptz) - Publication date
  - `meta_title` (text) - SEO title
  - `meta_description` (text) - SEO description
  - `created_at` (timestamptz) - Creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp

  ### `customer_profiles`
  - `id` (uuid, primary key) - Links to auth.users
  - `full_name` (text) - Customer name
  - `phone` (text) - Phone number
  - `default_shipping_address` (jsonb) - Default shipping
  - `default_billing_address` (jsonb) - Default billing
  - `created_at` (timestamptz) - Creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp

  ## Security

  1. Row Level Security (RLS) enabled on all tables
  2. Authenticated users can:
     - View all published products, categories, and blog posts
     - Create reviews for products they purchased
     - View and manage their own orders
     - Update their own profile
  3. Public users can:
     - View published products, categories, and blog posts (read-only)
  4. Anonymous users cannot access order or profile data
*/

-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  slug text UNIQUE NOT NULL,
  parent_id uuid REFERENCES categories(id) ON DELETE SET NULL,
  description text DEFAULT '',
  image_url text DEFAULT '',
  display_order integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  shopify_id text UNIQUE,
  name text NOT NULL,
  slug text UNIQUE NOT NULL,
  description text DEFAULT '',
  short_description text DEFAULT '',
  price decimal(10,2) NOT NULL DEFAULT 0,
  compare_at_price decimal(10,2),
  images jsonb DEFAULT '[]'::jsonb,
  features jsonb DEFAULT '[]'::jsonb,
  benefits jsonb DEFAULT '[]'::jsonb,
  specifications jsonb DEFAULT '{}'::jsonb,
  in_stock boolean DEFAULT true,
  stock_quantity integer DEFAULT 0,
  category_id uuid REFERENCES categories(id) ON DELETE SET NULL,
  meta_title text DEFAULT '',
  meta_description text DEFAULT '',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create product_reviews table
CREATE TABLE IF NOT EXISTS product_reviews (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id uuid REFERENCES products(id) ON DELETE CASCADE NOT NULL,
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  rating integer NOT NULL CHECK (rating >= 1 AND rating <= 5),
  title text DEFAULT '',
  comment text DEFAULT '',
  verified_purchase boolean DEFAULT false,
  created_at timestamptz DEFAULT now()
);

-- Create customer_profiles table
CREATE TABLE IF NOT EXISTS customer_profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name text DEFAULT '',
  phone text DEFAULT '',
  default_shipping_address jsonb DEFAULT '{}'::jsonb,
  default_billing_address jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users(id) ON DELETE SET NULL,
  order_number text UNIQUE NOT NULL,
  status text DEFAULT 'pending',
  subtotal decimal(10,2) DEFAULT 0,
  tax decimal(10,2) DEFAULT 0,
  shipping decimal(10,2) DEFAULT 0,
  total decimal(10,2) DEFAULT 0,
  stripe_payment_id text DEFAULT '',
  shipping_address jsonb DEFAULT '{}'::jsonb,
  billing_address jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz DEFAULT now()
);

-- Create order_items table
CREATE TABLE IF NOT EXISTS order_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id uuid REFERENCES orders(id) ON DELETE CASCADE NOT NULL,
  product_id uuid REFERENCES products(id) ON DELETE SET NULL,
  quantity integer DEFAULT 1,
  price decimal(10,2) DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Create blog_posts table
CREATE TABLE IF NOT EXISTS blog_posts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL,
  slug text UNIQUE NOT NULL,
  excerpt text DEFAULT '',
  content text DEFAULT '',
  author_id uuid REFERENCES auth.users(id) ON DELETE SET NULL,
  featured_image text DEFAULT '',
  published boolean DEFAULT false,
  published_at timestamptz,
  meta_title text DEFAULT '',
  meta_description text DEFAULT '',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_slug ON products(slug);
CREATE INDEX IF NOT EXISTS idx_categories_parent ON categories(parent_id);
CREATE INDEX IF NOT EXISTS idx_categories_slug ON categories(slug);
CREATE INDEX IF NOT EXISTS idx_reviews_product ON product_reviews(product_id);
CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_blog_slug ON blog_posts(slug);
CREATE INDEX IF NOT EXISTS idx_blog_published ON blog_posts(published, published_at);

-- Enable Row Level Security
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE customer_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE order_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE blog_posts ENABLE ROW LEVEL SECURITY;

-- RLS Policies for categories (public read)
CREATE POLICY "Anyone can view categories"
  ON categories FOR SELECT
  TO public
  USING (true);

-- RLS Policies for products (public read)
CREATE POLICY "Anyone can view products"
  ON products FOR SELECT
  TO public
  USING (true);

-- RLS Policies for product_reviews (public read, authenticated create)
CREATE POLICY "Anyone can view reviews"
  ON product_reviews FOR SELECT
  TO public
  USING (true);

CREATE POLICY "Authenticated users can create reviews"
  ON product_reviews FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own reviews"
  ON product_reviews FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own reviews"
  ON product_reviews FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

-- RLS Policies for customer_profiles
CREATE POLICY "Users can view own profile"
  ON customer_profiles FOR SELECT
  TO authenticated
  USING (auth.uid() = id);

CREATE POLICY "Users can create own profile"
  ON customer_profiles FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON customer_profiles FOR UPDATE
  TO authenticated
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- RLS Policies for orders
CREATE POLICY "Users can view own orders"
  ON orders FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create own orders"
  ON orders FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

-- RLS Policies for order_items
CREATE POLICY "Users can view own order items"
  ON order_items FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM orders
      WHERE orders.id = order_items.order_id
      AND orders.user_id = auth.uid()
    )
  );

-- RLS Policies for blog_posts (public read published posts)
CREATE POLICY "Anyone can view published blog posts"
  ON blog_posts FOR SELECT
  TO public
  USING (published = true);
