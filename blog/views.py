from django.shortcuts import render,get_object_or_404

from blog.models import Post


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, "blog/post_details.html", {"post": post})