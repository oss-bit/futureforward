from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.TextField(blank=True, null=True, help_text="Paste full SVG code here")

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Author(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default='Communications')
    bio = models.TextField(blank=True)
    avatar_initial = models.CharField(max_length=2, default='C')

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    POST_TYPE_CHOICES = [
        ('blog', 'Blog Post'),
        ('press', 'Press Release'),
        ('policy', 'Policy Brief'),
    ]

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=320)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    excerpt = models.TextField(max_length=500, blank=True)
    featured_image = models.ImageField(upload_to='posts/', blank=True, null=True)
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='blog')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)
    read_time = models.PositiveIntegerField(default=3, help_text='Minutes to read')

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', kwargs={'slug': self.slug})


# ── NEW: Structured paragraph content ──────────────────────────────────────

class Paragraph(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='paragraphs')
    heading = models.CharField(
        max_length=200, blank=True,
        help_text='Optional sub-heading displayed above this paragraph'
    )
    content = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'Paragraph {self.order} — {self.post.title[:40]}'


class ParagraphImage(models.Model):
    IMAGE_POSITION_CHOICES = [
        ('above', 'Above paragraph'),
        ('below', 'Below paragraph'),
        ('left',  'Float left'),
        ('right', 'Float right'),
    ]

    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/paragraphs/')
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200, blank=True, help_text='Screen-reader description')
    position = models.CharField(
        max_length=10, choices=IMAGE_POSITION_CHOICES, default='above'
    )
    order = models.PositiveIntegerField(default=0, help_text='Order when multiple images share a paragraph')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'Image {self.order} for Paragraph {self.paragraph.order} — {self.paragraph.post.title[:30]}'


# ── Everything below is unchanged ──────────────────────────────────────────

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


class Reports(models.Model):
    REPORT_CHOICES = [
        ('Project', 'Project'),
        ('Annual', 'Annual'),
    ]
    report_type = models.CharField(max_length=50, choices=REPORT_CHOICES, default='Project')
    file_name = models.CharField(max_length=200)
    title = models.CharField(max_length=300)
    thumbnail_filename = models.CharField(max_length=200)
    file_size = models.FloatField()
    is_active = models.BooleanField(default=False)
    publish_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='reports/', null=True, blank=True)
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class Slide(models.Model):
    title = models.CharField(max_length=200)
    title_em = models.CharField(max_length=100, blank=True,
                                 help_text='Italic highlighted word(s) in title')
    description = models.TextField()
    cta_text = models.CharField(max_length=60, default='Discover Our Work')
    cta_url = models.CharField(max_length=200, default='#about')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
