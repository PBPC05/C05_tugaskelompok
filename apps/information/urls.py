from django.urls import path
from .views import *

app_name = 'information'

urlpatterns = [
    path('drivers/', show_drivers, name='show_drivers'),
    path('drivers/<slug:slug>/', driver_detail, name='driver_detail'),
    path('teams/', show_teams, name='show_teams'),
    path('teams/<slug:slug>/', team_detail, name='team_detail'),
    path('standings/drivers/', show_driver_standings, name='show_driver_standings'),
    path('standings/constructors/', show_constructor_standings, name='show_constructor_standings'),
    path('schedule/', show_schedule, name='show_schedule'),
    path('races/<slug:slug>/', race_detail, name='race_detail'),
    path('api/drivers/', show_drivers_json, name='show_drivers_json'),
    path('api/teams/', show_teams_json, name='show_teams_json'),
    path('api/standings/drivers/<int:season>/', show_driver_standings_json, name='show_driver_standings_json'),
    path('api/standings/constructors/<int:season>/', show_constructor_standings_json, name='show_constructor_standings_json'),
    path('api/schedule/<int:season>/', show_schedule_json, name='show_schedule_json'),
    path('api/raceresult/delete/<int:pk>/', raceresult_delete_ajax, name='raceresult_delete_ajax'),
]