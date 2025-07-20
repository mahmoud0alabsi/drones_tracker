import uuid
from django.contrib.gis.db import models


class Drone(models.Model):
    serial = models.CharField(
        primary_key=True, unique=True, db_index=True, default=uuid.uuid4, editable=False, blank=False)
    height = models.FloatField(null=False, blank=False)
    home_distance = models.FloatField(null=False, blank=False)
    horizontal_speed = models.FloatField(null=False, blank=False)
    vertical_speed = models.FloatField(null=False, blank=False)
    latitude = models.PointField()
    longitude = models.PointField()
    is_online = models.BooleanField(default=False, null=False, blank=False)
    last_seen = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return self.serial

    class Meta:
        app_label = 'tracker'
        ordering = ['-last_seen']


class DroneLog(models.Model):
    drone = models.ForeignKey(Drone, editable=False,
                              blank=False, on_delete=models.CASCADE)
    payload = models.JSONField(editable=False)
    timestamp = models.DateTimeField(editable=False, null=False, blank=False)

    def __str__(self):
        return self.serial

    class Meta:
        app_label = 'tracker'
        ordering = ['-timestamp']
