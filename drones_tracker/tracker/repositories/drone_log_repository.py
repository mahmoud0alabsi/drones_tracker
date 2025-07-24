from decouple import config
from datetime import datetime, timedelta, timezone
from django.forms import ValidationError
from tracker.models import DroneLog
from .base import BaseRepository

DRONE_FLIGHT_MAX_TIME = config('DRONE_FLIGHT_MAX_TIME', cast=int, default=5)


class DroneLogRepository(BaseRepository):
    def __init__(self):
        super().__init__(DroneLog)

    def get_filtered(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def get_latest_flight_logs(self, serial=None, max_time=None, **kwargs):
        if serial is None:
            raise ValidationError(
                "You have to pass drone serial to fetch latest flight logs.")
        if max_time is None:
            max_time = DRONE_FLIGHT_MAX_TIME

        last_log = self.model.objects.filter(
            drone=serial,
        ).order_by('-timestamp').first()

        return self.model.objects.filter(
            drone=serial,
        ).order_by('-timestamp').filter(
            timestamp__gte=last_log.timestamp - timedelta(hours=max_time)
        )
