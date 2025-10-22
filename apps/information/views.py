from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import DriverEditableForm, TeamEditableForm, RaceResultAppendForm
from .models import Driver, Team, DriverRaceResult, DriverStanding, ConstructorStanding, Circuit, Race
from .csvio import export_drivers_csv, export_teams_csv, append_raceresult_csv, import_circuits_csv, import_races_csv
from .standings import driver_standings, constructor_standings

@login_required
@require_POST
def driver_update_ajax(request, pk):
    obj = get_object_or_404(Driver, pk=pk)
    form = DriverEditableForm(request.POST, instance=obj)
    if form.is_valid():
        form.save()
        export_drivers_csv()
        return JsonResponse({"ok": True})
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)

@login_required
@require_POST
def team_update_ajax(request, pk): #komen filler aja buat push
    obj = get_object_or_404(Team, pk=pk)
    form = TeamEditableForm(request.POST, instance=obj)
    if form.is_valid():
        form.save()
        export_teams_csv()
        return JsonResponse({"ok": True})
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)

@login_required
@require_POST
def raceresult_append_ajax(request):
    form = RaceResultAppendForm(request.POST)
    if form.is_valid():
        rr = form.save()
        append_raceresult_csv(rr)
        return JsonResponse({"ok": True})
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)

@login_required
@require_POST
def raceresult_delete_ajax(request, pk):
    obj = get_object_or_404(DriverRaceResult, pk=pk)
    obj.delete()
    return JsonResponse({"ok": True})

def standings_driver_json(request, season: int):
    data = [
        {"driver": d.full_name, "team": d.team.name, "points": d.points or 0, "wins": getattr(d, "wins", 0),
         "url": d.get_absolute_url()}
        for d in driver_standings(season)
    ]
    return JsonResponse({"season": season, "data": data})

def teams_json(request):
    data = [{"name": t.name, "url": t.get_absolute_url()} for t in Team.objects.all()]
    return JsonResponse(data, safe=False)

def show_drivers(request):
    drivers = Driver.objects.all().order_by('number')
    return render(request, 'drivers.html', {'drivers': drivers})

def driver_detail(request, slug):
    driver = get_object_or_404(Driver, slug=slug)
    return render(request, 'driver_detail.html', {'driver': driver})

def show_teams(request):
    teams = Team.objects.all().order_by('name')
    return render(request, 'teams.html', {'teams': teams})

def team_detail(request, slug):
    team = get_object_or_404(Team, slug=slug)
    return render(request, 'team_detail.html', {'team': team})

def show_driver_standings(request, season=2025):
    standings = driver_standings(season)
    return render(request, 'driver_standings.html', {'standings': standings, 'season': season})

def show_constructor_standings(request, season=2025):
    standings = constructor_standings(season)
    return render(request, 'constructor_standings.html', {'standings': standings, 'season': season})

def show_drivers_json(request):
    data = [
        {
            'full_name': d.full_name,
            'abbreviation': d.abbreviation,
            'number': d.number,
            'team': d.team.name,
            'country': d.country,
            'podiums': d.podiums,
            'points': d.points,
            'grands_prix_entered': d.grands_prix_entered,
            'world_championships': d.world_championships,
            'highest_race_finish': d.highest_race_finish,
            'highest_grid_position': d.highest_grid_position,
            'date_of_birth': d.date_of_birth.strftime('%d/%m/%Y') if d.date_of_birth else '',
            'place_of_birth': d.place_of_birth,
            'url': d.get_absolute_url(),
        } for d in Driver.objects.all().order_by('team')
    ]
    return JsonResponse(data, safe=False)

def show_teams_json(request):
    data = [
        {
            'name': t.name,
            'full_name': t.full_name,
            'base': t.base,
            'team_chief': t.team_chief,
            'technical_chief': t.technical_chief,
            'chassis': t.chassis,
            'power_unit': t.power_unit,
            'first_team_entry': t.first_team_entry,
            'world_championships': t.world_championships,
            'highest_race_finish': t.highest_race_finish,
            'pole_positions': t.pole_positions,
            'fastest_laps': t.fastest_laps,
            'color': t.color,
            'url': t.get_absolute_url(),
        } for t in Team.objects.all().order_by('name')
    ]
    return JsonResponse(data, safe=False)

def show_constructor_standings_json(request, season=2025):
    data = [
        {"team": t.name, "points": getattr(t, 'points', 0), "wins": getattr(t, 'wins', 0), "url": t.get_absolute_url()}
        for t in constructor_standings(season)
    ]
    return JsonResponse({"season": season, "data": data})

def show_driver_standings_json(request, season=2025):
    data = [
        {"driver": d.full_name, "team": d.team.name, "points": getattr(d, 'points', 0), "wins": getattr(d, 'wins', 0), "url": d.get_absolute_url()}
        for d in driver_standings(season)
    ]
    return JsonResponse({"season": season, "data": data})

def show_schedule(request, season=2025):
    races = Race.objects.filter(season=season).order_by('round_number')
    return render(request, 'schedule.html', {'races': races, 'season': season})

def race_detail(request, slug):
    race = get_object_or_404(Race, slug=slug)
    return render(request, 'race_detail.html', {'race': race})

def show_schedule_json(request, season=2025):
    data = [
        {
            'season': r.season,
            'round_number': r.round_number,
            'name': r.name,
            'circuit': r.circuit.name,
            'date': r.date.strftime('%Y-%m-%d') if r.date else '',
            'url': r.get_absolute_url(),
        } for r in Race.objects.filter(season=season).order_by('round_number')
    ]
    return JsonResponse({"season": season, "data": data})

@login_required
def import_circuits(request):
    import_circuits_csv()
    return JsonResponse({"ok": True})

@login_required
def import_races(request):
    import_races_csv()
    return JsonResponse({"ok": True})
