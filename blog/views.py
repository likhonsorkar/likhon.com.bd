from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment
from blog.forms import CommentForm

# Create your views here.
def blog(request):
    return render(request, "blog/index.html")
def post(request, slug):
    return render(request, "blog/article.html")
@login_required
def author_dash(request):
    return render(request, "blog/author/index.html")
@login_required
def author_myarticle(request):
    return render(request, "blog/author/articles.html")
@login_required
def author_createarticle(request):
    return render(request, "blog/author/create.html")
@login_required
def author_settings(request):
    return render(request, "blog/author/settings.html")

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('created_at')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login') # Or your login URL name
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })
