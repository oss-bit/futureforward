from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.http import FileResponse, Http404
from .models import Post, Category,  Slide, Author, Reports 
from .forms import CommentForm, NewsletterForm
import os

def _newsletter_form():
    return NewsletterForm()


def home(request):
    slides = Slide.objects.filter(is_active=True)
    recent_posts = Post.objects.filter(status='published').select_related(
        'author', 'category')[:6]
    newsletter_form = _newsletter_form()

    if request.method == 'POST' and 'newsletter_email' in request.POST:
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            try:
                newsletter_form.save()
                messages.success(request, 'Thank you for subscribing!')
            except Exception:
                messages.info(request, 'You are already subscribed.')
            return redirect('home')

    context = {
        'slides': slides,
        'recent_posts': recent_posts,
        'newsletter_form': newsletter_form,
        'active_page': 'home',
    }
    return render(request, 'website/home.html', context)


def about(request):
    newsletter_form = _newsletter_form()

    if request.method == 'POST' and 'newsletter_email' in request.POST:
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            try:
                newsletter_form.save()
                messages.success(request, 'Thank you for subscribing!')
            except Exception:
                messages.info(request, 'You are already subscribed.')
            return redirect('about')

    context = {
        'newsletter_form': newsletter_form,
        'active_page': 'about',
    }
    return render(request, 'website/about.html', context)

def reports(request):
    report_type = request.GET.get('type', 'Project')

    reports =  Reports.objects.filter(report_type=report_type,is_active=True)
    context = {'type':report_type,
                'reports':reports,
               }
    return render(request, 'website/reports.html',context)


def download_file(request, filename):
    # Construct the full path to the file (e.g., in your media folder)
    file_path = os.path.join(settings.MEDIA_ROOT,'reports' ,filename)
    
    if os.path.exists(file_path):
        # Open the file in 'rb' (read binary) mode
        file_handle = open(file_path, 'rb')
        # Return a FileResponse with the appropriate filename
        return FileResponse(file_handle, as_attachment=True, filename=filename)
    
    raise Http404("File does not exist")

def blog_list(request):
    posts = Post.objects.filter(
        status='published', post_type='blog'
    ).select_related('author', 'category')

    # Filter by category
    category_slug = request.GET.get('category', '')
    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=active_category)

    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(body__icontains=search_query)
        )

    featured_post = Post.objects.filter(
        status='published', post_type='blog', is_featured=True
    ).select_related('author', 'category').first()

    # If no manually featured, use the latest
    if not featured_post:
        featured_post = Post.objects.filter(
            status='published', post_type='blog'
        ).select_related('author', 'category').first()

    # Exclude featured from grid
    if featured_post:
        grid_posts = posts.exclude(pk=featured_post.pk)
    else:
        grid_posts = posts

    categories = Category.objects.all()
    recent_posts = Post.objects.filter(
        status='published', post_type='blog'
    ).select_related('author')[:5]

    newsletter_form = _newsletter_form()
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            try:
                newsletter_form.save()
                messages.success(request, 'Thank you for subscribing!')
            except Exception:
                messages.info(request, 'You are already subscribed.')
            return redirect('blog_list')

    context = {
        'featured_post': featured_post,
        'posts': grid_posts,
        'categories': categories,
        'recent_posts': recent_posts,
        'active_category': active_category,
        'search_query': search_query,
        'total_count': Post.objects.filter(status='published', post_type='blog').count(),
        'newsletter_form': newsletter_form,
        'active_page': 'stories',
    }
    return render(request, 'website/blog_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(approved=True)
    comment_form = CommentForm()
    related_posts = Post.objects.filter(
        status='published', post_type=post.post_type
    ).exclude(pk=post.pk).select_related('author', 'category')[:2]

    recent_posts = Post.objects.filter(
        status='published'
    ).exclude(pk=post.pk).select_related('author')[:5]

    newsletter_form = _newsletter_form()

    if request.method == 'POST':
        if 'newsletter_email' in request.POST:
            newsletter_form = NewsletterForm(request.POST)
            if newsletter_form.is_valid():
                try:
                    newsletter_form.save()
                    messages.success(request, 'Thank you for subscribing!')
                except Exception:
                    messages.info(request, 'You are already subscribed.')
            return redirect('post_detail', slug=slug)

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(
                request,
                'Your comment has been submitted and is awaiting approval.'
            )
            return redirect('post_detail', slug=slug)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts,
        'recent_posts': recent_posts,
        'newsletter_form': newsletter_form,
        'active_page': 'stories',
    }
    return render(request, 'website/post_detail.html', context)


@require_POST
def newsletter_subscribe(request):
    """AJAX endpoint for newsletter subscription."""
    form = NewsletterForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            return JsonResponse({'status': 'ok', 'message': 'Thank you for subscribing!'})
        except Exception:
            return JsonResponse({'status': 'info', 'message': 'You are already subscribed.'})
    return JsonResponse({'status': 'error', 'message': 'Please enter a valid email address.'})
