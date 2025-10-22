from django.urls import path
from apps.prediction.views import show_main, post_vote

app_name = 'prediction'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('post_vote', post_vote, name='post_vote')
]