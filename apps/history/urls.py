from django.urls import path
from apps.history.views import driver_user_page, driver_admin_page
from apps.history.views import add_driver, delete_driver, edit_driver
from apps.history.views import winner_user_page, winner_admin_page
from apps.history.views import add_winner, delete_winner, edit_winner

from apps.history.views import api_drivers, api_winners, proxy_image

app_name = 'history'

urlpatterns = [
    # Path buat history driver page nya
    path('driver/admin', driver_admin_page, name='driver_admin_page'),
    path('driver/user', driver_user_page, name='driver_user_page'),

    # Endpoints AJAX nya
    path('driver/add/', add_driver, name='add_driver'),
    path('driver/delete/<int:driver_id>/', delete_driver, name='delete_driver'),
    path('driver/edit/<int:driver_id>/', edit_driver, name='edit_driver'),

    # Path buat history winner page nya
    path('winner/user', winner_user_page, name='winner_user_page'),
    path('winner/admin', winner_admin_page, name='winner_admin_page'),

    # AJAX endpoints
    path('winner/add/', add_winner, name='add_winner'),
    path('winner/delete/<int:winner_id>/', delete_winner, name='delete_winner'),
    path('winner/edit/<int:winner_id>/', edit_winner, name='edit_winner'),

    # API JSON khusus Flutter
    path('api/drivers/', api_drivers, name='api_drivers'),
    path('api/winners/', api_winners, name='api_winners'),

    # utk proxy image nya flutter
    path("proxy-image/", proxy_image, name="proxy_image"),
]