from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import PredictionVote
import uuid

# Create your tests here.
class PredictionTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="Verstappen", password="1234")
        self.driver_vote = PredictionVote.objects.create(vote_type="driver", race="2025 Mexico City Grand Prix", content="Max Verstappen")
        self.team_vote = PredictionVote.objects.create(vote_type="team", race="2025 Mexico City Grand Prix", content="Red Bull")

    def test_votes_model(self):
        self.assertTrue(self.driver_vote.vote_type, "driver")
        self.assertTrue(self.driver_vote.race, "2025 Mexico City Grand Prix")
        self.assertTrue(self.driver_vote.content, "Max Verstappen")
        self.assertTrue(self.team_vote.vote_type, "team")
        self.assertTrue(self.team_vote.race, "2025 Mexico City Grand Prix")
        self.assertTrue(self.team_vote.content, "Red Bull")

    def test_post_vote(self):
        self.client.login(username="Verstappen", password="1234")

        post_url = reverse("prediction:post_vote")
        response = self.client.post(post_url, {"vote_type": "driver", "race": "2025 Mexico City Grand Prix", "content": "Esteban Ocon"})

        self.assertTrue(PredictionVote.objects.filter(user=self.user).exists())
