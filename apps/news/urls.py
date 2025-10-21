from django.urls import path
from apps.news.views import *

app_name = 'news'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('<uuid:news_id>/', show_news_detail, name='show_news_detail'),
    path('create-news/', show_news_create, name='create_news'),
    path('create-news/post', create_news, name='create_news_ajax'),
    path('<uuid:news_id>/edit', show_news_edit, name='edit_news'),
    path('<uuid:news_id>/edit/post', edit_news_ajax, name='edit_news_ajax'),
    path('<uuid:news_id>/delete', delete_news, name='delete_news'),
    path('json/', show_json, name='show_json'),
    path('json/<uuid:news_id>', show_json_by_id, name='show_json_by_id')
]