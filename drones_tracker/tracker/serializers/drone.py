from tracker.models import Drone
from rest_framework.serializers import ReadOnlyField
from rest_framework_gis.serializers import GeoModelSerializer, GeometryField


class DroneSerializer(GeoModelSerializer):
    location = GeometryField()
    is_online = ReadOnlyField()

    class Meta:
        model = Drone
        fields = '__all__'
        read_only_fields = [f.name for f in Drone._meta.get_fields()]
        geo_field = 'location'

    def create(self, validated_data):
        raise Exception('You can\'t create a Drone object.')

    def update(self, instance, validated_data):
        raise Exception('You can\'t update a Drone object.')


class OnlineDroneSerializer(GeoModelSerializer):
    location = GeometryField()

    class Meta:
        model = Drone
        fields = ['serial', 'location']
        read_only_fields = [f.name for f in Drone._meta.get_fields()]
        geo_field = 'location'
