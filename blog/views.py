from django.shortcuts import render,get_object_or_404

from blog.models import Post


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post_details.html", {"post": post})

def posts_list(request):
    posts = Post.objects.all()
    return render(request, "blog/posts_list.html", {"posts": posts})