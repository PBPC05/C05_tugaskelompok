from django.urls import path
from news.views import show_main, create_news, show_news_create
app_name = 'news'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-news/', show_news_create, name='create_news')
]