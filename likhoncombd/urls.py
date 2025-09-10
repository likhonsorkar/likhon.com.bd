"""
URL configuration for likhoncombd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.core.views import home, contact, signin, signup, logout_view, working, accessdenied, career
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="homepage"),
    path('blog/', include('apps.blog.urls')),
    path('accounts/signin/', signin, name="signin"),
    path('accounts/signup/', signup, name="signup"),
    path('accounts/logout', logout_view, name="logout"),
    path('contact/', contact, name="contact"),
    path('working/', working, name="working"),
    path('no-access', accessdenied, name="noaccess"),
    path('career/', career, name="career")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
