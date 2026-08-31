from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from blog.models import Post, Category, Comment, ContactMessage, Like
from .forms import ContactUsForm, PostForm
from django.contrib.admin.views.decorators import staff_member_required

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    recent_posts = Post.objects.all().order_by('-date')[:3]
    categories = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0).order_by('-post_count')[:10]

    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    else:
        liked_posts = []

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
        "liked_posts": liked_posts,
    }
    return render(request, "blog/post_details.html", contexts)


def posts_list(request):
    posts = Post.objects.all()
    page_number = request.GET.get('page')
    paginator = Paginator(posts, 6)
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
    posts = category.posts.all()
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

@staff_member_required
def contact_messages(request):
    messages = ContactMessage.objects.all().order_by('-created_at')

    return render(
        request,
        'blog/contact_messages.html',
        {'messages': messages}
    )


def LikeView(request, slug, pk):
        if not request.user.is_authenticated:
            return JsonResponse({
                'liked': False,
                'count': 0,
            })
        post = get_object_or_404(Post, slug=slug, id=pk)
        like_obj = Like.objects.filter(post=post, user=request.user)
        if like_obj.exists():
            like_obj.delete()
            liked = False
        else:
            Like.objects.create(post=post, user=request.user)
            liked = True

        return JsonResponse({
            'liked': liked,
            'count': post.likes.count(),
        })

def about(request):
    return render(request, 'blog/about.html')


def add_post(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()

            return redirect(post.get_absolute_url())
    else:
        form = PostForm()

    return render(
        request,
        'blog/add_post.html',
        {'form': form}
    )
  else:
    return redirect('account:login')
