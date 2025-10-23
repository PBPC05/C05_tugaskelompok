from django.db.models import Sum, Count, Q, F
from .models import Driver, Team, Race, Circuit
from django.db.models.functions import Coalesce
import csv
from pathlib import Path

def _sprint_points_by_driver(season: int) -> dict[int, float]:
    csv_path = Path("apps/information/csv/Formula1_2025Season_SprintResults.csv")
    if not csv_path.exists():
        return {}

    pts = {}
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        for row in reader:
            track = (row.get("Track") or "").strip()
            if not track:
                continue

            race = None
            circuit = Circuit.objects.filter(name=track).first()
            if circuit:
                race = (Race.objects
                        .filter(circuit=circuit, season=season)
                        .order_by("-round_number")
                        .first())
            if not race:
                race = (Race.objects
                        .filter(name=track, season=season)
                        .order_by("-round_number")
                        .first())
            if not race:
                continue 

            num = row.get("No")
            driver = None
            if num and str(num).strip().isdigit():
                driver = Driver.objects.filter(number=int(num)).first()
            if not driver:
                drv_name = (row.get("Driver") or "").strip()
                driver = Driver.objects.filter(full_name=drv_name).first()
            if not driver:
                continue

            try:
                p = float((row.get("Points") or "0").strip())
            except ValueError:
                p = 0.0

            pts[driver.id] = pts.get(driver.id, 0.0) + p

    return pts

def driver_standings(season: int):
    qs = (Driver.objects
        .filter(
            Q(race_results__race__season=season) |
            Q(team__isnull=False)
        )
        .select_related("team")
        .annotate(
            gp_points=Coalesce(
                Sum("race_results__points_awarded",
                    filter=Q(race_results__race__season=season)),
                0.0
            ),
            season_wins=Count(
                "race_results",
                filter=Q(race_results__race__season=season,
                         race_results__finish_position=1)
            ),
        ))

    sprint_pts = _sprint_points_by_driver(season)
    for d in qs:
        d.sprint_points = sprint_pts.get(d.id, 0.0)
        d.season_points = float(d.gp_points) + float(d.sprint_points)

    qs = sorted(qs, key=lambda d: (-d.season_points, -d.season_wins, d.full_name))
    return qs


def constructor_standings(season: int):
    qs = (Team.objects
        .filter(race_results__race__season=season)
        .annotate(
            gp_points=Coalesce(
                Sum("race_results__points_awarded",
                    filter=Q(race_results__race__season=season)),
                0.0
            ),
            season_wins=Count(
                "race_results",
                filter=Q(race_results__race__season=season,
                         race_results__finish_position=1)
            ),
        ))

    sprint_pts_driver = _sprint_points_by_driver(season)
    driver_team = {d.id: d.team_id for d in Driver.objects.all()}
    from collections import defaultdict
    sprint_pts_team = defaultdict(float)
    for drv_id, pts in sprint_pts_driver.items():
        tid = driver_team.get(drv_id)
        if tid:
            sprint_pts_team[tid] += pts

    for t in qs:
        t.sprint_points = sprint_pts_team.get(t.id, 0.0)
        t.season_points = float(t.gp_points) + float(t.sprint_points)

    qs = sorted(qs, key=lambda t: (-t.season_points, -t.season_wins, t.name))
    return qs