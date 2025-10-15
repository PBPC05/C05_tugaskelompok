from django.urls import path
from apps.news.views import show_main

app_name = 'news'

urlpatterns = [
    path('', show_main, name='show_main'),
]