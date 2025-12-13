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

    path('<uuid:pk>/hot-toggle/', toggle_hot_forum, name='hot_toggle_forum'),


    path('api/<uuid:pk>/replies/', forum_replies_json, name='forum_replies_json'),
    path('<uuid:pk>/create-reply-flutter/', create_reply_flutter, name='create_reply_flutter'),
    path('reply/<int:reply_id>/delete-flutter/', delete_reply_flutter, name='delete_reply_flutter'),
    path('reply/<int:reply_id>/like-flutter/', toggle_reply_like_flutter, name='toggle_reply_like_flutter'),
    path('create-forum-flutter/', create_forum_flutter, name='create_forum_flutter'),
    path('<uuid:pk>/update-forum-flutter/', update_forum_flutter, name='update_forum_flutter'),
    path('<uuid:pk>/delete-forum-flutter/', delete_forum_flutter, name='delete_forum_flutter'),
    path('<uuid:pk>/like-forum-flutter/', toggle_forum_like_flutter, name='toggle_forum_like_flutter'),
    path('<uuid:pk>/toggle-hot-flutter/', toggle_hot_forum_flutter, name='toggle_hot_forum_flutter'),
    path('api/check-admin/', check_admin, name='check_admin'),
    path('api/user/profile/', get_user_profile, name='user_profile'),
]
