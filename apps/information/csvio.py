import csv
from datetime import datetime
from .models import Driver, Team, DriverRaceResult, Circuit, Race

def export_drivers_csv():
    """Export all drivers to CSV file."""
    drivers = Driver.objects.all().order_by('team.id')
    with open('apps/information/csv/Formula1_2025season_drivers.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Driver', 'Abbreviation', 'No', 'Team', 'Country', 'Podiums', 'Points', 'Grands Prix Entered',
            'World Championships', 'Highest Race Finish', 'Highest Grid Position', 'Date of Birth', 'Place of Birth'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for driver in drivers:
            writer.writerow({
                'Driver': driver.full_name,
                'Abbreviation': driver.abbreviation,
                'No': driver.number,
                'Team': driver.team.name,
                'Country': driver.country,
                'Podiums': driver.podiums,
                'Points': driver.points,
                'Grands Prix Entered': driver.grands_prix_entered,
                'World Championships': driver.world_championships,
                'Highest Race Finish': driver.highest_race_finish,
                'Highest Grid Position': driver.highest_grid_position,
                'Date of Birth': driver.date_of_birth.strftime('%d/%m/%Y') if driver.date_of_birth else '',
                'Place of Birth': driver.place_of_birth,
            })

def export_teams_csv():
    """Export all teams to CSV file."""
    teams = Team.objects.all().order_by('id')
    with open('apps/information/csv/Formula1_2025season_teams.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Team', 'Full Team Name', 'Base', 'Team Chief', 'Technical Chief', 'Chassis', 'Power Unit',
            'First Team Entry', 'World Championships', 'Highest Race Finish', 'Pole Positions', 'Fastest Laps', 'Color'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for team in teams:
            writer.writerow({
                'Team': team.name,
                'Full Team Name': team.full_name,
                'Base': team.base,
                'Team Chief': team.team_chief,
                'Technical Chief': team.technical_chief,
                'Chassis': team.chassis,
                'Power Unit': team.power_unit,
                'First Team Entry': team.first_team_entry,
                'World Championships': team.world_championships,
                'Highest Race Finish': team.highest_race_finish,
                'Pole Positions': team.pole_positions,
                'Fastest Laps': team.fastest_laps,
                'Color': team.color,
            })

def append_raceresult_csv(race_result):
    """Append a single race result to the CSV file."""
    with open('apps/information/csv/Formula1_2025Season_RaceResults.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Track', 'Position', 'No', 'Driver', 'Team', 'Starting Grid', 'Laps', 'Time/Retired', 'Points',
            'Set Fastest Lap', 'Fastest Lap Time'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            'Track': race_result.race.name,
            'Position': race_result.finish_position or race_result.status,
            'No': race_result.driver.number,
            'Driver': race_result.driver.full_name,
            'Team': race_result.team.name,
            'Starting Grid': race_result.grid_position,
            'Laps': race_result.laps,
            'Time/Retired': race_result.time_text,
            'Points': race_result.points_awarded,
            'Set Fastest Lap': 'Yes' if race_result.fastest_lap else 'No',
            'Fastest Lap Time': '',
        })

def import_circuits_csv():
    """Import circuits from CSV file."""
    with open('apps/information/csv/Formula1_2025Season_circuits.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Circuit.objects.get_or_create(
                name=row['name'],
                defaults={
                    'long_name': row['long_name'],
                    'country': row['country'],
                }
            )

def import_races_csv():
    """Import races from CSV file."""
    with open('apps/information/csv/Formula1_2025Season_races.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            circuit = Circuit.objects.get(name=row['circuit_name'])
            Race.objects.get_or_create(
                season=int(row['season']),
                round_number=int(row['round_number']),
                defaults={
                    'name': row['name'],
                    'circuit': circuit,
                    'date': datetime.strptime(row['date'], '%Y-%m-%d').date() if row['date'] else None,
                }
            )

def import_drivers_csv():
    """Import drivers from CSV file."""
    with open('apps/information/csv/Formula1_2025season_drivers.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            team_name = (row.get("Team") or "").strip()
            team = None
            if team_name:
                team = Team.objects.filter(name=team_name).first()
            Driver.objects.get_or_create(
                full_name=row['Driver'],
                defaults={
                    'number': int(row['No']),
                    'team': team,
                    'abbreviation': row['Abbreviation'],
                    'country': row['Country'],
                    'podiums': int(row['Podiums']),
                    'points': float(row['Points']),
                    'grands_prix_entered': int(row['Grands Prix Entered']),
                    'world_championships': int(row['World Championships']),
                    'highest_race_finish': row['Highest Race Finish'],
                    'highest_grid_position': row['Highest Grid Position'],
                    'date_of_birth': datetime.strptime(row['Date of Birth'], '%d/%m/%Y').date() if row['Date of Birth'] else None,
                    'place_of_birth': row['Place of Birth'],
                    'number_image' : row['Number Logo'],
                    'driver_image' : row['Driver Image']
                }
            )

def import_teams_csv():
    """Import teams from CSV file."""
    with open('apps/information/csv/Formula1_2025season_teams.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Team.objects.get_or_create(
                name=row['Team'],
                defaults={
                    'full_name': row['Full Team Name'],
                    'base': row['Base'],
                    'team_chief': row['Team Chief'],
                    'technical_chief': row['Technical Chief'],
                    'chassis': row['Chassis'],
                    'power_unit': row['Power Unit'],
                    'first_team_entry': int(row['First Team Entry']) if row['First Team Entry'] else None,
                    'world_championships': int(row['World Championships']),
                    'highest_race_finish': row['Highest Race Finish'],
                    'pole_positions': int(row['Pole Positions']),
                    'fastest_laps': int(row['Fastest Laps']),
                    'color': row['Color'],
                    'team_logo': row['Logo']
                }
            )

def import_raceresult_csv():
    """Import race results from CSV file."""
    with open('apps/information/csv/Formula1_2025Season_RaceResults.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            track = (row.get("Track") or "").strip()
            circuit = Circuit.objects.filter(name=track).first()
            race = Race.objects.get(circuit=circuit)
            driver = Driver.objects.get(number=int(row['No']))
            team = Team.objects.get(name=row['Team'])
            DriverRaceResult.objects.get_or_create(
                race=race,
                driver=driver,
                defaults={
                    'team': team,
                    'grid_position': int(row['Starting Grid']) if row['Starting Grid'] else None,
                    'finish_position': int(row['Position']) if row['Position'].isdigit() else None,
                    'status': row['Position'] if not row['Position'].isdigit() else 'FINISHED',
                    'points_awarded': float(row['Points']),
                    'fastest_lap': row['Set Fastest Lap'] == 'Yes',
                    'laps': int(row['Laps']) if row['Laps'] else None,
                    'time_text': row['Time/Retired'],
                }
            )

