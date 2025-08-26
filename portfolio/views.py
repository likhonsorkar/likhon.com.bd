from django.shortcuts import render
from portfolio.models import Service, Project, Review

# Create your views here.
def homepage(request):
    services = Service.objects.all()
    projects = Project.objects.all()
    reviews =  Review.objects.filter(is_approved=True)
    context = {
        'services': services,
        'projects': projects,
        'reviews': reviews,
    }
    return render(request, "home.html", context)