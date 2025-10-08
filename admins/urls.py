from django.urls import path
from admins.views import show_main

app_name = 'admins'

urlpatterns = [
    path('', show_main, name='show_main'),
]