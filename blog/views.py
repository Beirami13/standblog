from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from blog.models import Post, Category, Comment, ContactMessage
from .forms import ContactUsForm

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    recent_posts = Post.objects.all().order_by('-date')[:3]
    categories = Category.objects.all()

    if request.method == "POST":
        context = request.POST.get('context')
        parent_id = request.POST.get('parent_id')
        parent_comment = None
        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)
        Comment.objects.create(
            post=post,
            author=request.user,
            context=context,
            parent=parent_comment
        )
    contexts = {
        "post": post,
        "recent_posts": recent_posts,
        "categories": categories,
    }
    return render(request, "blog/post_details.html", contexts)

def posts_list(request):
    posts = Post.objects.all()
    page_number = request.GET.get('page')
    paginator = Paginator(posts, 1)
    objects_list = paginator.get_page(page_number)
    recent_posts = Post.objects.all().order_by('-date')[:3]
    categories = Category.objects.all()
    context = {
        "posts": objects_list,
        "recent_posts": recent_posts,
        "categories": categories,
    }
    return render(request, "blog/posts_list.html", context)


def categories_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = category.post_set.all()
    return render(request, "blog/posts_list.html", {"posts": posts, "category": category})

def search(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(title__icontains=query)
    paginator = Paginator(posts, 1)
    page_number = request.GET.get('page')
    objects_list = paginator.get_page(page_number)

    return render(
        request,
        "blog/posts_list.html",
        {"posts": objects_list, "query": query}
    )

def contact_us(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
            )
            return redirect('blog:contact_us')
    else:
        form = ContactUsForm()

    return render(request, 'blog/contact.html', {'form': form})

from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def contact_messages(request):
    messages = ContactMessage.objects.all().order_by('-created_at')

    return render(
        request,
        'blog/contact_messages.html',
        {'messages': messages}
    )