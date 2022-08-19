import os
import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

os.environ['DJANGO_SETTINGS_MODULE'] = 'mechanics_notes.settings'


class NoteApiTest(APITestCase):

    def authenticate(self, email, password):
        self.client.post(reverse("register"), {"email": email, "password": password})
        login_response = self.client.post(reverse("login"), {"email": email, "password": password})
        token = login_response.json()['tokens']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def create_car(self):
        data = {
            "brand": "BMW",
            "model": "e60",
            "year": 1000
        }
        response = self.client.post("/api/car/", data, format='json')
        car = response.json()
        self.assertTrue(car['id'])
        return car['id']

    def test_create_note(self):
        self.authenticate("test_email", "asdasdsdasda")
        car_id = self.create_car()
        data = {
            "description": "sda",
            "date": "2022-08-19",
            "mileage": 231231231,
            "repair": "dasdasdas",
            "next_repair": "231312312",
        }
        response = self.client.post(f"/api/note/{car_id}", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note = response.json()
        self.assertTrue(note['id'])
        self.assertEqual(data['description'], note['description'])
        self.assertEqual(data['date'], note['date'])
        self.assertEqual(data['mileage'], note['mileage'])
        self.assertEqual(data['repair'], note['repair'])
        self.assertEqual(data['next_repair'], note['next_repair'])

    def test_if_date_is_null_today_date_should_be_inserted(self):
        self.authenticate("test_email", "asdasdsdasda")
        car_id = self.create_car()
        data = {
            "description": "sda",
            "mileage": 231231231,
            "repair": "dasdasdas",
            "next_repair": "231312312",
        }
        today_date = str(datetime.date.today())
        response = self.client.post(f"/api/note/{car_id}", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note = response.json()
        self.assertTrue(note['id'])
        self.assertEqual(today_date, note['date'])

    def test_user_should_get_notes_from_his_cars(self):
        self.authenticate("test_email", "asdasdsdasda")
        car_id = self.create_car()
        data = {
            "description": "sda",
            "mileage": 231231231,
            "repair": "dasdasdas",
            "next_repair": "231312312",
        }
        for x in range(2):
            response = self.client.post(f"/api/note/{car_id}", data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"/api/note/{car_id}", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notes = response.json()['notes']
        self.assertEqual(2, len(notes))
        self.assertNotEqual(notes[0]['id'], notes[1]['id'])
        self.assertEqual(notes[0]['car_id'], car_id)

    def test_user_should_not_has_access_to_notes_from_other_car(self):
        self.authenticate("test_email", "asdasdsdasda")
        data = {
            "description": "sda",
            "mileage": 231231231,
            "repair": "dasdasdas",
            "next_repair": "231312312",
        }
        car_id = self.create_car()
        for x in range(2):
            response = self.client.post(f"/api/note/{car_id}", data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.authenticate("testowy_email", "asdasdsdasda")
        response = self.client.get(f"/api/note/{car_id}", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
