from django.db import models

# Create your models here.
class Driver(models.Model):
    podiums = models.PositiveIntegerField()
    driver_name = models.CharField(max_length=255)
    nationality = models.CharField(max_length=150)
    car = models.CharField(max_length=150)
    points = models.FloatField()
    year = models.PositiveIntegerField(null=True, blank=True)
    driver_code = models.CharField(max_length=10, null=True, blank=True)

    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.driver_name
    
class Winner(models.Model):
    grand_prix = models.CharField(max_length=255)
    date = models.DateField()
    winner = models.CharField(max_length=255)
    car = models.CharField(max_length=150)
    laps = models.FloatField(null=True, blank=True)
    time = models.CharField(max_length=100)
    name_code = models.CharField(max_length=10, null=True, blank=True)
    
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.winner} - {self.grand_prix}"
