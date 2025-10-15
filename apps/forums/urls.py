from django.urls import path
from apps.forums.views import show_main

app_name = 'forums'

urlpatterns = [
    path('', show_main, name='show_main'),
]