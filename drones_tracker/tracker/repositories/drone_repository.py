from django.db.models import Q
from tracker.models import Drone
from .base import BaseRepository


class DroneRepository(BaseRepository):
    def __init__(self):
        super().__init__(Drone)

    def get_filtered(self, condition=None, **kwargs):
        return self.model.objects.filter(condition)

    def get_Q_filter(self, **kwargs):
        return Q(
            **kwargs
        )
