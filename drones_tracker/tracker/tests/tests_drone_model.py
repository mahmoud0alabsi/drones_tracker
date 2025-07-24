from django.test import TestCase
from django.contrib.gis.geos import Point
from datetime import datetime, timedelta, timezone
from tracker.models import Drone


class DroneModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Drone.objects.create(
            serial='fsd45gfd486',
            height=19.75,
            home_distance=593.47,
            horizontal_speed=47.2,
            vertical_speed=0.3,
            location=Point(31.972234376040774, 35.832892596512636),
            last_seen=datetime.now(timezone.utc),
        )

    def test_str_method(self):
        drone = Drone.objects.get(serial='fsd45gfd486')
        self.assertEqual(drone.serial, 'fsd45gfd486')

    def test_is_online_method(self):
        drone = Drone.objects.get(serial='fsd45gfd486')
        self.assertTrue(drone.is_online)

        drone.last_seen = datetime.now(timezone.utc) - timedelta(seconds=45)
        drone.save()

        self.assertFalse(drone.is_online)

    def test_within_range_method(self):
        drone = Drone.objects.get(serial='fsd45gfd486')
        within_range = drone.within_range(
            5, (31.95663821495475, 35.84713617459755))
        self.assertTrue(within_range)

        within_range = drone.within_range(
            2, (31.95663821495475, 35.84713617459755))
        self.assertFalse(within_range)
