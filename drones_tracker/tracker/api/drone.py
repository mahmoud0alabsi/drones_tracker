from decouple import config
from datetime import datetime, timezone, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from tracker.models import Drone
from tracker.serializers.drone import DroneSerializer, OnlineDroneSerializer

IS_ONLINE_DELTA = config('IS_ONLINE_DELTA', cast=int, default=30)


class DronesView(APIView):
    serializer_class = DroneSerializer

    @swagger_auto_schema(
        operation_summary='Get all drones (or drones contains sub-serial)',
        operation_description="Retrieve a list of drones.",
        tags=["Drones managment"],
        manual_parameters=[
            openapi.Parameter(
                'contains',
                openapi.IN_QUERY,
                description="serial (or part of serial)",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def get(self, request):
        contains = request.query_params.get('contains', '')
        if contains:
            drones = Drone.objects.filter(serial__contains=contains)
        else:
            drones = Drone.objects.all()
        serializer = DroneSerializer(drones, many=True)
        return Response(serializer.data)


class OnlineDronesView(APIView):
    serializer_class = OnlineDroneSerializer

    @swagger_auto_schema(
        operation_summary='Get online drones with their location.',
        operation_description="Retrieve one or list of drones.",
        tags=["Drones managment"],
    )
    def get(self, request):
        drones = Drone.objects.filter(
            last_seen__gte=datetime.now(
                timezone.utc) - timedelta(seconds=IS_ONLINE_DELTA)
        )
        serializer = OnlineDroneSerializer(drones, many=True)
        return Response(serializer.data)


class DronesWithinRangeView(APIView):
    serializer_class = DroneSerializer

    @swagger_auto_schema(
        operation_summary='Get all drones within a specific range',
        operation_description="Retrieve a list of drones.",
        tags=["Drones managment"],
        manual_parameters=[
            openapi.Parameter(
                'range',
                openapi.IN_QUERY,
                required=True,
                description="range",
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                'latitude',
                openapi.IN_QUERY,
                required=True,
                description="latitude",
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                'longitude',
                openapi.IN_QUERY,
                required=True,
                description="longitude",
                type=openapi.TYPE_NUMBER,
            ),
        ],
    )
    def get(self, request):
        range = float(request.query_params.get('range', ''))
        latitude = float(request.query_params.get('latitude', ''))
        longitude = float(request.query_params.get('longitude', ''))
        if not range or not latitude or not longitude:
            return Response('You must set all required params.', status=400)

        drones = Drone.objects.all()
        drones_within_range = []
        for drone in drones:
            if drone.within_range(range, (latitude, longitude)):
                drones_within_range.append(drone)

        serializer = DroneSerializer(drones_within_range, many=True)
        return Response(serializer.data)
