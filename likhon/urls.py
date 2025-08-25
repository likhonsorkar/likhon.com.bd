from django.contrib import admin
from django.urls import path, include
from portfolio.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name="homepage" ),
    path('portfolio/', include('portfolio.urls')),
    path('blog/', include('blog.urls')),
]
