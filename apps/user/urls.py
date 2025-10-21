from django.urls import path
from apps.news.views import show_main, create_news, show_news_create
app_name = 'user'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-news/', show_news_create, name='create_news')
] 