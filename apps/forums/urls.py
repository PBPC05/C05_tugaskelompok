from django.urls import path
from . import views

app_name = "forums"

urlpatterns = [
    path('', views.forums_list_view, name='list'),
    path('create/', views.forums_create_view, name='create_forum'),
    path('<uuid:pk>/', views.forum_detail_view, name='show_forum_detail'),
    path('<uuid:pk>/edit/', views.forums_edit_view, name='edit_forum'),
    path('<uuid:pk>/delete/', views.forums_delete_view, name='delete_forum'),

    path('api/json/', views.forums_list_json, name='show_json'),
    path('api/<uuid:pk>/', views.forum_detail_json, name='detail_json'),

    path('<uuid:pk>/like/', views.forum_like_toggle, name='like_forum'),
    path('reply/<int:reply_id>/like/', views.reply_like_toggle, name='like_reply'),
    path('<uuid:pk>/reply/create/', views.create_reply, name='create_reply'),
    path('reply/<int:reply_id>/delete/', views.delete_reply, name='delete_reply'),
]
