"""
Management command to seed the database with sample content
for Future Forward Development Initiative (FFDI) website.
"""

import os
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from website.models import (
    Category, Author, Post, Paragraph, ParagraphImage, Slide, Reports
)


def local_image(relative_path):
    """Load image from seed_images folder."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, relative_path)
    if not os.path.exists(full_path):
        return None
    return open(full_path, 'rb')


def local_file(relative_path):
    """Load PDF from seed_files folder."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, relative_path)
    if not os.path.exists(full_path):
        return None
    return open(full_path, 'rb')


# ====================== SAMPLE DATA ======================
POSTS = [
    {
        "title": "The Dopamine Trap: How Algorithms Hooked a Generation",
        "excerpt": ("While young Nigerians are heavily plugged into the internet, they are mostly participating as consumers of entertainment rather than creators of wealth.",
                    "When a young person’s primary relationship with a screen is curated by ultra-smart algorithms like TikTok, Instagram, or Facebook, their brain gets used to quick, easy dopamine hits.",
                    "Tech literacy must be integrated into our schools with the exact same weight as reading and writing."
        ),
        "category": "Youth Empowerment",
        "is_featured": True,
        "featured_image_path":"seed_images/youths_scrolling.jpg",
        "read_time": 6,
        "days_ago": 3,
        "paragraphs":[
            {
                "heading": "",
                "content": (
                   "More than 60% of Nigerians are under the age of 25. This means our country has one of the youngest, most energetic, and most vibrant populations in the world. On paper, this is our biggest strength. But if you look around today, a quiet crisis is playing out on millions of glowing smartphone screens. While young Nigerians are heavily plugged into the internet, they are mostly participating as consumers of entertainment rather than creators of wealth.This is not a character flaw, and it is not because young people are lazy. It is a structural trap."
                ),
                "order": 0,
                # No image on this paragraph
                "images": [
                    {
                        "source":   "local",
                        "value":    "seed_images/youths_phone_scrolling.webp",
                        "filename": "youths_phone_scrolling.webp",
                        "caption":  "",
                        "alt_text": "",
                        "position": "below",
                        "order":    0,
                    },
                ],
            },
            {
                "heading": "",
                "content": (
                    "The root of the problem lies in our educational system. Because our schools have historically treated practical tech skills—like coding, digital marketing, data analysis, or UI/UX design—as luxuries rather than necessities, millions of youth jump online without the tools to use the internet to their advantage.",
                     ),
                "order": 10,
                # No image on this paragraph
            },
            {
                "heading": "",
                "content": (
                   "When a young person’s primary relationship with a screen is curated by ultra-smart algorithms like TikTok, Instagram, or Facebook, their brain gets used to quick, easy dopamine hits. They learn to chase likes and views instead of high-income skills. In a country where money is hard to come by, youth end up spending their scarce cash on expensive data bundles just to watch endless videos, making global tech companies rich while their own pockets stay empty.",

                ),
                "order": 20,
                
            },
            {
                "heading": "",
                "content": (
                   "The real-world consequences of this digital vacuum are dangerous. Recent studies reveal that over 83% of surveyed Nigerian university students constantly encounter fraudulent \"get-rich-quick\" schemes and fake investment promises on social media. Because they lack baseline digital and financial literacy to spot these scams, about 40% of them actually fall for these traps. This leads to massive financial losses, deep academic disengagement, and severe anxiety."
                ),
                "order": 30,
                # Two images: one floated left, one floated right
            },
            {
                "heading": "",
                "content": (
                    "We cannot simply lecture young people and expect them to easily switch from a high-energy entertainment feed to a dry, self-taught tech tutorial—especially when they are battling expensive data, slow internet, and unstable electricity."
                ),
                "order": 40,
                # Image placed below the paragraph text
            },
            {
                "heading": "",
                "content": (
                   "To break this dopamine trap, Nigeria must bridge the massive gap between curriculum policies and classroom realities. Tech literacy must be integrated into our schools with the exact same weight as reading and writing. Until we formally equip young Nigerians with the right skills, clever algorithms will continue to steal their time and attention—the very assets they should be using to build a prosperous future for themselves and the nation."
                ),
                "order": 50,
                # No image on the closing paragraph
            },
        ],
    },

    # ── All other posts remain image-free for now;
    #    add an "images" key to any paragraph to attach images later.
]

SLIDES = [
        {
            "title": "Sustainable Futures are Not a Privilege",
            "title_em": "Right",
            "description": "We equip young Nigerians with knowledge, skills, and platforms to lead climate action, mental wellbeing, and sustainable community development.",
            "cta_text": "Learn More About Us",
            "cta_url": "/about-us/",
            "order": 1
            },
        {
            "title": "We Empower Marginalized",
            "title_em": "Youth",
            "description": "Building bridges for young Nigerians to lead real change in climate resilience, agriculture, mental health, and community development.",
            "cta_text": "Explore Our Focus Areas",
            "cta_url": "/#thematic",
            "order": 2
            },
        {
            "title": "Youth Empowerment is Not a Dream",
            "title_em": "It’s Reality",
            "description": "We create platforms where young Nigerians actively lead on climate change, mental wellbeing, agriculture, and community resilience.",
            "cta_text": "Read Our Stories",
            "cta_url": "/blog-posts/",
            "order": 3
            },
        {
            "title": "The Future Belongs to Those Who",
            "title_em": "Shape It",
            "description": "We empower young Nigerians with the skills and confidence to drive climate resilience, mental wellbeing, and sustainable development.",
            "cta_text": "Learn More About Us",
            "cta_url": "/about-us/",
            "order": 4
            },
        {
            "title": "Young Voices Deserve To Be",
            "title_em": "Heard",
            "description": "We create spaces for Nigerian youth to speak out, lead, and drive meaningful change in climate, agriculture, and mental health.",
            "cta_text": "Explore Our Focus Areas",
            "cta_url": "/#thematic",
            "order": 5
            },
        {
            "title": "We Empower Young Nigerians To",
            "title_em": "Lead The Change",
            "description": "Building a new generation of resilient leaders driving sustainable development, climate action, and mental wellbeing across Nigeria.",
            "cta_text": "Read Our Stories",
            "cta_url": "/blog-posts/",
            "order": 6
            },
        {
        "title": "Young People Are Not The Future",
        "title_em": "They Are The Present",
        "description": "We equip Nigerian youth today with skills, voice, and opportunity to create solutions in climate resilience, agriculture, and community development.",
        "cta_text": "Learn More About Us",
        "cta_url": "/about-us/",
        "order": 7
                }
]





REPORTS = [
    {
        "report_type": "Project",
        "title": "Resilience Reimagined",
        "file_name": "Resilience_Reimagined_Report.pdf",
        "file_path": "seed_files/reports/Resilience_Reimagined_Report.pdf",
        "thumbnail_filename": "Resilience_Reimagined.png",
        "file_size": 1.3,
        "is_active": True,
    },
    {
        "report_type": "Project",
        "title": "The Green Project",
        "file_name": "The_Green_Future_Project_Report.pdf",
        "file_path": "seed_files/reports/The_Green_Future_Project_Report.pdf",
        "thumbnail_filename": "The_Green_Project.png",
        "file_size": 1.2,
        "is_active": True,
    }
]


class Command(BaseCommand):
    help = 'Seed the database with sample content for FFDI website'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing data before seeding')

    def handle(self, *args, **options):
        if options.get('clear'):
            self.stdout.write('Clearing existing data...')
            Post.objects.all().delete()
            Category.objects.all().delete()
            Author.objects.all().delete()
            Slide.objects.all().delete()
            Reports.objects.all().delete()
            self.stdout.write(self.style.WARNING('Existing data cleared.'))

        # 1. Author
        author, _ = Author.objects.get_or_create(
            name='Communications',
            defaults={
                'role': 'FFDI Team',
                'bio': 'Future Forward Development Initiative (FFDI) is a youth-led organization passionate about empowering young people and underserved communities in Northern Nigeria.',
                'avatar_initial': 'F',
            }
        )
        self.stdout.write(f' ✓ Author: {author.name}')

        # 2. Categories with Icons
        cat_icons = {
            'Gender & Inclusion': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="8" r="5"/><circle cx="16" cy="8" r="5"/><path d="M8 14v6"/><path d="M16 14v6"/><path d="M12 18h8"/></svg>',
            'Health & Well-being': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 11V5a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v6"/><path d="M12 3v18"/><circle cx="12" cy="12" r="4"/><path d="M8 15h8"/></svg>',
            'Youth Empowerment': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 18a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v12z"/><circle cx="12" cy="11" r="3"/><path d="M19 8v8"/></svg>',
            'Climate Action': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v2"/><path d="M12 20v2"/><path d="M4.93 4.93l1.41 1.41"/><path d="M17.66 17.66l1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="M6.34 17.66l-1.41 1.41"/><path d="M19.07 4.93l-1.41 1.41"/><path d="M12 7a5 5 0 0 1 5 5 5 5 0 0 1-10 0 5 5 0 0 1 5-5z"/></svg>',
            'Entrepreneurship': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/><path d="M12 22v-5"/></svg>',
        }

        for name, icon in cat_icons.items():
            Category.objects.get_or_create(
                slug=slugify(name),
                defaults={'name': name, 'icon': icon}
            )
        self.stdout.write(' ✓ Categories created')

        # 3. Seed Posts + Paragraphs + Images
        post_count = 0
        for data in POSTS:
            slug = slugify(data['title'])[:250]
            pub_date = timezone.now() - timezone.timedelta(days=data.get('days_ago', 0))
            futured_img = local_image(data['featured_image_path'])
            default_kwargs = {
                    'title': data['title'],
                    'author': author,
                    'category': Category.objects.filter(name=data['category']).first(),
                    'excerpt': data['excerpt'],
                    'post_type': 'blog',
                    'status': 'published',
                    'is_featured': data.get('is_featured', False),
                    'published_at': pub_date,
                    'read_time': data.get('read_time', 4),
                }
            if futured_img:
                filename = os.path.basename(data['featured_image_path'])
                file_img = File( futured_img,filename )
                default_kwargs['featured_image']=file_img

            post, created = Post.objects.get_or_create(
                slug=slug,
                defaults=default_kwargs)

            if created:
                for p in data.get('paragraphs', []):
                    para = Paragraph.objects.create(
                        post=post,
                        heading=p.get('heading', ''),
                        content=p['content'],
                        order=p['order']
                    )
                    for img in p.get('images', []):
                        file_obj = local_image(img['value'])
                        if file_obj:
                            pi = ParagraphImage(
                                paragraph=para,
                                caption=img.get('caption', ''),
                                alt_text=img.get('alt_text', ''),
                                position=img.get('position', 'above'),
                                order=img.get('order', 0),
                            )
                            pi.image.save(img['filename'], File(file_obj), save=True)
                            file_obj.close()
                post_count += 1
            
        self.stdout.write(f' ✓ {post_count} blog posts seeded')

        # 4. Seed Slides
        for slide in SLIDES:
            Slide.objects.get_or_create(order=slide['order'], defaults=slide)
        self.stdout.write(f' ✓ {len(SLIDES)} slides seeded')

        # 5. Seed Reports with PDF files
        report_count = 0
        for data in REPORTS:
            file_obj = local_file(data['file_path'])
            if not file_obj:
                self.stdout.write(self.style.WARNING(f'File not found: {data["file_path"]}'))
                continue

            report, created = Reports.objects.get_or_create(
                file_name=data['file_name'],
                defaults={
                    'report_type': data['report_type'],
                    'title': data['title'],
                    'thumbnail_filename': data['thumbnail_filename'],
                    'file_size': data['file_size'],
                    'is_active': data['is_active'],
                }
            )
            if created:
                report.file.save(data['file_name'], File(file_obj), save=True)
                file_obj.close()
                report_count += 1

        self.stdout.write(f' ✓ {report_count} reports seeded')

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
        self.stdout.write('Run: python manage.py runserver')
