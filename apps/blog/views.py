from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from apps.blog.models import Post, Comment, Tag
from apps.blog.forms import CommentForm, PostForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags


def blog_list(request):
    query = request.GET.get('q')
    if query:
        posts_list = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-created_at')
    else:
        posts_list = Post.objects.all().order_by('-created_at')
    
    paginator = Paginator(posts_list, 5)  # Show 5 posts per page.
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/index.html', {'posts': posts})


def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all().order_by('created_at')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('blog_detail', slug=post.slug)
    else:
        comment_form = CommentForm()

    meta_description = strip_tags(post.content)[:160]

    return render(request, 'blog/article.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'meta_title': post.title,
        'meta_description': meta_description,
    })


def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(tags=tag).order_by('-created_at')
    return render(request, 'blog/index.html', {'posts': posts, 'tag': tag})


@login_required
def author_dash(request):
    return render(request, "blog/author/index.html")

@login_required
def author_myarticle(request):
    return render(request, "blog/author/articles.html")

@login_required
def author_createarticle(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save the many-to-many data for the form.
            return redirect('author_myarticle')
    else:
        form = PostForm()
    return render(request, "blog/author/create.html", {'form': form})

@login_required
def author_edit_article(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('author_myarticle')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/author/create.html', {'form': form})

@login_required
def author_delete_article(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('author_myarticle')
    return render(request, 'blog/author/delete_confirm.html', {'post': post})

@login_required
def author_settings(request):
    return render(request, "blog/author/settings.html")

@csrf_exempt
def image_upload_view(request):
    if request.method == 'POST':
        file = request.FILES['file']
        # You might want to save the file to a specific location
        # and return the URL to the file.
        # For simplicity, this example doesn't save the file.
        return JsonResponse({'location': 'image_url'})
    return JsonResponse({'error': 'Invalid request'})