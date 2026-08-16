from django.shortcuts import render
from blog.models import Post, Category

def home(request):
    posts = Post.objects.all()
    recent_posts = Post.objects.all()[:2]
    categories = Category.objects.all()

    return render(request, 'home/index.html', {
        'posts': posts,
        'recent_posts': recent_posts,
        'categories': categories,
    })