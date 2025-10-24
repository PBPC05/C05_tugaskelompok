from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.history.models import Driver, Winner
import json

# Create your tests here.
# TEST MODEL NYA
class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create(
            driver_name="Lewis Hamilton",
            nationality="British",
            car="Mercedes",
            points=347.0,
            podiums=10,
            year=2023,
            driver_code="HAM",
        )

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "Lewis Hamilton")

    def test_driver_fields(self):
        self.assertEqual(self.driver.car, "Mercedes")
        self.assertEqual(self.driver.year, 2023)
        self.assertEqual(self.driver.points, 347.0)


class WinnerModelTest(TestCase):
    def setUp(self):
        self.winner = Winner.objects.create(
            grand_prix="Monaco GP",
            date="2023-05-28",
            winner="Max Verstappen",
            car="Red Bull",
            laps=78,
            time="1:48:51.980",
            name_code="VER",
        )

    def test_winner_str(self):
        self.assertEqual(str(self.winner), "Max Verstappen - Monaco GP")

    def test_winner_fields(self):
        self.assertEqual(self.winner.car, "Red Bull")
        self.assertEqual(self.winner.laps, 78)
        self.assertEqual(self.winner.time, "1:48:51.980")


# TESTS DRIVER VIEW NYA
class DriverViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver = Driver.objects.create(
            driver_name="Charles Leclerc",
            nationality="Monégasque",
            car="Ferrari",
            points=280.5,
            podiums=8,
            year=2023,
            driver_code="LEC",
        )

    def test_driver_user_page_renders(self):
        response = self.client.get(reverse("history:driver_user_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "driver_page_user_carousel.html")

    def test_add_driver(self):
        response = self.client.post(
            reverse("history:add_driver"),
            data=json.dumps({
                "driver_name": "Lando Norris",
                "nationality": "British",
                "car": "McLaren",
                "points": 200,
                "podiums": 5,
                "year": 2023,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Driver.objects.filter(driver_name="Lando Norris").exists())

    def test_edit_driver(self):
        response = self.client.post(
            reverse("history:edit_driver", args=[self.driver.id]),
            data=json.dumps({
                "driver_name": "Charles Leclerc Jr",
                "nationality": "Monégasque",
                "car": "Ferrari",
                "points": 285,
                "podiums": 9,
                "year": 2024,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.driver_name, "Charles Leclerc Jr")

    def test_delete_driver(self):
        response = self.client.delete(reverse("history:delete_driver", args=[self.driver.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Driver.objects.filter(id=self.driver.id).exists())


# TESTS WINNER VIEW NYA
class WinnerViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.winner = Winner.objects.create(
            grand_prix="Silverstone GP",
            date="2023-07-09",
            winner="Lewis Hamilton",
            car="Mercedes",
            laps=52,
            time="1:27:44.710",
            name_code="HAM",
        )

    def test_winner_user_page_renders(self):
        response = self.client.get(reverse("history:winner_user_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "winner_page_user_carousel.html")

    def test_add_winner(self):
        response = self.client.post(
            reverse("history:add_winner"),
            data=json.dumps({
                "grand_prix": "Belgium GP",
                "date": "2023-08-01",
                "winner": "Max Verstappen",
                "car": "Red Bull",
                "laps": 44,
                "time": "1:29:45.222",
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Winner.objects.filter(grand_prix="Belgium GP").exists())

    def test_edit_winner(self):
        response = self.client.post(
            reverse("history:edit_winner", args=[self.winner.id]),
            data=json.dumps({
                "grand_prix": "Silverstone GP",
                "date": "2023-07-09",
                "winner": "Lewis Hamilton Jr",
                "car": "Mercedes",
                "laps": 53,
                "time": "1:28:00.000",
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.winner.refresh_from_db()
        self.assertEqual(self.winner.winner, "Lewis Hamilton Jr")

    def test_delete_winner(self):
        response = self.client.delete(reverse("history:delete_winner", args=[self.winner.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Winner.objects.filter(id=self.winner.id).exists())


# TESTS ADMIN ACCESS NYA
class AdminAccessTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass", email="admin@test.com"
        )

    def test_driver_admin_page_accessible_if_logged_in(self):
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(reverse("history:driver_admin_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "driver_page_admin.html")

    def test_winner_admin_page_accessible_if_logged_in(self):
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(reverse("history:winner_admin_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "winner_page_admin.html")


# TESTS EMPTY PAGE NYA
class EmptyPageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_driver_user_page_empty_context(self):
        response = self.client.get(reverse("history:driver_user_page"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["drivers"]), 0)

    def test_winner_user_page_empty_context(self):
        response = self.client.get(reverse("history:winner_user_page"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["winners"]), 0)
