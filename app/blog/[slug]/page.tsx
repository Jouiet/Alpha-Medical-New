import { notFound } from 'next/navigation';
import Link from 'next/link';
import { Calendar, Clock, ArrowLeft, Share2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Metadata } from 'next';

const blogPosts: Record<string, {
  title: string;
  category: string;
  author: string;
  date: string;
  readTime: string;
  image: string;
  content: { type: string; text: string }[];
}> = {
  'how-to-relieve-lower-back-pain': {
    title: 'How to Relieve Lower Back Pain: A Comprehensive Guide',
    category: 'Pain Management',
    author: 'Dr. Sarah Johnson',
    date: 'March 15, 2025',
    readTime: '8 min read',
    image: 'https://images.pexels.com/photos/6823567/pexels-photo-6823567.jpeg?auto=compress&cs=tinysrgb&w=1200',
    content: [
      { type: 'p', text: 'Lower back pain affects millions of people worldwide, significantly impacting daily activities and quality of life. Understanding the root causes and implementing effective relief strategies is crucial for long-term wellness.' },
      { type: 'h2', text: 'Understanding Lower Back Pain' },
      { type: 'p', text: 'Lower back pain can stem from various sources including muscle strain, poor posture, herniated discs, or degenerative conditions. Identifying the cause is the first step toward effective treatment.' },
      { type: 'h2', text: 'Immediate Relief Strategies' },
      { type: 'p', text: 'For acute lower back pain, the following strategies can provide immediate relief:' },
      { type: 'ul', text: '• Apply ice packs for the first 48 hours to reduce inflammation\n• After 48 hours, switch to heat therapy to relax muscles\n• Maintain proper posture while sitting and standing\n• Use ergonomic support cushions and back braces\n• Practice gentle stretching exercises' },
      { type: 'h2', text: 'Effective Exercises for Back Pain' },
      { type: 'p', text: 'Strengthening core muscles is essential for supporting the lower back. Recommended exercises include:' },
      { type: 'ul', text: '• Pelvic tilts: Lie on your back with knees bent, gently arch and flatten your lower back\n• Cat-cow stretches: On hands and knees, alternate between arching and rounding your spine\n• Bird dog: From hands and knees, extend opposite arm and leg while maintaining balance\n• Bridges: Lie on your back, lift hips while keeping shoulders grounded\n• Wall sits: Slide down a wall until thighs are parallel to the floor, hold for 30 seconds' },
      { type: 'h2', text: 'Medical Devices for Back Support' },
      { type: 'p', text: 'Several medical-grade devices can provide significant relief:' },
      { type: 'ul', text: '• Back braces: Provide lumbar support and promote proper alignment\n• TENS units: Use electrical stimulation to block pain signals\n• Massage devices: Help relax tight muscles and improve circulation\n• Ergonomic chairs: Maintain proper spinal alignment during extended sitting\n• Adjustable standing desks: Allow alternation between sitting and standing positions' },
      { type: 'h2', text: 'When to Seek Professional Help' },
      { type: 'p', text: 'Consult a healthcare professional if you experience:' },
      { type: 'ul', text: '• Pain lasting more than 6 weeks\n• Severe pain not relieved by rest\n• Pain radiating down one or both legs\n• Numbness, tingling, or weakness in legs\n• Unexplained weight loss accompanying back pain\n• Loss of bladder or bowel control' },
      { type: 'h2', text: 'Prevention is Key' },
      { type: 'p', text: 'Preventing future episodes of lower back pain involves:' },
      { type: 'ul', text: '• Maintaining a healthy weight to reduce stress on the spine\n• Regular exercise focusing on core strength and flexibility\n• Proper lifting techniques: bend at knees, not waist\n• Using ergonomic furniture and equipment\n• Taking regular breaks during prolonged sitting\n• Managing stress through relaxation techniques' },
      { type: 'p', text: 'Remember, consistency is crucial. Incorporating these strategies into your daily routine can significantly reduce the frequency and severity of lower back pain episodes. Always consult with a healthcare professional before starting any new treatment regimen.' }
    ]
  },
  'benefits-of-pressotherapy-athletic-recovery': {
    title: 'The Benefits of Pressotherapy for Athletic Recovery',
    category: 'Recovery',
    author: 'Michael Chen',
    date: 'March 12, 2025',
    readTime: '6 min read',
    image: 'https://images.pexels.com/photos/8172765/pexels-photo-8172765.jpeg?auto=compress&cs=tinysrgb&w=1200',
    content: [
      { type: 'p', text: 'Pressotherapy, also known as compression therapy, has become a cornerstone of athletic recovery protocols used by professional athletes worldwide. This innovative treatment uses controlled air pressure to enhance circulation and accelerate muscle recovery.' },
      { type: 'h2', text: 'What is Pressotherapy?' },
      { type: 'p', text: 'Pressotherapy involves wearing specialized boots or sleeves that inflate and deflate in a rhythmic pattern, applying controlled pressure to the limbs. This mimics the natural muscle pump action, promoting blood flow and lymphatic drainage.' },
      { type: 'h2', text: 'Key Benefits for Athletes' },
      { type: 'ul', text: '• Reduced muscle soreness: Accelerates lactic acid removal from muscles\n• Faster recovery: Improves oxygen and nutrient delivery to tissues\n• Decreased inflammation: Enhances lymphatic drainage to reduce swelling\n• Improved flexibility: Reduces muscle tension and stiffness\n• Enhanced performance: Allows for more frequent high-intensity training sessions' },
      { type: 'h2', text: 'How Pressotherapy Works' },
      { type: 'p', text: 'The compression therapy system operates through sequential compression cycles:' },
      { type: 'ul', text: '1. Distal to proximal compression: Pressure moves from extremities toward the heart\n2. Graduated pressure levels: Intensity varies across different chambers\n3. Rhythmic cycles: Alternating compression and decompression phases\n4. Customizable settings: Adjust pressure levels and session duration based on needs' },
      { type: 'h2', text: 'Scientific Evidence' },
      { type: 'p', text: 'Research has demonstrated significant benefits of pressotherapy:' },
      { type: 'ul', text: '• 30% reduction in delayed onset muscle soreness (DOMS)\n• 40% improvement in perceived recovery\n• Enhanced blood lactate clearance post-exercise\n• Reduced markers of muscle damage and inflammation\n• Improved range of motion in treated limbs' },
      { type: 'h2', text: 'Optimal Usage Protocols' },
      { type: 'p', text: 'For maximum benefit, follow these guidelines:' },
      { type: 'ul', text: '• Timing: Use within 2 hours post-exercise for best results\n• Duration: 20-30 minute sessions are most effective\n• Frequency: Daily use during intense training periods\n• Pressure: Start with lower settings and gradually increase\n• Hydration: Drink plenty of water before and after sessions' },
      { type: 'h2', text: 'Who Can Benefit?' },
      { type: 'p', text: 'Pressotherapy is beneficial for:' },
      { type: 'ul', text: '• Competitive athletes in high-intensity sports\n• Endurance athletes (runners, cyclists, triathletes)\n• Team sport athletes (basketball, soccer, football)\n• Fitness enthusiasts with intense training routines\n• Individuals recovering from muscle strains or injuries' },
      { type: 'h2', text: 'Home vs. Professional Systems' },
      { type: 'p', text: 'While professional systems offer advanced features, home units have become increasingly sophisticated and affordable. Modern home pressotherapy systems provide:' },
      { type: 'ul', text: '• Multiple pressure zones for targeted treatment\n• Programmable pressure levels and cycles\n• Portable and user-friendly designs\n• Cost-effective alternative to clinic visits\n• Convenient recovery in the comfort of your home' },
      { type: 'p', text: 'Incorporating pressotherapy into your recovery routine can significantly enhance your athletic performance and reduce injury risk. Consult with a sports medicine professional to determine the best protocol for your specific needs.' }
    ]
  },
  'understanding-cervical-traction-therapy': {
    title: 'Understanding Cervical Traction Therapy',
    category: 'Treatment',
    author: 'Dr. Emily Roberts',
    date: 'March 10, 2025',
    readTime: '7 min read',
    image: 'https://images.pexels.com/photos/6823574/pexels-photo-6823574.jpeg?auto=compress&cs=tinysrgb&w=1200',
    content: [
      { type: 'p', text: 'Cervical traction therapy is a non-invasive treatment method that has been used for decades to relieve neck pain and associated symptoms. This comprehensive guide explores how it works, who can benefit, and proper usage techniques.' },
      { type: 'h2', text: 'What is Cervical Traction?' },
      { type: 'p', text: 'Cervical traction involves applying a gentle pulling force to the neck to stretch and decompress the cervical spine. This creates space between vertebrae, reducing pressure on nerves and intervertebral discs.' },
      { type: 'h2', text: 'Types of Cervical Traction' },
      { type: 'ul', text: '• Mechanical traction: Uses a device with weights or pneumatic pressure\n• Manual traction: Performed by a physical therapist using hands-on techniques\n• Intermittent traction: Alternates between traction and relaxation phases\n• Sustained traction: Maintains constant gentle pull for extended periods\n• Over-the-door traction: Home-use system using body weight for resistance' },
      { type: 'h2', text: 'Conditions That Benefit from Cervical Traction' },
      { type: 'ul', text: '• Cervical radiculopathy: Nerve compression causing arm pain\n• Herniated or bulging discs in the neck\n• Cervical spondylosis: Age-related wear and tear\n• Muscle spasms and neck tension\n• Whiplash injuries\n• Cervical osteoarthritis\n• Pinched nerves in the neck' },
      { type: 'h2', text: 'How Cervical Traction Works' },
      { type: 'p', text: 'The therapeutic effects occur through multiple mechanisms:' },
      { type: 'ul', text: '• Spinal decompression: Creates negative pressure in disc spaces\n• Nerve root decompression: Reduces pressure on compressed nerves\n• Muscle relaxation: Stretches tight muscles and reduces spasms\n• Improved circulation: Enhances blood flow to affected areas\n• Pain gate mechanism: Stimulates nerve fibers that inhibit pain signals' },
      { type: 'h2', text: 'Proper Usage Guidelines' },
      { type: 'p', text: 'For safe and effective cervical traction at home:' },
      { type: 'ul', text: '• Start with low force: Begin with 10-15 pounds and gradually increase\n• Duration: 15-20 minutes per session, 2-3 times daily\n• Angle: Maintain 20-30 degree neck flexion for optimal results\n• Position: Sit or lie down in a comfortable, supported position\n• Consistency: Use regularly for at least 2-3 weeks before evaluating effectiveness\n• Never use if experiencing severe pain, dizziness, or neurological symptoms' },
      { type: 'h2', text: 'Expected Results and Timeline' },
      { type: 'p', text: 'Most patients experience:' },
      { type: 'ul', text: '• Week 1-2: Reduced muscle tension and improved range of motion\n• Week 3-4: Decreased pain intensity and frequency\n• Week 5-8: Significant improvement in symptoms and function\n• Long-term: Maintenance sessions as needed to prevent recurrence' },
      { type: 'h2', text: 'Contraindications and Precautions' },
      { type: 'p', text: 'Do not use cervical traction if you have:' },
      { type: 'ul', text: '• Acute spinal injury or fracture\n• Spinal instability or ligamentous laxity\n• Rheumatoid arthritis affecting the neck\n• Osteoporosis or bone disease\n• Tumor or infection in the spine\n• Cardiovascular disease or hypertension\n• Pregnancy (unless cleared by physician)' },
      { type: 'h2', text: 'Combining with Other Therapies' },
      { type: 'p', text: 'For optimal results, combine cervical traction with:' },
      { type: 'ul', text: '• Physical therapy exercises for neck strengthening\n• Postural correction techniques\n• Heat or ice therapy\n• Anti-inflammatory medications (as prescribed)\n• Ergonomic workplace modifications\n• Stress management and relaxation techniques' },
      { type: 'p', text: 'While cervical traction can be highly effective, always consult with a healthcare professional before starting treatment. They can assess your specific condition and recommend the most appropriate traction protocol for your needs.' }
    ]
  },
  '5-essential-exercises-posture-correction': {
    title: '5 Essential Exercises for Posture Correction',
    category: 'Exercise',
    author: 'Dr. James Wilson',
    date: 'March 8, 2025',
    readTime: '5 min read',
    image: 'https://images.pexels.com/photos/6111619/pexels-photo-6111619.jpeg?auto=compress&cs=tinysrgb&w=1200',
    content: [
      { type: 'p', text: 'Poor posture has become epidemic in our digital age, contributing to neck pain, shoulder tension, and long-term spinal problems. These five exercises can help correct postural imbalances and reduce associated pain.' },
      { type: 'h2', text: 'Why Posture Matters' },
      { type: 'p', text: 'Good posture is essential for:' },
      { type: 'ul', text: '• Reducing strain on muscles, ligaments, and joints\n• Preventing chronic pain and degenerative conditions\n• Improving breathing and circulation\n• Enhancing confidence and appearance\n• Optimizing physical performance and energy levels' },
      { type: 'h2', text: 'Exercise 1: Chin Tucks' },
      { type: 'p', text: 'This exercise strengthens deep neck flexors and counters forward head posture.' },
      { type: 'ul', text: '• Sit or stand with shoulders relaxed\n• Keep eyes level and looking straight ahead\n• Gently draw chin backward, creating a "double chin"\n• Hold for 5 seconds, feeling stretch at base of skull\n• Repeat 10 times, 3 sets throughout the day' },
      { type: 'h2', text: 'Exercise 2: Wall Angels' },
      { type: 'p', text: 'Wall angels improve shoulder blade positioning and thoracic mobility.' },
      { type: 'ul', text: '• Stand with back against wall, feet 4 inches from base\n• Press lower back, head, and shoulders against wall\n• Raise arms to "goal post" position (elbows at 90 degrees)\n• Slowly slide arms overhead while maintaining contact with wall\n• Lower arms back to starting position\n• Perform 12-15 repetitions, 3 sets daily' },
      { type: 'h2', text: 'Exercise 3: Thoracic Extension over Foam Roller' },
      { type: 'p', text: 'This exercise opens up rounded upper back (kyphosis).' },
      { type: 'ul', text: '• Place foam roller horizontally under upper back\n• Support head with hands, elbows pointing forward\n• Gently arch back over roller, looking upward\n• Hold stretch for 20-30 seconds\n• Roll to different positions along upper back\n• Repeat 3-5 times per session' },
      { type: 'h2', text: 'Exercise 4: Doorway Chest Stretch' },
      { type: 'p', text: 'Stretches tight chest muscles that pull shoulders forward.' },
      { type: 'ul', text: '• Stand in doorway with forearm against door frame\n• Position elbow at shoulder height (90-degree angle)\n• Step forward with one foot until stretch felt in chest\n• Hold for 30 seconds without bouncing\n• Repeat on opposite side\n• Perform 3 times per side, twice daily' },
      { type: 'h2', text: 'Exercise 5: Prone Y-T-W Raises' },
      { type: 'p', text: 'Strengthens upper back muscles that support good posture.' },
      { type: 'ul', text: '• Lie face-down on exercise mat or bench\n• Y-raise: Extend arms overhead at 45-degree angle, lift slightly off ground\n• T-raise: Extend arms straight out to sides at shoulder level, lift slightly\n• W-raise: Bend elbows to 90 degrees, pull shoulder blades together\n• Hold each position for 3-5 seconds\n• Perform 10 repetitions of each variation, 2-3 sets' },
      { type: 'h2', text: 'Creating a Routine' },
      { type: 'p', text: 'For best results:' },
      { type: 'ul', text: '• Perform exercises daily, preferably at same time\n• Start with lower repetitions and gradually increase\n• Focus on quality over quantity - proper form is crucial\n• Combine with regular breaks from sitting\n• Use reminders or alarms to maintain consistency\n• Track progress weekly to stay motivated' },
      { type: 'h2', text: 'Additional Posture Tips' },
      { type: 'ul', text: '• Set up ergonomic workstation with monitor at eye level\n• Use lumbar support when sitting\n• Take 2-minute movement breaks every 30 minutes\n• Practice mindful posture awareness throughout day\n• Consider posture corrector braces for initial support\n• Address underlying muscle imbalances with professional guidance' },
      { type: 'p', text: 'Consistency is key to postural correction. These exercises, performed regularly along with ergonomic modifications and posture awareness, can significantly improve your alignment and reduce pain within 4-6 weeks.' }
    ]
  },
  'science-behind-led-light-therapy-skin': {
    title: 'The Science Behind LED Light Therapy for Skin',
    category: 'Wellness',
    author: 'Dr. Lisa Anderson',
    date: 'March 5, 2025',
    readTime: '9 min read',
    image: 'https://images.pexels.com/photos/3865618/pexels-photo-3865618.jpeg?auto=compress&cs=tinysrgb&w=1200',
    content: [
      { type: 'p', text: 'LED light therapy, also known as photobiomodulation, has emerged as a scientifically-backed treatment for various skin concerns. This non-invasive therapy harnesses specific wavelengths of light to stimulate cellular processes and improve skin health.' },
      { type: 'h2', text: 'Understanding Photobiomodulation' },
      { type: 'p', text: 'LED light therapy works at the cellular level by:' },
      { type: 'ul', text: '• Stimulating mitochondrial function to increase ATP production\n• Enhancing collagen and elastin synthesis\n• Improving circulation and oxygen delivery\n• Reducing inflammation and oxidative stress\n• Accelerating wound healing and tissue repair' },
      { type: 'h2', text: 'Different Wavelengths, Different Benefits' },
      { type: 'p', text: 'Each light wavelength penetrates to different skin depths and provides unique benefits:' },
      { type: 'h2', text: 'Red Light (630-700nm)' },
      { type: 'ul', text: '• Penetration: Reaches deep dermis layer\n• Benefits: Stimulates collagen production, reduces fine lines and wrinkles\n• Improves skin firmness and elasticity\n• Promotes wound healing and reduces scarring\n• Best for: Anti-aging, skin rejuvenation, scar reduction' },
      { type: 'h2', text: 'Near-Infrared Light (700-1200nm)' },
      { type: 'ul', text: '• Penetration: Deepest penetration, reaches muscle tissue\n• Benefits: Reduces inflammation, promotes healing\n• Improves circulation and lymphatic drainage\n• Relieves pain and muscle tension\n• Best for: Deep healing, anti-inflammatory effects' },
      { type: 'h2', text: 'Blue Light (400-495nm)' },
      { type: 'ul', text: '• Penetration: Superficial, targets epidermis\n• Benefits: Kills acne-causing bacteria (P. acnes)\n• Reduces sebum production\n• Minimizes pores and prevents breakouts\n• Best for: Acne treatment, oily skin management' },
      { type: 'h2', text: 'Yellow Light (570-590nm)' },
      { type: 'ul', text: '• Penetration: Moderate depth\n• Benefits: Reduces redness and inflammation\n• Improves lymphatic flow and detoxification\n• Soothes sensitive skin\n• Best for: Rosacea, sensitive skin, post-treatment healing' },
      { type: 'h2', text: 'Scientific Evidence' },
      { type: 'p', text: 'Numerous peer-reviewed studies support LED therapy effectiveness:' },
      { type: 'ul', text: '• 90% of participants showed improved skin texture after 12 weeks\n• 81% reduction in fine lines and wrinkles with consistent use\n• 50-70% improvement in acne lesions with blue light therapy\n• Significant increase in collagen density measured via ultrasound\n• Enhanced cellular metabolism and ATP production confirmed in vitro' },
      { type: 'h2', text: 'Optimal Treatment Protocols' },
      { type: 'p', text: 'For maximum benefit:' },
      { type: 'ul', text: '• Frequency: 3-5 times per week for first 4-6 weeks\n• Duration: 15-20 minutes per session\n• Distance: Position device 6-12 inches from skin\n• Consistency: Maintenance sessions 1-2 times weekly after initial phase\n• Combination: Can combine different wavelengths in single session\n• Timing: Best results with clean, makeup-free skin' },
      { type: 'h2', text: 'Safety and Side Effects' },
      { type: 'p', text: 'LED therapy is extremely safe when used properly:' },
      { type: 'ul', text: '• Non-invasive with no UV radiation\n• No downtime or recovery period needed\n• Suitable for all skin types and tones\n• Minimal side effects - occasional mild redness\n• Can be used alongside other skincare treatments\n• Safe for long-term use without skin damage risk' },
      { type: 'h2', text: 'Choosing a Home Device' },
      { type: 'p', text: 'Look for these features:' },
      { type: 'ul', text: '• FDA-cleared or approved for safety\n• Appropriate wavelengths (630-850nm for anti-aging)\n• Adequate power density (minimum 20-50 mW/cm²)\n• Treatment area size appropriate for your needs\n• Programmable timer and intensity settings\n• Positive user reviews and clinical evidence' },
      { type: 'h2', text: 'Combining with Other Treatments' },
      { type: 'p', text: 'LED therapy enhances results when combined with:' },
      { type: 'ul', text: '• Topical retinoids and vitamin C serums\n• Hyaluronic acid for hydration\n• Chemical exfoliants (use on alternate days)\n• Microneedling (wait 24-48 hours between treatments)\n• Professional facials and peels' },
      { type: 'h2', text: 'Expected Results Timeline' },
      { type: 'ul', text: '• Week 1-2: Improved skin tone and radiance\n• Week 4-6: Noticeable reduction in fine lines\n• Week 8-12: Significant improvement in skin texture and firmness\n• Month 4+: Continued collagen remodeling and long-term benefits' },
      { type: 'p', text: 'LED light therapy represents a scientifically-validated, non-invasive approach to skin rejuvenation. With consistent use and proper protocols, it can deliver significant improvements in skin health and appearance without the risks associated with more aggressive treatments.' }
    ]
  },
  'knee-rehabilitation-injury-to-recovery': {
    title: 'Knee Rehabilitation: From Injury to Full Recovery',
    category: 'Rehabilitation',
    author: 'Dr. Mark Thompson',
    date: 'March 3, 2025',
    readTime: '10 min read',
    image: 'https://images.pexels.com/photos/6823581/pexels-photo-6823581.jpeg?auto=compress&cs=tinysrgb&w=1200',
    content: [
      { type: 'p', text: 'Knee injuries are among the most common orthopedic problems, affecting athletes and non-athletes alike. Proper rehabilitation is crucial for full recovery and prevention of re-injury. This comprehensive guide outlines the phases of knee rehabilitation and provides evidence-based strategies for optimal outcomes.' },
      { type: 'h2', text: 'Common Knee Injuries' },
      { type: 'ul', text: '• ACL tear: Anterior cruciate ligament rupture\n• MCL sprain: Medial collateral ligament injury\n• Meniscus tear: Cartilage damage in knee joint\n• Patellar tendinitis: Inflammation of kneecap tendon\n• Patellofemoral pain syndrome: Runner\'s knee\n• Osteoarthritis: Degenerative joint disease' },
      { type: 'h2', text: 'Phase 1: Acute Phase (Days 1-7)' },
      { type: 'p', text: 'Goals: Control pain and swelling, protect healing tissues' },
      { type: 'ul', text: '• RICE protocol: Rest, Ice, Compression, Elevation\n• Ice: 15-20 minutes every 2-3 hours\n• Compression: Use elastic bandage or knee brace\n• Elevation: Keep knee above heart level when possible\n• Pain management: Anti-inflammatory medications as prescribed\n• Gentle ankle pumps to prevent blood clots\n• Isometric quadriceps sets without moving knee' },
      { type: 'h2', text: 'Phase 2: Early Rehabilitation (Weeks 1-3)' },
      { type: 'p', text: 'Goals: Restore range of motion, reduce swelling, begin gentle strengthening' },
      { type: 'ul', text: '• Heel slides: Gently bend and straighten knee while lying down\n• Straight leg raises: Lift leg 6 inches while keeping knee straight\n• Quad sets: Tighten thigh muscle, hold 5 seconds, 3 sets of 10\n• Hamstring curls: Bend knee against light resistance\n• Calf raises: Rise up on toes, hold 2 seconds\n• Stationary bike: Start with no resistance, gradually increase\n• Pool exercises: Use water buoyancy for gentle movement' },
      { type: 'h2', text: 'Phase 3: Progressive Strengthening (Weeks 3-8)' },
      { type: 'p', text: 'Goals: Build strength, improve stability, increase functional capacity' },
      { type: 'ul', text: '• Partial squats: Lower down 45 degrees, keeping knees behind toes\n• Step-ups: Use 4-6 inch step, progress to higher steps\n• Leg press: Start with light weight, gradually increase resistance\n• Hamstring bridges: Lie on back, lift hips while bending knees\n• Side-lying leg lifts: Strengthen hip abductors for knee stability\n• Resistance band exercises: Lateral walks, monster walks\n• Balance exercises: Single-leg stance, progressing to unstable surfaces' },
      { type: 'h2', text: 'Phase 4: Advanced Strengthening (Weeks 8-16)' },
      { type: 'p', text: 'Goals: Return to sport-specific activities, prevent re-injury' },
      { type: 'ul', text: '• Full squats: Deep squats with proper form\n• Lunges: Forward, reverse, and lateral variations\n• Single-leg squats: Progress from assisted to unassisted\n• Box jumps: Start low (6 inches), gradually increase height\n• Agility drills: Ladder drills, cone drills, cutting exercises\n• Plyometrics: Jump training for power development\n• Sport-specific drills: Gradual return to activity demands' },
      { type: 'h2', text: 'Essential Equipment for Knee Rehabilitation' },
      { type: 'ul', text: '• Knee braces: Provide support and stability during healing\n• Ice/heat packs: Manage pain and inflammation\n• Resistance bands: Progressive resistance training\n• Foam roller: Self-myofascial release for tight muscles\n• Balance board: Proprioception training\n• Compression sleeves: Reduce swelling, provide warmth\n• TENS unit: Pain management through electrical stimulation' },
      { type: 'h2', text: 'Pain Management Strategies' },
      { type: 'ul', text: '• Cryotherapy: Ice for acute inflammation\n• Heat therapy: For chronic pain and muscle tension\n• Manual therapy: Massage and joint mobilization\n• Therapeutic ultrasound: Deep tissue healing\n• Electrical stimulation: Muscle activation and pain relief\n• Acupuncture: Alternative pain management option\n• Meditation and breathing: Mind-body pain control' },
      { type: 'h2', text: 'Return to Activity Criteria' },
      { type: 'p', text: 'You can safely return to full activity when:' },
      { type: 'ul', text: '• No pain or minimal pain during activities\n• Full range of motion compared to uninjured knee\n• 90% strength of uninjured leg (measured by testing)\n• Normal gait pattern without limping\n• Able to hop on injured leg without pain\n• Successfully complete sport-specific movements\n• Cleared by physical therapist or physician' },
      { type: 'h2', text: 'Preventing Re-injury' },
      { type: 'ul', text: '• Continue strengthening exercises 2-3 times weekly\n• Maintain flexibility through regular stretching\n• Use proper technique during activities\n• Wear appropriate footwear with good support\n• Gradually progress activity intensity and duration\n• Address any biomechanical issues (e.g., flat feet)\n• Cross-train to avoid overuse\n• Listen to your body and rest when needed' },
      { type: 'h2', text: 'When to Seek Professional Help' },
      { type: 'ul', text: '• Increasing pain or swelling\n• Inability to bear weight on leg\n• Feeling of knee instability or "giving way"\n• Locking or catching sensation in knee\n• Significant loss of range of motion\n• No improvement after 2-3 weeks of home rehabilitation\n• Recurring injuries in same knee' },
      { type: 'h2', text: 'Nutrition for Joint Health' },
      { type: 'p', text: 'Support healing with proper nutrition:' },
      { type: 'ul', text: '• Protein: 1.2-2.0g per kg body weight for tissue repair\n• Omega-3 fatty acids: Reduce inflammation (fish, flaxseed)\n• Vitamin C: Collagen synthesis (citrus, berries)\n• Vitamin D: Bone health (sunlight, supplements)\n• Calcium: Bone strength (dairy, leafy greens)\n• Glucosamine/chondroitin: May support cartilage health\n• Hydration: Essential for joint lubrication' },
      { type: 'p', text: 'Remember, every knee injury is unique. This guide provides general principles, but individual rehabilitation should be customized based on specific injury type, severity, and personal factors. Always work with qualified healthcare professionals to develop an appropriate rehabilitation plan for your situation.' }
    ]
  }
};

export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const post = blogPosts[params.slug];

  if (!post) {
    return {
      title: 'Article Not Found | Alpha Medical Care',
    };
  }

  return {
    title: `${post.title} | Alpha Medical Care Blog`,
    description: post.content[0].text.substring(0, 160),
  };
}

export default function BlogArticlePage({ params }: { params: { slug: string } }) {
  const post = blogPosts[params.slug];

  if (!post) {
    notFound();
  }

  return (
    <article className="py-12">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-4xl">
          <Link href="/blog" className="mb-6 inline-flex items-center text-blue-600 hover:text-blue-700">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Blog
          </Link>

          <div className="mb-8">
            <Badge className="mb-4 bg-blue-600">{post.category}</Badge>
            <h1 className="mb-4 text-4xl font-bold text-slate-900 md:text-5xl">
              {post.title}
            </h1>
            <div className="flex flex-wrap items-center gap-4 text-slate-600">
              <div className="flex items-center gap-2">
                <Calendar className="h-4 w-4" />
                <span>{post.date}</span>
              </div>
              <div className="flex items-center gap-2">
                <Clock className="h-4 w-4" />
                <span>{post.readTime}</span>
              </div>
              <div className="flex items-center gap-2">
                <span>By {post.author}</span>
              </div>
            </div>
          </div>

          <div className="relative mb-8 aspect-[21/9] overflow-hidden rounded-lg">
            <img
              src={post.image}
              alt={post.title}
              className="h-full w-full object-cover"
            />
          </div>

          <div className="prose prose-lg prose-slate max-w-none">
            {post.content.map((block, index) => {
              if (block.type === 'h2') {
                return (
                  <h2 key={index} className="mb-4 mt-8 text-2xl font-bold text-slate-900">
                    {block.text}
                  </h2>
                );
              }
              if (block.type === 'p') {
                return (
                  <p key={index} className="mb-4 text-slate-700 leading-relaxed">
                    {block.text}
                  </p>
                );
              }
              if (block.type === 'ul') {
                return (
                  <ul key={index} className="mb-6 ml-6 list-disc space-y-2 text-slate-700">
                    {block.text.split('\n').map((item, i) => (
                      <li key={i}>{item.replace(/^[•\-]\s*/, '')}</li>
                    ))}
                  </ul>
                );
              }
              return null;
            })}
          </div>

          <div className="mt-12 flex items-center justify-between border-t pt-8">
            <Link href="/blog">
              <Button variant="outline">
                <ArrowLeft className="mr-2 h-4 w-4" />
                More Articles
              </Button>
            </Link>
            <Button variant="outline">
              <Share2 className="mr-2 h-4 w-4" />
              Share Article
            </Button>
          </div>
        </div>
      </div>
    </article>
  );
}
