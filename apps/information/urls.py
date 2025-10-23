from django.urls import path
from .views import *

app_name = 'information'

urlpatterns = [
    path('drivers/', show_drivers, name='show_drivers'),
    path('drivers/<slug:slug>/', driver_detail, name='driver_detail'),
    path('teams/', show_teams, name='show_teams'),
    path('teams/<slug:slug>/', team_detail, name='team_detail'),
    path('standings/', show_standings, name='show_standings'),
    path('schedule/', show_schedule, name='show_schedule'),
    path('races/<slug:slug>/', race_detail, name='race_detail'),
    path('api/drivers/', show_drivers_json, name='show_drivers_json'),
    path("api/drivers/<slug:slug>/", show_drivers_json_detail, name="show_driver_json_detail"),
    path('api/teams/', show_teams_json, name='show_teams_json'),
    path("api/teams/<slug:slug>/", show_teams_json_detail, name="show_team_json_detail"),
    path('api/standings/drivers/2025/', show_driver_standings_json, name='show_driver_standings_json'),
    path('api/standings/constructors/2025/', show_constructor_standings_json, name='show_constructor_standings_json'),
    path('api/schedule/2025/', show_schedule_json, name='show_schedule_json'),
    path("api/races/<slug:slug>/", show_races_json_detail, name="show_races_json_detail"),
]