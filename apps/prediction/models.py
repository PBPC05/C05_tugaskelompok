from django.db import models
from django.contrib.auth.models import User

class PredictionVote(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=20, default="driver")
    race = models.CharField(max_length=255)
    content = models.CharField(max_length=255)