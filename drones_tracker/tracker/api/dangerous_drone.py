from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ValidationError
from tracker.serializers.drone import DroneSerializer
from tracker.repositories.drone_repository import DroneRepository
from tracker.api.online_drone import OnlineDronesView


class DangerousZoneDroneView(APIView):
    drone_repo = DroneRepository()
    serializer = DroneSerializer

    @swagger_auto_schema(
        operation_summary='Get drones flight in dangerous zones.',
        operation_description="Retrieve a list of drones.",
        tags=["Drones managment"],
        manual_parameters=[
            openapi.Parameter(
                'height',
                openapi.IN_QUERY,
                description="height (meters)",
                type=openapi.TYPE_NUMBER,
                default=500
            ),
            openapi.Parameter(
                'horizontal-speed',
                openapi.IN_QUERY,
                description="horizontal speed (m/s)",
                type=openapi.TYPE_NUMBER,
                default=10
            ),
        ],
    )
    def get(self, request):
        try:
            height = float(request.query_params.get('height', ''))
            horizontal_speed = float(
                request.query_params.get('horizontal-speed', ''))

            if height is None or not (type(height) in [float, int]):
                raise ValidationError('height is incorrect')
            if horizontal_speed is None or not (type(horizontal_speed) in [float, int]):
                raise ValidationError('height is incorrect')

            online_filter = OnlineDronesView.get_online_drones_filter(
                self=None)
            height_Q = Q(height__gte=height)
            horizontal_speed_Q = Q(horizontal_speed__gte=horizontal_speed)
            combined_condition = online_filter & (
                height_Q | horizontal_speed_Q)
            dangerous_drones = self.drone_repo.get_filtered(
                condition=combined_condition)

            drones_with_reasons = self.serializer(
                dangerous_drones, many=True)
            drones_with_reasons = self._set_dangerous_reason(
                drones_with_reasons.data, height, horizontal_speed)

            return Response(drones_with_reasons)
        except APIException as e:
            return Response(
                e.get_full_details(),
                status=e.status_code,
                exception=True
            )
        except Exception as e:
            return Response(
                {'message': str(e)},
                status=500,
                exception=True
            )

    def _set_dangerous_reason(self, drones, height, horizontal_speed):
        for drone in drones:
            if drone['height'] >= height:
                reason = f'Drone flight with height grater than or equal {height}.'
            else:
                reason = f'Drone flight with horizontal speed grater than or equal {horizontal_speed}.'
            drone['reason'] = reason

        return drones
