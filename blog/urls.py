from django.contrib import admin
from django.urls import path
from blog.views import blog, post

urlpatterns = [
    path('', blog,  name='blog'),
    path('<str:slug>/', post,  name='postdetail'),
]
