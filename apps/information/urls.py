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
    path('admin/drivers/', manage_driver, name='manage_driver'),
    path('driver/<int:pk>/update/ajax/', driver_update_ajax, name='driver_update_ajax'),
    path('admin/drivers/flutter/<int:pk>/update/', driver_update_flutter, name='driver_update_flutter'),
    path('admin/teams/', manage_teams, name='manage_teams'),
    path('team/<int:pk>/update/ajax/', team_update_ajax, name='team_update_ajax'),
    path('admin/teams/flutter/<int:pk>/update/', team_update_flutter, name='team_update_flutter'),
    path('admin/results/', manage_results, name='manage_results'),
    path('result/append/ajax/', raceresult_append_ajax, name='raceresult_append_ajax'),
    path('result/<int:pk>/delete/ajax/', raceresult_delete_ajax, name='raceresult_delete_ajax'),
    path('api/manage/results/', manage_results_json, name='manage_results_json'),
    path('raceresult/append/flutter/', raceresult_append_flutter, name='raceresult_append_flutter'),
    path('raceresult/<int:pk>/delete/flutter/', raceresult_delete_flutter, name='raceresult_delete_flutter'),
]