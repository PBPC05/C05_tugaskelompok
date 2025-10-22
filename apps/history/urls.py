from django.urls import path
from apps.history.views import show_main, driver_user_page, driver_admin_page
from apps.history.views import add_driver, delete_driver, edit_driver
app_name = 'history'

urlpatterns = [
    # path('', show_main, name='show_main'),
    path('driver/admin', driver_admin_page, name='driver_admin_page'),
    path('driver/user', driver_user_page, name='driver_user_page'),

    # endpoints AJAX nya
    path('driver/add/', add_driver, name='add_driver'),
    path('driver/delete/<int:driver_id>/', delete_driver, name='delete_driver'),
    path('driver/edit/<int:driver_id>/', edit_driver, name='edit_driver'),
]