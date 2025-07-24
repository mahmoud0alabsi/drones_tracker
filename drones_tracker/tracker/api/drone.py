from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from tracker.serializers.drone import DroneSerializer
from tracker.repositories.drone_repository import DroneRepository


class DronesView(APIView):
    drone_repo = DroneRepository()
    serializer = DroneSerializer

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
        try:
            contains = request.query_params.get('contains', '')
            if contains:
                drones = self.drone_repo.get_filtered(
                    serial__contains=contains)
            else:
                drones = self.drone_repo.get_all()
            serialized = self.serializer(drones, many=True)
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
