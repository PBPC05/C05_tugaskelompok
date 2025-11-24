from django.urls import path
from apps.news.views import *

app_name = 'news'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('<uuid:news_id>/', show_news_detail, name='show_news_detail'),
    path('create-news/', show_news_create, name='create_news'),
    path('create-news/post', create_news, name='create_news_ajax'),
    path('<str:news_id>/edit', show_news_edit, name='edit_news'),
    path('<str:news_id>/edit/post', edit_news_ajax, name='edit_news_ajax'),
    path('<str:news_id>/delete', delete_news, name='delete_news'),
    path('<str:news_id>/comment', post_comment, name='post_comment'),
    path('json/', show_json, name='show_json'),
    path('json/<str:news_id>', show_json_by_id, name='show_json_by_id'),
    path('json/<str:news_id>/comments', get_comments_json, name='get_comments_json'),
    path('<str:news_id>/comment/<str:comment_id>/delete', delete_comment, name='delete_comment'),
    path('proxy-image/', proxy_image, name="proxy_image"),
    path('create-flutter/', create_news_flutter, name='create_flutter')
]