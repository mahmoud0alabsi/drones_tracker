from datetime import datetime, timedelta, timezone
from decouple import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from tracker.models import DroneLog

DRONE_FLIGHT_MAX_TIME = config('DRONE_FLIGHT_MAX_TIME', cast=int, default=5)
DRONE_PACKETS_TIMESTAMP_DELTA = config(
    'DRONE_PACKETS_TIMESTAMP_DELTA', cast=int, default=30)


class DronesFlightPathView(APIView):
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
            path_type = request.query_params.get('path-type', '')
            if not serial or serial is None:
                return Response('You have to specify a drone serial.', status=400)

            drone_logs = DroneLog.objects.filter(
                drone=serial,
            ).order_by('-timestamp').filter(
                timestamp__gte=datetime.now(
                    timezone.utc) - timedelta(hours=DRONE_FLIGHT_MAX_TIME)
            )

            flight_logs = get_last_flight_logs(drone_logs)

            if path_type == 'lines':
                geo_json = get_geo_json_path_as_lines(flight_logs)
            else:
                geo_json = get_geo_json_path_as_points(flight_logs)
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


def get_last_flight_logs(drone_logs):
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


def get_geo_json_path_as_points(logs):
    try:
        features = []
        for log in logs:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [log.payload['longitude'], log.payload['latitude']]
                },
                "properties": {
                    "height": log.payload['height'],
                    "horizontal_speed": log.payload['horizontal_speed'],
                    "timestamp": log.timestamp
                }
            })

        return {
            "type": "FeatureCollection",
            "features": features
        }
    except Exception as e:
        raise e


def get_geo_json_path_as_lines(logs):
    try:
        raise Exception('Errror error error')
        coordinates = []
        for log in logs:
            coordinates.append(
                [log.payload['longitude'], log.payload['latitude']])

        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "coordinates": coordinates,
                        "type": "LineString"
                    }
                }
            ]
        }
    except Exception as e:
        raise e
