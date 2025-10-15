from django.urls import path
from apps.history.views import show_main

app_name = 'history'

urlpatterns = [
    path('', show_main, name='show_main'),
]