from django.urls import path
from apps.authentication.views import register, login_user, logout_user
from apps.authentication.views import manage_users, edit_user, delete_user, ban_user
from apps.authentication.views import user_dashboard, edit_profile, view_profile

app_name = 'authentication'

urlpatterns = [
    # Authentication
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    # User Dashboard & profile
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/<str:username>/', view_profile, name='view_profile'),

    # Admin - User management
    path('manage_users/', manage_users, name='manage_users'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('ban_user/<int:user_id>/', ban_user, name='ban_user'),
    # todo tambahin path untuk drivers, team result dari faiq
]