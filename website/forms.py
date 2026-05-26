from django import forms
from .models import Comment, NewsletterSubscriber


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'website', 'body']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your full name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your@email.com',
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://yourwebsite.com (optional)',
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Share your thoughts on this post…',
                'rows': 5,
            }),
        }
        labels = {
            'name': 'Name',
            'email': 'Email',
            'website': 'Website',
            'body': 'Comment',
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your email address',
                'class': 'footer-newsletter-input',
            }),
        }
