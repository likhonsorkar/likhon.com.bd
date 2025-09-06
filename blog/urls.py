from django.urls import path
from blog.views import (
    blog_list,
    blog_detail,
    author_dash,
    author_myarticle,
    author_createarticle,
    author_settings
)

urlpatterns = [
    path('', blog_list, name='blog'),
    path('detail/<str:slug>/', blog_detail, name='blog_detail'),
    path('dashboard/', author_dash, name='author_dash'),
    path('dashboard/my-articles/', author_myarticle, name='author_myarticle'),
    path('dashboard/create-article/', author_createarticle, name='author_createarticle'),
    path('dashboard/settings/', author_settings, name='author_settings'),
]
