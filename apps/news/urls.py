from django.urls import path
from apps.news.views import show_main, show_news_create, create_news

app_name = 'news'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-news/', show_news_create, name='create_news')
]