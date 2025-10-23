from django.urls import path
from apps.prediction.views import show_main, post_vote, get_votes_json

app_name = 'prediction'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('post_vote', post_vote, name='post_vote'),
    path('json', get_votes_json, name='get_votes_json')
]