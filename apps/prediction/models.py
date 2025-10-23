from django.db import models

class PredictionVote(models.Model):
    vote_type = models.CharField(max_length=20, default="driver")
    race = models.CharField(max_length=255)
    content = models.CharField(max_length=255)