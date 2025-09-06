from django.contrib import admin
from django.urls import path
from blog.views import blog, post, author_dash, author_createarticle, author_myarticle,author_settings

urlpatterns = [
    path('', blog,  name='blog'),
    path('details/<str:slug>/', post,  name='postdetail'),
    path('dashboard/', author_dash,  name='author_dash'),
    path('dashboard/my-article/', author_myarticle,  name='myarticle'),
    path('dashboard/create-article', author_createarticle,  name='newarticle'),
    path('dashboard/settings', author_settings,  name='authorsettings'),
]
