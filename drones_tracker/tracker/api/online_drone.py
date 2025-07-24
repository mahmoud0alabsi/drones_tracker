from decouple import config
from datetime import datetime, timezone, timedelta
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from tracker.serializers.drone import OnlineDroneSerializer
from tracker.repositories.drone_repository import DroneRepository

IS_ONLINE_DELTA = config('IS_ONLINE_DELTA', cast=int, default=30)


class OnlineDronesView(APIView):
    drone_repo = DroneRepository()
    serializer = OnlineDroneSerializer

    @swagger_auto_schema(
        operation_summary='Get online drones with their location.',
        operation_description="Retrieve one or list of drones.",
        tags=["Drones managment"],
    )
    def get(self, request):
        try:
            online_filter = self.get_online_drones_filter(self=self)
            online_drones = self.drone_repo.get_filtered(online_filter)
            serialized = self.serializer(online_drones, many=True)
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

    @staticmethod
    def get_online_drones_filter(self=None):
        repo = None
        if self is None:
            repo = DroneRepository()
        else:
            repo = self.drone_repo
        return repo.get_Q_filter(
            last_seen__gte=datetime.now(
                timezone.utc) - timedelta(seconds=IS_ONLINE_DELTA)
        )
