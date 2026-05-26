# Connected Development [CODE] — Django Website

A full Django project replicating the Connected Development [CODE] website across four pages:
- **Home** (`/`) — hero slider, about, mandate, values, thematic areas, stories, partners
- **About** (`/about-us/`) — intro, vision/mission glass cards, objectives, NGO certification
- **Blog List** (`/blog-posts/`) — featured post, filterable grid, sidebar with search/tags/social
- **Post Detail** (`/blog-posts/<slug>/`) — article body, related posts, comments, reading progress

---

## Quick Start

### 1. Clone / unzip the project
```bash
cd code_project
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Seed the database with sample content
```bash
python manage.py seed_data
```
To wipe and re-seed:
```bash
python manage.py seed_data --clear
```

### 6. Create a superuser (for the admin)
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** in your browser.  
Admin panel: **http://127.0.0.1:8000/admin/**

---

## Project Structure

```
code_project/
├── manage.py
├── requirements.txt
├── db.sqlite3                      (created after migrate)
│
├── code_project/                   Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── website/                        Main app
    ├── models.py                   Post, Category, Tag, Author, Comment,
    │                               NewsletterSubscriber, Slide,
    │                               ThematicArea, DonorPartner
    ├── views.py                    home, about, blog_list, post_detail,
    │                               newsletter_subscribe
    ├── urls.py
    ├── forms.py                    CommentForm, NewsletterForm
    ├── admin.py                    Full admin config for all models
    │
    ├── templatetags/
    │   └── website_tags.py         mod_six, mod_two_delay, multiply_by,
    │                               slice_after_words, filter_published
    │
    ├── management/commands/
    │   └── seed_data.py            python manage.py seed_data [--clear]
    │
    ├── static/
    │   ├── css/
    │   │   ├── main.css            Base styles (nav, hero slider, sections)
    │   │   ├── pages.css           Page-specific styles (about, blog, article)
    │   │   └── extra.css           Django additions (mobile nav, messages,
    │   │                           progress bar, extra.css)
    │   └── js/
    │       └── main.js             Slider, scroll reveal, counters,
    │                               mobile nav, newsletter AJAX, scroll-top
    │
    └── templates/website/
        ├── base.html               Shared nav, footer, messages, static tags
        ├── home.html               Landing page
        ├── about.html              About Us page
        ├── blog_list.html          Blog listing with sidebar
        └── post_detail.html        Single article page
```

---

## URLs

| URL | View | Name |
|-----|------|------|
| `/` | `home` | `home` |
| `/about-us/` | `about` | `about` |
| `/blog-posts/` | `blog_list` | `blog_list` |
| `/blog-posts/<slug>/` | `post_detail` | `post_detail` |
| `/newsletter/subscribe/` | `newsletter_subscribe` | `newsletter_subscribe` |
| `/admin/` | Django admin | — |

---

## Key Features

- **Hero slider** — auto-advances every 6 s, dot navigation, prev/next arrows, Ken Burns zoom, staggered content animations
- **Scroll reveal** — elements animate in as you scroll using IntersectionObserver
- **Counter animation** — stat numbers count up when scrolled into view
- **Vision/Mission glass cards** — frosted-glass backdrop-filter cards over a rich CSS background scene
- **Blog filtering** — filter by category via URL query param (`?category=<slug>`)
- **Blog search** — keyword search across title, excerpt, and body (`?q=<term>`)
- **Comment system** — moderated comments; approve in admin before they appear
- **Newsletter AJAX** — footer email subscribe uses fetch() with CSRF, no page reload
- **Reading progress bar** — thin gold bar tracks scroll progress on article pages
- **Mobile nav** — hamburger drawer on screens ≤ 900 px
- **Flash messages** — Django messages styled as toast notifications, auto-dismiss after 4 s
- **Admin** — full content management for all models via Django admin

---

## Colour Palette

| Variable | Value | Usage |
|----------|-------|-------|
| `--green-deep` | `#002525` | Backgrounds, nav, footer |
| `--green-mid` | `#004040` | Section backgrounds |
| `--green-accent` | `#007070` | Links, accents |
| `--green-light` | `#00a0a0` | Highlights |
| `--gold` | `#ffbf00` | Borders, badges, CTAs |
| `--gold-light` | `#ffdb4d` | Hover states, italic text |
| `--cream` | `#f8f3e8` | Page background |

---

## Customising Content

All content is managed through the Django admin at `/admin/`.

- **Slides** — edit hero slider slides (tag, title, description, CTA)
- **Thematic Areas** — add/reorder the 8 focus area cards on the homepage
- **Posts** — create blog posts with rich body text, category, tags, card icon/gradient
- **Authors** — manage author profiles shown in sidebars and article headers
- **Donor Partners** — add partner logos for the marquee section
- **Newsletter Subscribers** — view all subscribers
- **Comments** — moderate and approve reader comments

---

## Production Notes

Before deploying to production:

1. Change `SECRET_KEY` in `settings.py` to a random secret
2. Set `DEBUG = False`
3. Add your domain to `ALLOWED_HOSTS`
4. Run `python manage.py collectstatic`
5. Configure a proper database (PostgreSQL recommended)
6. Set up a web server (nginx + gunicorn recommended)
7. Configure media file serving for uploaded images
