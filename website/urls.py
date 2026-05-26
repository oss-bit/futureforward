from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about, name='about'),
    path('blog-posts/', views.blog_list, name='blog_list'),
    path('blog-posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('reports/', views.reports, name='reports'),
    path('download/<str:filename>/', views.download_file, name='download_file'),
    ]
