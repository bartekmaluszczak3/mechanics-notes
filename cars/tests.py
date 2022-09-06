from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'mechanics_notes.settings'


# Create your tests here.
class CarApiTest(APITestCase):

    def authenticate(self, email, password):
        self.client.post(reverse("register"), {"email": email, "password": password})
        login_response = self.client.post(reverse("login"), {"email": email, "password": password})
        token = login_response.json()['tokens']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_create_car(self):
        self.authenticate("test_email", "asdasdsdasda")
        data = {
            "brand": "BMW",
            "model": "e60",
            "year": 1000
        }
        response = self.client.post("/api/car/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()['brand'])
        self.assertTrue(response.json()['model'])
        self.assertTrue(response.json()['year'])
        self.assertEqual([], response.json()['notes'])

    def test_user_has_access_to_his_car(self):
        self.authenticate("test_email", "asdasdsdasda")
        data = {
            "brand": "BMW",
            "model": "e60",
            "year": 1000
        }
        response = self.client.post("/api/car/", data, format='json')
        self.assertTrue(response.json()['id'])
        car_id = response.json()['id']
        response = self.client.get(f"/api/car/{car_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_should_not_has_access_to_others_car(self):
        self.authenticate("test_email", "asdasdsdasda")
        data = {
            "brand": "BMW",
            "model": "e60",
            "year": 1000
        }
        response = self.client.post("/api/car/", data, format='json')
        self.assertTrue(response.json()['id'])
        car_id = response.json()['id']

        self.authenticate("testowy_email", "asdasdsdasda")
        response = self.client.get(f"/api/car/{car_id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

