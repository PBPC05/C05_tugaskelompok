from django.urls import path
from apps.history.views import show_main, history_page

app_name = 'history'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('history/', history_page, name='history_page'),
]