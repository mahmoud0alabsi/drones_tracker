import string
import random
from datetime import datetime, timezone, timedelta
from rest_framework.test import APITestCase
from django.contrib.gis.geos import Point
from django.urls import reverse
from tracker.models import Drone


class DronesViewTest(APITestCase):
    @classmethod
    def setUpTestData(self):
        for idx in range(10):
            Drone.objects.create(
                serial=''.join(random.choices(
                    string.ascii_uppercase + string.digits, k=10)),
                height=7*idx,
                home_distance=478 + (idx*2),
                horizontal_speed=47.2,
                vertical_speed=0.3,
                location=Point(31.972234376040774 + (idx/1000),
                               35.832892596512636 + (idx/1000)),
                last_seen=datetime.now(timezone.utc) - timedelta(minutes=idx),
            )

    def setUp(self):
        self.url = reverse("api:drones")

    def test_view_url_exists(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
