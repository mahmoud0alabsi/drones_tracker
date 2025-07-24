from datetime import datetime, timezone, timedelta
from rest_framework.test import APITestCase
from django.contrib.gis.geos import Point
from django.urls import reverse
from tracker.models import Drone
from tracker.mqtt.mqtt_call_backs import store_drone


class DronesFlightPathViewTest(APITestCase):
    drone_serial = '45fdsf987dsf'

    @classmethod
    def setUpTestData(self):
        for idx in range(10):
            time_delta = timedelta(seconds=idx+5)
            store_drone(
                topic=f'thing/product/{self.drone_serial}/osd',
                payload={
                    "serial": self.drone_serial,
                    "height": 7*idx,
                    "home_distance": 478 + (idx*2),
                    "horizontal_speed": 10.9,
                    "vertical_speed": 2.4,
                    "latitude": 31.972234376040774 + (idx/1000),
                    "longitude": 35.832892596512636 + (idx/1000),
                },
                last_seen=datetime.now(timezone.utc) - timedelta(minutes=5) +
                time_delta
            )

    def setUp(self):
        self.url = reverse("api:drone_flight_path", args=(self.drone_serial,))

    def test_view_url_exists(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.url + '?path-type=lines')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.url + '?path-type=point')
        self.assertEqual(response.status_code, 400)

        response = self.client.get(self.url + '?path-type=points')
        self.assertEqual(response.status_code, 200)
