from django.urls import path
from .api.drone import DronesView
from .api.online_drone import OnlineDronesView
from .api.drone_within_range import DronesWithinRangeView
from .api.flight_path import DronesFlightPathView
from .api.dangerous_drone import DangerousZoneDroneView

app_name = "api"

urlpatterns = [
    path('drones/', DronesView.as_view(), name='drones'),
    path('drones/online/', OnlineDronesView.as_view(), name='online_drones'),
    path('drones/range/', DronesWithinRangeView.as_view(),
         name='drones_within_range'),
    path('drones/<str:serial>/path/',
         DronesFlightPathView.as_view(), name='drone_flight_path'),
    path('drones/dangerous/',
         DangerousZoneDroneView.as_view(), name='drone_flight_in_dangerous_zones'),
]
