from django.urls import path
from apps.prediction.views import *

app_name = 'prediction'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('post_vote', post_vote, name='post_vote'),
    path('json', get_votes_json, name='get_votes_json'),
    path('clear_votes', clear_votes, name='clear_votes'),
    path('post_vote_flutter', post_vote_flutter, name='post_vote_flutter'),
    path('clear_votes_flutter', clear_votes_flutter, name='clear_votes_flutter'),
    path('check_user', check_user, name='check_user'),
    path('check_admin', check_admin, name='check_admin'),
]