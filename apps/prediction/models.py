from django.db import models

class PredictionVote(models.Model):
    TYPE_SELECTIONS = {
        'driver': "Driver",
        'team': "Team"
    }

    # user
    type = models.CharField(max_length=20, choices=TYPE_SELECTIONS, default="driver")
    race = models.CharField(max_length=255)
    content = models.CharField(max_length=255)