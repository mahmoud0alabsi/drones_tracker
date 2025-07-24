from decouple import config
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ValidationError
from tracker.serializers.drone import DroneSerializer
from tracker.repositories.drone_repository import DroneRepository


class DronesWithinRangeView(APIView):
    drone_repo = DroneRepository()
    serializer = DroneSerializer

    @swagger_auto_schema(
        operation_summary='Get all drones within a specific range',
        operation_description="Retrieve a list of drones.",
        tags=["Drones managment"],
        manual_parameters=[
            openapi.Parameter(
                'range',
                openapi.IN_QUERY,
                required=True,
                description="range (in km)",
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
        try:
            range = float(request.query_params.get('range', 5))
            latitude = float(request.query_params.get('latitude', 0.0))
            longitude = float(request.query_params.get('longitude', 0.0))
            if not range or not latitude or not longitude:
                raise ValidationError(
                    'You must set all required params.', status=400)
            if type(range) not in (float, int):
                raise ValidationError(
                    'The range parameter type must be float or int.', status=400)
            if type(latitude) is not float:
                raise ValidationError(
                    'The latitude parameter type must be float.', status=400)
            if type(longitude) is not float:
                raise ValidationError(
                    'The longitude parameter type must be float.', status=400)

            drones = self.drone_repo.get_all()
            drones_within_range = []
            for drone in drones:
                if drone.within_range(range, (latitude, longitude)):
                    drones_within_range.append(drone)

            serialized = self.serializer(drones_within_range, many=True)
            return Response(serialized.data)
        except APIException as e:
            return Response(
                e.get_full_details(),
                status=e.status_code,
                exception=True
            )
        except Exception as e:
            return Response(
                {'message': str(e), },
                status=500,
                exception=True
            )
