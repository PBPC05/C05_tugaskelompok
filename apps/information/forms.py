from django import forms
from .models import Driver, Team, DriverRaceResult

class DriverEditableForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = [
            "podiums", "points", "grands_prix_entered",
            "world_championships", "highest_race_finish", "highest_grid_position",
        ]

class TeamEditableForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            "world_championships", "highest_race_finish",
            "pole_positions", "fastest_laps",
        ]

class RaceResultAppendForm(forms.ModelForm):
    class Meta:
        model = DriverRaceResult
        fields = [
            "race", "driver", "team", "grid_position", "finish_position",
            "status", "points_awarded", "fastest_lap", "laps", "time_text",
        ]
