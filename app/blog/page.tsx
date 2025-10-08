import { supabase } from '@/lib/supabase';
import Link from 'next/link';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Calendar, Clock, ArrowRight } from 'lucide-react';

async function getBlogPosts() {
  const { data: posts } = await supabase
    .from('blog_posts')
    .select('*')
    .eq('published', true)
    .order('published_at', { ascending: false });

  return posts || [];
}

export default async function BlogPage() {
  const posts = await getBlogPosts();

  const staticPosts = [
    {
      id: 1,
      title: 'How to Relieve Lower Back Pain: A Comprehensive Guide',
      slug: 'how-to-relieve-lower-back-pain',
      excerpt: 'Discover effective methods and exercises to alleviate lower back pain and improve your quality of life. Learn from expert physiotherapists.',
      image: 'https://images.pexels.com/photos/6823567/pexels-photo-6823567.jpeg?auto=compress&cs=tinysrgb&w=800',
      category: 'Pain Management',
      author: 'Dr. Sarah Johnson',
      date: 'March 15, 2025',
      readTime: '8 min read'
    },
    {
      id: 2,
      title: 'The Benefits of Pressotherapy for Athletic Recovery',
      slug: 'benefits-of-pressotherapy-athletic-recovery',
      excerpt: 'Learn how pressotherapy boots can accelerate muscle recovery, reduce inflammation, and improve athletic performance.',
      image: 'https://images.pexels.com/photos/8172765/pexels-photo-8172765.jpeg?auto=compress&cs=tinysrgb&w=800',
      category: 'Recovery',
      author: 'Michael Chen',
      date: 'March 12, 2025',
      readTime: '6 min read'
    },
    {
      id: 3,
      title: 'Understanding Cervical Traction Therapy',
      slug: 'understanding-cervical-traction-therapy',
      excerpt: 'A detailed look at how cervical traction devices work and who can benefit from this non-invasive treatment approach.',
      image: 'https://images.pexels.com/photos/6823574/pexels-photo-6823574.jpeg?auto=compress&cs=tinysrgb&w=800',
      category: 'Treatment',
      author: 'Dr. Emily Roberts',
      date: 'March 10, 2025',
      readTime: '7 min read'
    },
    {
      id: 4,
      title: '5 Essential Exercises for Posture Correction',
      slug: '5-essential-exercises-posture-correction',
      excerpt: 'Simple yet effective exercises you can do at home to improve your posture and reduce neck and shoulder pain.',
      image: 'https://images.pexels.com/photos/6111619/pexels-photo-6111619.jpeg?auto=compress&cs=tinysrgb&w=800',
      category: 'Exercise',
      author: 'Dr. James Wilson',
      date: 'March 8, 2025',
      readTime: '5 min read'
    },
    {
      id: 5,
      title: 'The Science Behind LED Light Therapy for Skin',
      slug: 'science-behind-led-light-therapy-skin',
      excerpt: 'Explore how different wavelengths of LED light can rejuvenate skin, reduce wrinkles, and promote healing.',
      image: 'https://images.pexels.com/photos/3865618/pexels-photo-3865618.jpeg?auto=compress&cs=tinysrgb&w=800',
      category: 'Wellness',
      author: 'Dr. Lisa Anderson',
      date: 'March 5, 2025',
      readTime: '9 min read'
    },
    {
      id: 6,
      title: 'Knee Rehabilitation: From Injury to Full Recovery',
      slug: 'knee-rehabilitation-injury-to-recovery',
      excerpt: 'A step-by-step guide to knee rehabilitation, including exercises, equipment, and expert tips for optimal recovery.',
      image: 'https://images.pexels.com/photos/6823581/pexels-photo-6823581.jpeg?auto=compress&cs=tinysrgb&w=800',
      category: 'Rehabilitation',
      author: 'Dr. Mark Thompson',
      date: 'March 3, 2025',
      readTime: '10 min read'
    }
  ];

  const categories = ['All', 'Pain Management', 'Recovery', 'Treatment', 'Exercise', 'Wellness', 'Rehabilitation'];

  return (
    <div className="flex flex-col">
      <section className="bg-gradient-to-br from-blue-50 to-teal-50 py-16">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-3xl text-center">
            <h1 className="mb-4 text-4xl font-bold text-slate-900 md:text-5xl">
              Health & Wellness Blog
            </h1>
            <p className="text-lg text-slate-600">
              Expert insights, tips, and guides to help you on your journey to better health and recovery
            </p>
          </div>
        </div>
      </section>

      <section className="bg-white py-12">
        <div className="container mx-auto px-4">
          <div className="mb-8 flex flex-wrap gap-2 justify-center">
            {categories.map((category) => (
              <Button
                key={category}
                variant={category === 'All' ? 'default' : 'outline'}
                size="sm"
              >
                {category}
              </Button>
            ))}
          </div>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {(posts.length > 0 ? posts : staticPosts).map((post) => (
              <Link key={post.id} href={`/blog/${post.slug}`}>
                <Card className="group h-full overflow-hidden transition-all hover:shadow-lg">
                  <div className="relative aspect-[16/10] overflow-hidden">
                    <img
                      src={post.featured_image || post.image}
                      alt={post.title}
                      className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
                    />
                    <Badge className="absolute left-4 top-4 bg-blue-600">
                      Health Tips
                    </Badge>
                  </div>
                  <CardContent className="p-6">
                    <div className="mb-3 flex items-center gap-4 text-sm text-slate-500">
                      <div className="flex items-center gap-1">
                        <Calendar className="h-4 w-4" />
                        <span>{post.published_at ? new Date(post.published_at).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' }) : post.date}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Clock className="h-4 w-4" />
                        <span>{post.readTime || '5 min read'}</span>
                      </div>
                    </div>
                    <h3 className="mb-3 text-xl font-bold text-slate-900 line-clamp-2">
                      {post.title}
                    </h3>
                    <p className="mb-4 text-slate-600 line-clamp-3">{post.excerpt}</p>
                    <Button variant="ghost" size="sm" className="group-hover:text-blue-600">
                      Read More
                      <ArrowRight className="ml-1 h-4 w-4" />
                    </Button>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-gradient-to-br from-blue-600 to-teal-500 py-12 text-white">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="mb-4 text-3xl font-bold">Subscribe to Our Newsletter</h2>
            <p className="mb-6 text-blue-50">
              Get the latest health tips, product updates, and exclusive offers delivered to your inbox.
            </p>
            <div className="flex gap-2">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 rounded-lg px-4 py-3 text-slate-900"
              />
              <Button size="lg" variant="secondary">
                Subscribe
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
