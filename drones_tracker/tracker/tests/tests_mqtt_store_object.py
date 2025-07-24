from django.test import TestCase
from tracker.models import Drone, DroneLog
from tracker.mqtt.mqtt_call_backs import store_drone


class MQTTMethodsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        store_drone(
            topic='thing/product/123456abc/osd',
            payload={
                "serial": "123456abc",
                "height": 12.36,
                "home_distance": 65.4,
                "horizontal_speed": 10.9,
                "vertical_speed": 2.4,
                "latitude": 31.48714189,
                "longitude": 35.48714189,
            }
        )

    def test_is_drone_created(self):
        drone = Drone.objects.get(serial='123456abc')
        self.assertEqual(drone.serial, '123456abc')

    def test_drone_log_created(self):
        drone = Drone.objects.get(serial='123456abc')
        log = DroneLog.objects.get(drone=drone)
        self.assertTrue(drone.serial == log.drone.serial)
