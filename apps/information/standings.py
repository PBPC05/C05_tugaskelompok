from django.db.models import Sum, Count, Q, F
from .models import Driver, Team, DriverRaceResult

def driver_standings(season: int):
    return (Driver.objects
        .filter(race_results__race__season=season)
        .annotate(
            points=Sum("race_results__points_awarded",
                       filter=Q(race_results__race__season=season)),
            wins=Count("race_results",
                       filter=Q(race_results__race__season=season, race_results__finish_position=1)),
        )
        .order_by(F("points").desc(nulls_last=True), F("wins").desc(), "full_name")
    )

def constructor_standings(season: int):
    return (Team.objects
        .filter(race_results__race__season=season)
        .annotate(
            points=Sum("race_results__points_awarded",
                       filter=Q(race_results__race__season=season)),
            wins=Count("race_results",
                       filter=Q(race_results__race__season=season, race_results__finish_position=1)),
        )
        .order_by(F("points").desc(nulls_last=True), F("wins").desc(), "name")
    )
