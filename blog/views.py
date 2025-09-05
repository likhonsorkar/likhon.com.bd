from django.shortcuts import render

# Create your views here.
def blog(request):
    return render(request, "blog/index.html")
def post(request, slug):
    return render(request, "blog/article.html")