from django.db.models import Count
from django.shortcuts import render
from blog.models import Post, Category, Like

def home(request):
    posts = Post.objects.all()
    recent_posts = posts[:2]
    categories = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0).order_by('-post_count')[:10]

    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    else:
        liked_posts = []

    return render(request, 'home/index.html', {
        'posts': posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'liked_posts': liked_posts,
    })