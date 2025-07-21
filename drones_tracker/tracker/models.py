import uuid
from decouple import config
from datetime import datetime, timezone, timedelta
from django.contrib.gis.db import models
from haversine import haversine

IS_ONLINE_DELTA = config('IS_ONLINE_DELTA', cast=int, default=30)


class Drone(models.Model):
    serial = models.CharField(
        primary_key=True, unique=True, db_index=True, default=uuid.uuid4, editable=False, blank=False)
    height = models.FloatField(null=False, blank=False)
    home_distance = models.FloatField(null=False, blank=False)
    horizontal_speed = models.FloatField(null=False, blank=False)
    vertical_speed = models.FloatField(null=False, blank=False)
    location = models.PointField()
    last_seen = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return self.serial

    @property
    def is_online(self):
        # the drone is online only when last seen within 30 seconds
        return self.last_seen >= (datetime.now(timezone.utc) - timedelta(seconds=IS_ONLINE_DELTA))

    def calculate_distance(self, point):
        return haversine(point, self.location)

    def within_range(self, range, point):
        return self.calculate_distance(point) <= range

    class Meta:
        app_label = 'tracker'
        ordering = ['-last_seen']


class DroneLog(models.Model):
    drone = models.ForeignKey(Drone, editable=False,
                              blank=False, on_delete=models.CASCADE)
    payload = models.JSONField()
    timestamp = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return self.drone.serial

    class Meta:
        app_label = 'tracker'
        ordering = ['-timestamp']
