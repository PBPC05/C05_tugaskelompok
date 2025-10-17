from django.db import models
from django.utils.text import slugify

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    base = models.CharField(max_length=100, blank=True)
    team_chief = models.CharField(max_length=100, blank=True)
    technical_chief = models.CharField(max_length=100, blank=True)
    chassis = models.CharField(max_length=100, blank=True)
    power_unit = models.CharField(max_length=100, blank=True)
    first_team_entry = models.PositiveIntegerField(null=True, blank=True)
    world_championships = models.PositiveIntegerField(default=0)
    pole_positions = models.PositiveIntegerField(default=0)
    fastest_laps = models.PositiveIntegerField(default=0)
    highest_race_finish = models.CharField(max_length=20, blank=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Driver(models.Model):
    full_name = models.CharField(max_length=120, unique=True)
    number = models.PositiveIntegerField(unique=True, db_index=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="drivers")

    abbreviation = models.CharField(max_length=8, blank=True)
    country = models.CharField(max_length=80, blank=True)
    place_of_birth = models.CharField(max_length=120, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    grands_prix_entered = models.PositiveIntegerField(default=0)
    highest_grid_position = models.PositiveIntegerField(default=0)
    highest_race_finish = models.CharField(max_length=50, blank=True)
    podiums = models.PositiveIntegerField(default=0)
    points = models.FloatField(default=0.0)
    world_championships = models.PositiveIntegerField(default=0)

    slug = models.SlugField(max_length=150, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
    
