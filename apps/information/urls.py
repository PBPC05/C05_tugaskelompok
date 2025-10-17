from django.urls import path
from apps.information.views import show_main

app_name = 'information'

urlpatterns = [
    path('', show_main, name='show_main'),
]