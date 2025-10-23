import json
import datetime
import uuid 
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from .models import Team, Driver, Circuit, Race, DriverRaceResult


class ModelTests(TestCase):

    def test_team_model(self):
        unique_suffix = uuid.uuid4().hex[:8]
        team_name = f"Team Model Test Team {unique_suffix}"
        team = Team.objects.create(name=team_name, full_name=f"Team Model Test Full Name {unique_suffix}")
        expected_slug = slugify(team_name)
        self.assertEqual(team.__str__(), team_name)
        self.assertEqual(team.slug, expected_slug)
        self.assertEqual(team.get_absolute_url(), f"/information/teams/{team.slug}/")

    def test_driver_model(self):
        unique_suffix = uuid.uuid4().hex[:8]
        team_name = f"Driver Model Test Team {unique_suffix}"
        team = Team.objects.create(name=team_name)

        driver_name = f"Driver Model Test Driver {unique_suffix}"
        driver_number = int(uuid.uuid4().int % 10000) + 1000 
        driver = Driver.objects.create(
            full_name=driver_name,
            number=driver_number,
            team=team
        )
        expected_slug = slugify(driver_name)
        self.assertEqual(driver.__str__(), driver_name)
        self.assertEqual(driver.slug, expected_slug)
        self.assertEqual(driver.get_absolute_url(), f"/information/drivers/{driver.slug}/")

    def test_circuit_model(self):
        unique_suffix = uuid.uuid4().hex[:8]
        circuit_name = f"Circuit Model Test Circuit {unique_suffix}"
        circuit = Circuit.objects.create(name=circuit_name, long_name=f"Circuit Model Test Long Name {unique_suffix}")
        expected_slug = slugify(circuit_name)
        self.assertEqual(circuit.__str__(), circuit_name)
        self.assertEqual(circuit.slug, expected_slug)

    def test_race_model(self):
        unique_suffix = uuid.uuid4().hex[:8]
        circuit_name = f"Race Model Test Circuit {unique_suffix}"
        circuit = Circuit.objects.create(name=circuit_name)

        race_name = f"Race Model Test Race {unique_suffix}"
        race_season = 5000 + int(uuid.uuid4().int % 100)
        race_round = 200 + int(uuid.uuid4().int % 50)
        race = Race.objects.create(
            season=race_season,
            round_number=race_round,
            name=race_name,
            circuit=circuit
        )
        expected_slug = slugify(f"{race.season} {race.name}")
        self.assertEqual(race.__str__(), f"{race_name} {race.season}")
        self.assertEqual(race.slug, expected_slug)
        self.assertEqual(race.get_absolute_url(), f"/information/races/{race.slug}/")

    def test_driver_race_result_model(self):
        unique_suffix = uuid.uuid4().hex[:8]
        team_name = f"Result Model Test Team {unique_suffix}"
        team = Team.objects.create(name=team_name)

        driver_name_1 = f"Result Model Test Driver 1 {unique_suffix}"
        driver_number_1 = int(uuid.uuid4().int % 10000) + 11000 
        driver_1 = Driver.objects.create(full_name=driver_name_1, number=driver_number_1, team=team)

        driver_name_2 = f"Result Model Test Driver 2 {unique_suffix}"
        driver_number_2 = int(uuid.uuid4().int % 10000) + 21000 
        driver_2 = Driver.objects.create(full_name=driver_name_2, number=driver_number_2, team=team)

        circuit_name = f"Result Model Test Circuit {unique_suffix}"
        circuit = Circuit.objects.create(name=circuit_name)

        race_name = f"Result Model Test Race {unique_suffix}"
        race_season = 5100 + int(uuid.uuid4().int % 100)
        race_round = 250 + int(uuid.uuid4().int % 50)
        race = Race.objects.create(
            season=race_season,
            round_number=race_round,
            name=race_name,
            circuit=circuit
        )

        result = DriverRaceResult.objects.create(
            race=race,
            driver=driver_1,
            team=team,
            finish_position=1,
            points_awarded=25
        )
        self.assertEqual(result.__str__(), f"{race} - {driver_1} (1)")
        self.assertEqual(result.cell_display(), "1")

        result_dnf = DriverRaceResult.objects.create(
            race=race,
            driver=driver_2,
            team=team,
            finish_position=None,
            status="DNF"
        )
        self.assertEqual(result_dnf.cell_display(), "DNF")


class ViewAndAPITests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Siapkan data dummy sekali per class"""
        unique_suffix_setup = uuid.uuid4().hex[:8] 
        team_name_setup = f"McLaren Setup {unique_suffix_setup}"
        cls.team = Team.objects.create(
            name=team_name_setup,
            full_name=f"McLaren Formula 1 Team Setup {unique_suffix_setup}",
            color="#f47500",
            team_logo="http://example.com/logo.png"
        )

        driver_name_setup = f"Lando Norris Setup {unique_suffix_setup}"
        driver_slug_setup = slugify(driver_name_setup)
        driver_number_setup = int(uuid.uuid4().int % 10000) + 31000 
        cls.driver = Driver.objects.create(
            full_name=driver_name_setup,
            number=driver_number_setup,
            team=cls.team,
            slug=driver_slug_setup,
            driver_image="http://example.com/driver.png",
            number_image="http://example.com/number.png"
        )

        circuit_name_setup = f"Australia Setup {unique_suffix_setup}"
        cls.circuit = Circuit.objects.create(
            name=circuit_name_setup,
            long_name=f"Melbourne Grand Prix Circuit Setup {unique_suffix_setup}"
        )

        race_season_setup_1 = 6000 + int(uuid.uuid4().int % 100)
        race_round_setup_1 = 300 + int(uuid.uuid4().int % 50)
        race_name_1_setup = f"Australian GP Setup {unique_suffix_setup}"
        race_slug_1_setup = slugify(f"{race_season_setup_1} {race_name_1_setup}") 
        cls.race = Race.objects.create(
            season=race_season_setup_1, 
            round_number=race_round_setup_1, 
            name=race_name_1_setup,
            circuit=cls.circuit,
            date=datetime.date(2025, 3, 16), 
            slug=race_slug_1_setup
        )

        race_season_setup_2 = race_season_setup_1 
        race_round_setup_2 = race_round_setup_1 + 1 
        race_name_2_setup = f"Chinese GP Setup {unique_suffix_setup}"
        race_slug_2_setup = slugify(f"{race_season_setup_2} {race_name_2_setup}") 
        cls.race_no_results = Race.objects.create(
            season=race_season_setup_2,
            round_number=race_round_setup_2,
            name=race_name_2_setup,
            circuit=cls.circuit,
            slug=race_slug_2_setup
        )

        cls.result = DriverRaceResult.objects.create(
            race=cls.race,
            driver=cls.driver,
            team=cls.team,
            finish_position=1,
            points_awarded=25,
            fastest_lap=True,
            time_text="1:30:00.000"
        )


    def test_show_drivers_view(self):
        response = self.client.get(reverse("information:show_drivers"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "drivers.html")

    def test_driver_detail_view(self):
        response = self.client.get(reverse("information:driver_detail", kwargs={"slug": self.driver.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "driver_detail.html")
        self.assertEqual(response.context["driver_slug"], self.driver.slug)

    def test_show_teams_view(self):
        response = self.client.get(reverse("information:show_teams"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "teams.html")

    def test_team_detail_view(self):
        response = self.client.get(reverse("information:team_detail", kwargs={"slug": self.team.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "team_detail.html")
        self.assertEqual(response.context["team_slug"], self.team.slug)

    def test_show_standings_view(self):
        response = self.client.get(reverse("information:show_standings"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "standings.html")

    def test_show_schedule_view(self):
        response = self.client.get(reverse("information:show_schedule"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "schedule.html")

    def test_race_detail_view(self):
        response = self.client.get(reverse("information:race_detail", kwargs={"slug": self.race.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "race_detail.html")
        self.assertEqual(response.context["race_slug"], self.race.slug)

    def test_show_drivers_json_api(self):
        response = self.client.get(reverse("information:show_drivers_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) >= 1)
        self.assertTrue(any(d['full_name'] == self.driver.full_name for d in data))

    def test_show_drivers_json_detail_api(self):
        response = self.client.get(reverse("information:show_driver_json_detail", kwargs={"slug": self.driver.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual(data["full_name"], self.driver.full_name)
        self.assertEqual(data["team"], self.team.name)
        self.assertIn("number_image", data)
        self.assertIn("driver_image", data)

    def test_show_teams_json_api(self):
        response = self.client.get(reverse("information:show_teams_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) >= 1)
        self.assertTrue(any(t['name'] == self.team.name for t in data))

    def test_show_teams_json_detail_api(self):
        response = self.client.get(reverse("information:show_team_json_detail", kwargs={"slug": self.team.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual(data["full_name"], self.team.full_name)
        self.assertEqual(data["color"], "#f47500")

    def test_show_schedule_json_api(self):
        response = self.client.get(reverse("information:show_schedule_json")) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")


    def test_show_races_json_detail_api(self):
        response = self.client.get(reverse("information:show_races_json_detail", kwargs={"slug": self.race.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)

        self.assertEqual(data["name"], self.race.name)
        self.assertEqual(data["has_results"], True)
        self.assertEqual(data["result_count"], 1)

        result_data = data["results"][0]
        self.assertEqual(result_data["position"], 1)
        self.assertEqual(result_data["driver"]["full_name"], self.driver.full_name) 
        self.assertEqual(result_data["team"]["name"], self.team.name) 
        self.assertEqual(result_data["fastest_lap"], True)

    def test_show_races_json_detail_no_results_api(self):
        response = self.client.get(reverse("information:show_races_json_detail", kwargs={"slug": self.race_no_results.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)

        self.assertEqual(data["name"], self.race_no_results.name)
        self.assertEqual(data["has_results"], False)
        self.assertEqual(data["result_count"], 0)
        self.assertEqual(len(data["results"]), 0)

    def test_show_driver_standings_json_api(self):
        response = self.client.get(reverse("information:show_driver_standings_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_show_constructor_standings_json_api(self):
        response = self.client.get(reverse("information:show_constructor_standings_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

