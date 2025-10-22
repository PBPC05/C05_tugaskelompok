from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=250)
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
    color = models.CharField(max_length=7)

    team_logo = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("team_detail", kwargs={"slug": self.slug})
    
class Driver(models.Model):
    full_name = models.CharField(max_length=120, unique=True)
    number = models.PositiveIntegerField(unique=True, db_index=True)
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="drivers")

    number_image = models.URLField(blank=True)
    driver_image = models.URLField(blank=True)

    abbreviation = models.CharField(max_length=8, blank=True)
    country = models.CharField(max_length=80, blank=True)
    place_of_birth = models.CharField(max_length=120, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    grands_prix_entered = models.PositiveIntegerField(default=0)
    highest_grid_position = models.CharField(max_length=50, blank=True)
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
    
    def get_absolute_url(self):
        return reverse("driver_detail", kwargs={"slug": self.slug})
    
class Circuit(models.Model):
    name = models.CharField(max_length=100, unique=True)
    long_name = models.CharField(max_length=250)
    country = models.CharField(max_length=80, blank=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    circuit_image = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("circuit_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name
    
class Race(models.Model):
    season = models.PositiveIntegerField(db_index=True)
    round_number = models.PositiveIntegerField()
    name = models.CharField(max_length=120)
    circuit = models.ForeignKey(Circuit, on_delete=models.PROTECT, related_name="races")
    date = models.DateField(null=True, blank=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    class Meta:
        unique_together = ("season", "round_number")
        ordering = ["season", "round_number"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.season} {self.name}")
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("race_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.name} {self.season}"
    
class DriverRaceResult(models.Model):
    STATUS = [
        ("FINISHED", "Finished"),
        ("RET", "Retired"),
        ("DNF", "DNF"),
        ("DSQ", "Disqualified"),
        ("DNS", "DNS"),
        ("WD",  "Withdrawn"),
    ]

    race   = models.ForeignKey(Race,   on_delete=models.CASCADE, related_name="driver_results")
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name="race_results")
    team   = models.ForeignKey(Team,   on_delete=models.PROTECT, related_name="race_results")

    grid_position   = models.PositiveIntegerField(null=True, blank=True)
    finish_position = models.PositiveIntegerField(null=True, blank=True) 
    status          = models.CharField(max_length=10, choices=STATUS, default="FINISHED")
    points_awarded  = models.FloatField(default=0.0)
    fastest_lap     = models.BooleanField(default=False)
    laps            = models.PositiveIntegerField(null=True, blank=True)
    time_text       = models.CharField(max_length=64, blank=True)

    class Meta:
        unique_together = ("race", "driver")
        ordering = ["race__round_number", "finish_position"]

    def cell_display(self):
        return str(self.finish_position) if self.finish_position else self.status

    def __str__(self):
        return f"{self.race} - {self.driver} ({self.cell_display()})"
    
class DriverStanding(models.Model):
    season   = models.PositiveIntegerField(db_index=True)
    driver   = models.ForeignKey("Driver", on_delete=models.CASCADE, related_name="standings")
    points   = models.FloatField(default=0.0)
    wins     = models.PositiveIntegerField(default=0)
    position = models.PositiveIntegerField()

    class Meta:
        unique_together = ("season", "driver")
        ordering = ["position"]

    def __str__(self):
        return f"{self.season} - {self.position}. {self.driver}"


class ConstructorStanding(models.Model):
    season   = models.PositiveIntegerField(db_index=True)
    team     = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="standings")
    points   = models.FloatField(default=0.0)
    wins     = models.PositiveIntegerField(default=0)
    position = models.PositiveIntegerField()

    class Meta:
        unique_together = ("season", "team")
        ordering = ["position"]

    def __str__(self):
        return f"{self.season} - {self.position}. {self.team}"

