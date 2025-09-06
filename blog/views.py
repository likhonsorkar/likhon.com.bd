from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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