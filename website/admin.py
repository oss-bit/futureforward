from django.contrib import admin
from django.utils.html import format_html
from .models import (Category,  Author, Post, Comment,
                     NewsletterSubscriber, Slide, Paragraph, ParagraphImage)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}



@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'avatar_initial']


# ── Inlines ──────────────────────────────────────────────────────────────────

class ParagraphImageInline(admin.TabularInline):
    model = ParagraphImage
    extra = 1
    fields = ['image', 'image_preview', 'caption', 'alt_text', 'position', 'order']
    readonly_fields = ['image_preview']
    ordering = ['order']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:4px;object-fit:cover;">',
                obj.image.url
            )
        return '—'
    image_preview.short_description = 'Preview'


class ParagraphInline(admin.StackedInline):
    model = Paragraph
    extra = 1
    fields = ['order', 'heading', 'content']
    ordering = ['order']
    # Opens the paragraph's own change page where ParagraphImageInline is shown
    show_change_link = True


# ── Post ─────────────────────────────────────────────────────────────────────

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ['title', 'author', 'category', 'post_type',
                     'status', 'is_featured', 'published_at', 'paragraph_count']
    list_filter   = ['status', 'post_type', 'category', 'is_featured']
    search_fields = ['title', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy  = 'published_at'
    list_editable   = ['status', 'is_featured']
    inlines         = [ParagraphInline]

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'category', 'excerpt')
        }),
        ('Appearance', {
            'fields': ('featured_image',)
        }),
        ('Publishing', {
            'fields': ('post_type', 'status', 'is_featured',
                       'published_at', 'read_time')
        }),
    )

    def paragraph_count(self, obj):
        count = obj.paragraphs.count()
        return count if count else '—'
    paragraph_count.short_description = 'Paragraphs'


# ── Paragraph (standalone, so images can be managed directly) ────────────────

@admin.register(Paragraph)
class ParagraphAdmin(admin.ModelAdmin):
    list_display  = ['post', 'order', 'heading_preview', 'image_count']
    list_filter   = ['post']
    search_fields = ['post__title', 'heading', 'content']
    ordering      = ['post', 'order']
    inlines       = [ParagraphImageInline]

    def heading_preview(self, obj):
        return obj.heading if obj.heading else '(no heading)'
    heading_preview.short_description = 'Heading'

    def image_count(self, obj):
        count = obj.images.count()
        return count if count else '—'
    image_count.short_description = 'Images'


# ── ParagraphImage (standalone for bulk image management) ────────────────────

@admin.register(ParagraphImage)
class ParagraphImageAdmin(admin.ModelAdmin):
    list_display  = ['paragraph', 'image_preview', 'position', 'order', 'caption']
    list_filter   = ['position', 'paragraph__post']
    search_fields = ['caption', 'alt_text', 'paragraph__post__title']
    list_editable = ['position', 'order']
    ordering      = ['paragraph__post', 'paragraph__order', 'order']
    readonly_fields = ['image_preview']

    fieldsets = (
        ('Image', {
            'fields': ('paragraph', 'image', 'image_preview')
        }),
        ('Metadata', {
            'fields': ('caption', 'alt_text')
        }),
        ('Layout', {
            'fields': ('position', 'order')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:160px;border-radius:6px;object-fit:cover;">',
                obj.image.url
            )
        return '—'
    image_preview.short_description = 'Preview'


# ── Comment ──────────────────────────────────────────────────────────────────

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ['name', 'post', 'created_at', 'approved']
    list_filter   = ['approved']
    list_editable = ['approved']
    actions       = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = 'Approve selected comments'


# ── Newsletter ────────────────────────────────────────────────────────────────

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter  = ['is_active']


# ── Slide ─────────────────────────────────────────────────────────────────────

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display  = [ 'title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
