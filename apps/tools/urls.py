from django.urls import path
from apps.tools.views import *

app_name = 'tools'

urlpatterns = [
    path('', dashboard, name='toolsdashboard'),
    path('cv-maker/',cv_maker, name='cv_maker'),
]


