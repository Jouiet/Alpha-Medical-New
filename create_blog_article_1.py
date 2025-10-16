#!/usr/bin/env python3
"""Create blog article: Heat vs Cold Therapy"""

import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env.admin')

SHOPIFY_STORE_DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN")
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN")

REST_URL = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-10"

headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN
}

# Article content
title = "When to Use Heat vs Cold Therapy for Pain Relief: Evidence-Based Guide 2026"
author = "Alpha Medical Care"
handle = "heat-vs-cold-therapy-pain-relief-guide-2026"
tags = "pain relief, heat therapy, cold therapy, recovery, injury treatment, inflammation, muscle pain"

# Create comprehensive HTML content (~2,200 words)
body_html = """
<div class="article-content">

<p>Whether you're dealing with a sports injury, chronic pain, or post-workout soreness, choosing between heat and cold therapy can significantly impact your recovery. This evidence-based guide will help you make the right choice for faster, more effective pain relief.</p>

<h2>Understanding Heat and Cold Therapy Basics</h2>

<p>Heat and cold therapy—also called thermotherapy and cryotherapy—are two of the most accessible and effective pain management techniques available. Both methods work by affecting blood flow, inflammation, and nerve signals, but they achieve these effects in opposite ways.</p>

<h3>How Heat Therapy Works</h3>

<p>Heat therapy increases blood circulation to the affected area, relaxing muscles and improving flexibility. When applied to painful areas, heat stimulates thermoreceptors in the skin, which can help block pain signals from reaching the brain. This increased blood flow delivers more oxygen and nutrients to damaged tissues, accelerating the healing process.</p>

<p>Heat causes vasodilation—the widening of blood vessels—which helps flush out metabolic waste products like lactic acid that contribute to muscle soreness and stiffness. This makes heat therapy particularly effective for chronic conditions and muscle tension.</p>

<h3>How Cold Therapy Works</h3>

<p>Cold therapy works through vasoconstriction—narrowing blood vessels to reduce blood flow to the affected area. This process decreases inflammation, swelling, and tissue damage. Cold also numbs nerve endings, providing immediate pain relief and slowing down the transmission of pain signals.</p>

<p>The reduction in metabolic activity caused by cold therapy helps prevent secondary tissue damage that can occur after an initial injury. This is why cold therapy is the go-to treatment immediately following acute injuries.</p>

<h2>When to Use Cold Therapy (Cryotherapy)</h2>

<h3>Acute Injuries (First 48-72 Hours)</h3>

<p><strong>Best for:</strong> Sprains, strains, bumps, bruises, and any injury causing swelling</p>

<p>Cold therapy is your first line of defense for acute injuries. The standard protocol, often called RICE (Rest, Ice, Compression, Elevation), includes cold therapy as a critical component. Apply cold within the first 15-30 minutes after injury for maximum benefit.</p>

<p><strong>How to apply:</strong></p>
<ul>
<li>Apply cold for 15-20 minutes at a time</li>
<li>Wait at least 45-60 minutes between applications</li>
<li>Continue for the first 2-3 days after injury</li>
<li>Use a thin towel between the cold source and skin to prevent ice burns</li>
</ul>

<h3>Post-Exercise Recovery</h3>

<p><strong>Best for:</strong> Reducing inflammation after intense workouts, preventing delayed onset muscle soreness (DOMS)</p>

<p>Athletes frequently use cold therapy immediately after training or competition to minimize inflammation and speed recovery. Ice baths and cold compression wraps are popular among professional athletes for this purpose.</p>

<p>Research shows that cold therapy applied within 30 minutes post-exercise can significantly reduce muscle soreness and accelerate recovery time. A 2016 study in the Journal of Athletic Training found that cold water immersion reduced perceived muscle soreness by 20% compared to passive recovery.</p>

<h3>Inflammatory Conditions</h3>

<p><strong>Best for:</strong> Arthritis flares, bursitis, tendinitis, gout attacks</p>

<p>Cold therapy can provide significant relief during acute inflammatory episodes. For conditions like rheumatoid arthritis or gout, cold helps reduce swelling and numb sharp pain during flare-ups.</p>

<p><strong>Important note:</strong> While cold helps during acute inflammatory episodes, some chronic arthritis sufferers find heat more beneficial between flare-ups. Individual response varies, so pay attention to what works best for your body.</p>

<h3>Migraine and Headache Relief</h3>

<p><strong>Best for:</strong> Migraines, tension headaches, sinus headaches</p>

<p>Applying cold packs to the forehead, temples, or back of the neck can provide rapid relief for many headache sufferers. The cold constricts blood vessels and reduces inflammation that contributes to headache pain.</p>

<h2>When to Use Heat Therapy (Thermotherapy)</h2>

<h3>Chronic Pain and Stiffness</h3>

<p><strong>Best for:</strong> Chronic back pain, osteoarthritis, fibromyalgia, old injuries</p>

<p>Heat therapy excels at managing long-term pain conditions. The increased blood flow helps relax tight muscles and improve joint mobility. A 2006 study published in Spine found that continuous low-level heat wrap therapy was more effective than oral analgesics for chronic lower back pain.</p>

<p><strong>How to apply:</strong></p>
<ul>
<li>Apply heat for 15-20 minutes at a time</li>
<li>Can be repeated every 2-3 hours as needed</li>
<li>Never apply heat directly on bare skin</li>
<li>Never sleep with a heating pad on</li>
</ul>

<h3>Muscle Tension and Spasms</h3>

<p><strong>Best for:</strong> Muscle knots, spasms, tight muscles from stress or overuse</p>

<p>Heat is highly effective for relaxing tense muscles and relieving spasms. The warmth increases tissue elasticity and decreases joint stiffness, making it easier to stretch and move without pain.</p>

<p>Neck and shoulder tension—common among office workers—responds particularly well to heat therapy. Combining heat with gentle stretching can provide even better results.</p>

<h3>Pre-Exercise Warm-Up</h3>

<p><strong>Best for:</strong> Preparing stiff joints and tight muscles before physical activity</p>

<p>Applying heat before exercise can improve flexibility and reduce injury risk, especially for individuals with chronic stiffness or limited mobility. Heat increases tissue temperature, making muscles more pliable and receptive to stretching.</p>

<p><strong>Pro tip:</strong> Combine heat therapy with dynamic stretching for optimal pre-exercise preparation. This combination can improve range of motion by up to 15% compared to stretching alone.</p>

<h3>Menstrual Cramps and Abdominal Pain</h3>

<p><strong>Best for:</strong> Period pain, digestive cramping, abdominal muscle tension</p>

<p>Heat therapy is one of the most effective non-pharmacological treatments for menstrual cramps. A 2014 study in Evidence-Based Nursing confirmed that heat therapy was as effective as ibuprofen for menstrual pain relief.</p>

<h2>Conditions That Benefit from Contrast Therapy</h2>

<p>Contrast therapy—alternating between heat and cold—combines the benefits of both modalities. This technique is particularly effective for certain conditions:</p>

<h3>Subacute Injuries (3-7 Days Post-Injury)</h3>

<p>Once initial swelling has subsided, contrast therapy can accelerate healing. Start with cold (constricts blood vessels), then switch to heat (dilates blood vessels), creating a pumping action that helps remove waste products and deliver nutrients.</p>

<p><strong>Protocol:</strong></p>
<ul>
<li>3 minutes cold therapy</li>
<li>1 minute heat therapy</li>
<li>Repeat cycle 3-4 times</li>
<li>Always end with cold</li>
</ul>

<h3>Chronic Repetitive Strain Injuries</h3>

<p>Conditions like tennis elbow, carpal tunnel syndrome, and plantar fasciitis may benefit from contrast therapy, especially when combined with targeted exercises and rest.</p>

<h2>When NOT to Use Heat or Cold Therapy</h2>

<h3>Avoid Cold Therapy If:</h3>

<ul>
<li><strong>You have circulatory problems:</strong> Raynaud's disease, peripheral vascular disease, or diabetes with nerve damage</li>
<li><strong>You have cold sensitivity:</strong> Cold urticaria (cold allergy) or hypersensitivity</li>
<li><strong>On open wounds:</strong> Cold can impair healing of open injuries</li>
<li><strong>Before physical activity:</strong> Cold can reduce muscle performance and increase injury risk</li>
</ul>

<h3>Avoid Heat Therapy If:</h3>

<ul>
<li><strong>You have acute inflammation:</strong> Fresh injuries with swelling should never receive heat</li>
<li><strong>You have poor sensation:</strong> Diabetes-related neuropathy or nerve damage increases burn risk</li>
<li><strong>You have dermatitis or open wounds:</strong> Heat can worsen skin conditions and impair wound healing</li>
<li><strong>You're pregnant:</strong> Avoid prolonged heat application to the abdomen, especially in the first trimester</li>
<li><strong>You have certain conditions:</strong> Deep vein thrombosis, multiple sclerosis (heat can worsen symptoms), or malignant tumors</li>
</ul>

<h2>Choosing the Right Application Method</h2>

<h3>Cold Therapy Options</h3>

<ul>
<li><strong>Ice packs:</strong> Convenient, reusable, good for most applications</li>
<li><strong>Cold gel packs:</strong> Stay flexible when frozen, conform better to body contours</li>
<li><strong>Cold compression wraps:</strong> Combine cold and compression for maximum effect (best for acute injuries)</li>
<li><strong>Ice massage:</strong> Direct ice application for small, specific areas like trigger points</li>
<li><strong>Cold therapy machines:</strong> Professional-grade continuous cold therapy for post-surgical recovery</li>
</ul>

<h3>Heat Therapy Options</h3>

<ul>
<li><strong>Heating pads:</strong> Consistent, controlled temperature; good for large areas</li>
<li><strong>Heat wraps:</strong> Portable, disposable, provide continuous low-level heat for up to 12 hours</li>
<li><strong>Hot water bottles:</strong> Inexpensive, moldable to body contours</li>
<li><strong>Moist heat packs:</strong> Penetrate deeper than dry heat; excellent for muscle tension</li>
<li><strong>Warm baths:</strong> Full-body heat therapy; add Epsom salts for additional muscle relaxation</li>
</ul>

<h2>Evidence-Based Application Guidelines</h2>

<h3>Temperature Safety</h3>

<p><strong>Cold therapy:</strong> 50-60°F (10-15°C) is ideal. Below 40°F (4°C) increases frostbite risk.</p>

<p><strong>Heat therapy:</strong> 104-113°F (40-45°C) is safe and effective. Never exceed 120°F (49°C) to prevent burns.</p>

<h3>Duration and Frequency</h3>

<p><strong>Standard protocol:</strong> 15-20 minutes per session is optimal for most conditions. Longer applications don't necessarily provide better results and may increase risk of tissue damage.</p>

<p><strong>Frequency:</strong> Heat can be applied every 2-3 hours as needed. Cold therapy should include 45-60 minute breaks between applications to prevent cold-related tissue damage.</p>

<h2>Professional Medical Devices vs. Home Remedies</h2>

<p>While DIY cold packs (frozen vegetables) and hot water bottles can provide relief, professional-grade therapy devices offer significant advantages:</p>

<ul>
<li><strong>Consistent temperature control:</strong> Reduces risk of burns or cold injury</li>
<li><strong>Better contour fit:</strong> Ensures optimal contact with affected areas</li>
<li><strong>Compression integration:</strong> Many professional devices combine compression with temperature therapy</li>
<li><strong>Longer-lasting relief:</strong> Medical-grade devices maintain therapeutic temperatures longer</li>
<li><strong>Convenience and reusability:</strong> Durable, easy to use, and cost-effective long-term</li>
</ul>

<h2>Combining Therapy with Other Pain Management Strategies</h2>

<p>For optimal results, combine heat or cold therapy with:</p>

<ul>
<li><strong>Appropriate rest:</strong> Allow injured tissues time to heal</li>
<li><strong>Gentle movement:</strong> Light activity prevents stiffness without causing further injury</li>
<li><strong>Proper support:</strong> Braces, wraps, or kinesiology tape can stabilize injured areas</li>
<li><strong>Physical therapy exercises:</strong> Targeted stretching and strengthening accelerate recovery</li>
<li><strong>Anti-inflammatory diet:</strong> Nutrition plays a crucial role in healing and pain management</li>
</ul>

<h2>When to See a Healthcare Provider</h2>

<p>Seek professional medical attention if:</p>

<ul>
<li>Pain persists beyond 2 weeks despite home treatment</li>
<li>Swelling doesn't improve after 48-72 hours</li>
<li>You experience numbness, tingling, or color changes in the affected area</li>
<li>Pain is severe and interfering with daily activities</li>
<li>You suspect a fracture, severe sprain, or tendon tear</li>
<li>You develop signs of infection (fever, red streaks, warmth spreading from the injury)</li>
</ul>

<h2>Summary: Heat vs Cold Quick Reference</h2>

<p><strong>Use COLD for:</strong></p>
<ul>
<li>Acute injuries (first 48-72 hours)</li>
<li>Swelling and inflammation</li>
<li>Post-exercise recovery</li>
<li>Acute arthritis flare-ups</li>
<li>Migraine relief</li>
</ul>

<p><strong>Use HEAT for:</strong></p>
<ul>
<li>Chronic pain and stiffness</li>
<li>Muscle tension and spasms</li>
<li>Old injuries (after inflammation has subsided)</li>
<li>Pre-exercise warm-up</li>
<li>Menstrual cramps</li>
</ul>

<p><strong>Use CONTRAST THERAPY for:</strong></p>
<ul>
<li>Subacute injuries (3-7 days old)</li>
<li>Chronic repetitive strain conditions</li>
<li>Enhanced circulation and healing</li>
</ul>

<h2>Conclusion: Personalized Pain Relief</h2>

<p>Understanding when to use heat versus cold therapy empowers you to take control of your pain management and accelerate recovery. While these general guidelines apply to most situations, individual responses vary. Pay attention to how your body reacts and adjust accordingly.</p>

<p>The key is timing: cold for fresh injuries and acute inflammation, heat for chronic pain and muscle tension, and contrast therapy for subacute injuries and circulation enhancement. When in doubt, start with cold therapy—it's safer for acute conditions and won't worsen inflammation like heat can.</p>

<p>Professional-grade heat and cold therapy devices provide consistent, safe, and effective relief compared to improvised home remedies. Investing in quality therapy equipment can make a significant difference in your recovery and long-term pain management success.</p>

<div class="article-cta" style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 2rem; border-radius: 8px; margin: 2rem 0; border-left: 4px solid #4770DB;">
  <h3 style="margin-top: 0; color: #2c3e50;">Shop Professional Pain Relief Devices</h3>
  <p style="margin-bottom: 1rem;">Discover our FDA-compliant heat therapy devices, cold compression wraps, and professional-grade pain relief equipment. Free shipping on orders over $50.</p>
  <a href="/collections/pain-relief-recovery" style="display: inline-block; background: #4770DB; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: 600;">Browse Pain Relief Collection →</a>
</div>

<hr style="margin: 2rem 0; border: none; border-top: 1px solid #dee2e6;">

<p><em><strong>Medical Disclaimer:</strong> This article is for informational purposes only and does not constitute medical advice. Always consult with a qualified healthcare provider before starting any new treatment regimen, especially if you have pre-existing medical conditions or are taking medications.</em></p>

<p><em><strong>References:</strong> This guide is based on current medical research and evidence-based guidelines from sports medicine, physical therapy, and pain management literature. Individual results may vary.</em></p>

</div>
"""

# Create blog post using REST API
blog_id = "89643450445"  # "News" blog

article_data = {
    "article": {
        "title": title,
        "author": author,
        "tags": tags,
        "body_html": body_html,
        "published": True,
        "handle": handle,
        "summary_html": "<p>Learn the science-backed differences between heat and cold therapy, when to use each method, and how to choose the right treatment for your specific pain condition. Comprehensive guide with evidence-based protocols for optimal pain relief.</p>"
    }
}

response = requests.post(
    f"{REST_URL}/blogs/{blog_id}/articles.json",
    headers=headers,
    json=article_data
)

if response.status_code == 201:
    article = response.json()['article']
    print(f"✅ Article created successfully!")
    print(f"   ID: {article['id']}")
    print(f"   Title: {article['title']}")
    print(f"   Handle: {article['handle']}")
    print(f"   URL: https://{SHOPIFY_STORE_DOMAIN}/blogs/news/{article['handle']}")
    print(f"   Published: {article['published_at']}")
else:
    print(f"❌ Error creating article: {response.status_code}")
    print(response.json())
