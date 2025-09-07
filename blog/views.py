from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment, Tag
from blog.forms import CommentForm, PostForm, ProfileForm
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import os
from django.conf import settings
import uuid


@csrf_exempt
@login_required
def image_upload_view(request):
    if request.method == 'POST':
        file = request.FILES['file']
        
        # Generate a unique filename
        ext = file.name.split('.')[-1]
        filename = f"{uuid.uuid4()}.webp"
        
        # Define the path to save the image
        filepath = os.path.join(settings.MEDIA_ROOT, 'post_images', filename)
        
        # Open the image and convert to WebP
        try:
            with Image.open(file) as img:
                img.save(filepath, 'WEBP')
            
            # Get the URL for the saved image
            file_url = os.path.join(settings.MEDIA_URL, 'post_images', filename).replace('\\', '/')
            
            return JsonResponse({'location': file_url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Invalid request'}, status=400)


def blog_list(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    
    tags = Tag.objects.all()
    return render(request, 'blog/index.html', {'posts': posts, 'tags': tags})


def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.views += 1
    post.save()
    comments = post.comments.all().order_by('created_at')
    tags = Tag.objects.all()
    
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

    return render(request, 'blog/article.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'tags': tags
    })

def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(tags=tag).order_by('-created_at')
    tags = Tag.objects.all()
    context = {
        'tag': tag,
        'posts': posts,
        'tags': tags
    }
    return render(request, 'blog/category.html', context)


@login_required
def author_dash(request):
    author_posts = Post.objects.filter(author=request.user)
    total_articles = author_posts.count()
    recent_articles = author_posts.order_by('-created_at')[:5]
    total_views = 0
    total_earnings = 0
    context = {
        'total_articles': total_articles,
        'total_views': total_views,
        'total_earnings': total_earnings,
        'recent_articles': recent_articles,
    }
    return render(request, "blog/author/index.html", context)

@login_required
def author_myarticle(request):
    author_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    context = {
        'posts': author_posts,
    }
    return render(request, "blog/author/articles.html", context)

@login_required
def author_createarticle(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
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
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('author_settings')
    else:
        form = ProfileForm(instance=request.user)
    
    context = {
        'form': form
    }
    return render(request, "blog/author/settings.html", context)
