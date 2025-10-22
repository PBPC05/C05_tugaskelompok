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