from django.urls import path
from apps.prediction.views import show_main, post_vote, get_votes_json, clear_votes, post_vote_flutter

app_name = 'prediction'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('post_vote', post_vote, name='post_vote'),
    path('json', get_votes_json, name='get_votes_json'),
    path('clear_votes', clear_votes, name='clear_votes'),
    path('post_vote_flutter', post_vote_flutter, name='post_vote_flutter')
]