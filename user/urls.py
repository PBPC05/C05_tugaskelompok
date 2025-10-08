from django.urls import path
from user.views import show_main

app_name = 'user'

urlpatterns = [
    path('', show_main, name='show_main'),
]