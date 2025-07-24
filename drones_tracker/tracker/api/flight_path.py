from decouple import config
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ValidationError
from tracker.repositories.drone_log_repository import DroneLogRepository
from tracker.strategies.geo_json_path_strategies import GeoJSONStrategyFactory, GeoJSONPathContext

DRONE_FLIGHT_MAX_TIME = config('DRONE_FLIGHT_MAX_TIME', cast=int, default=5)
DRONE_PACKETS_TIMESTAMP_DELTA = config(
    'DRONE_PACKETS_TIMESTAMP_DELTA', cast=int, default=30)


class DronesFlightPathView(APIView):
    drone_log_repo = DroneLogRepository()

    @swagger_auto_schema(
        operation_summary='Get drone\'s flight path as GeoJSON format.',
        operation_description="Retrieve a drone flight path.",
        tags=["Drones managment"],
        manual_parameters=[
            openapi.Parameter(
                'path-type',
                openapi.IN_QUERY,
                description="path-type",
                type=openapi.TYPE_STRING,
                default='points',
                enum=['points', 'lines']
            ),
        ],
    )
    def get(self, request, serial):
        try:
            path_type = request.query_params.get('path-type', 'points')
            if not serial or serial is None:
                raise ValidationError('You have to specify a drone serial')

            drone_logs = self.drone_log_repo.get_latest_flight_logs(
                serial=serial, max_time=DRONE_FLIGHT_MAX_TIME)

            latest_flight_logs = self._process_flight_logs(drone_logs)

            path_generator = GeoJSONPathContext(path_strategy=None)
            strategy = GeoJSONStrategyFactory.create_strategy(path_type)
            path_generator.set_path_strategy(strategy)
            geo_json = path_generator.get_path(logs=latest_flight_logs)
            return Response(geo_json)
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

    def _process_flight_logs(self, drone_logs):
        try:
            base_log_idx = 0
            first_log_idx = 0
            for idx in range(1, len(drone_logs) - 1):
                delta = drone_logs[base_log_idx].timestamp - \
                    drone_logs[idx].timestamp
                if delta.seconds > DRONE_PACKETS_TIMESTAMP_DELTA:
                    first_log_idx = idx - 1
                    break
                else:
                    base_log_idx = idx

            return drone_logs[:first_log_idx+1][::-1]
        except Exception as e:
            raise e
