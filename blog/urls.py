from django.urls import path
from blog.views import (
    blog_list,
    blog_detail,
    posts_by_tag,
    author_dash,
    author_myarticle,
    author_createarticle,
    author_edit_article,
    author_delete_article,
    author_settings,
    image_upload_view
)

urlpatterns = [
    path('', blog_list, name='blog'),
    path('detail/<str:slug>/', blog_detail, name='blog_detail'),
    path('tag/<str:tag_name>/', posts_by_tag, name='posts_by_tag'),
    path('dashboard/', author_dash, name='author_dash'),
    path('dashboard/my-articles/', author_myarticle, name='author_myarticle'),
    path('dashboard/create-article/', author_createarticle, name='author_createarticle'),
    path('dashboard/edit-article/<str:slug>/', author_edit_article, name='author_edit_article'),
    path('dashboard/delete-article/<str:slug>/', author_delete_article, name='author_delete_article'),
    path('dashboard/settings/', author_settings, name='author_settings'),
    path('image-upload/', image_upload_view, name='image_upload'),
]
