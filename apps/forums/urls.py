from django.urls import path
from apps.forums.views import *

app_name = "forums"

urlpatterns = [
    path('', forums_list_view, name='list'),
    path('create/', forums_create_view, name='create_forum'),
    path('<uuid:pk>/', forum_detail_view, name='show_forum_detail'),
    path('<uuid:pk>/edit/', forums_edit_view, name='edit_forum'),
    path('<uuid:pk>/delete/', forums_delete_view, name='delete_forum'),

    path('api/json/', forums_list_json, name='show_json'),
    path('api/<uuid:pk>/', forum_detail_json, name='detail_json'),

    path('<uuid:pk>/like/', forum_like_toggle, name='like_forum'),
    path('reply/<int:reply_id>/like/', reply_like_toggle, name='like_reply'),
    path('<uuid:pk>/reply/create/', create_reply, name='create_reply'),
    path('reply/<int:reply_id>/delete/', delete_reply, name='delete_reply'),

    path('<uuid:pk>/replies/load-more/', load_more_replies, name='load_more_replies'),
]
