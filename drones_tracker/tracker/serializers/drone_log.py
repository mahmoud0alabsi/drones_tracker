from rest_framework import serializers
from tracker.models import DroneLog


class DroneLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DroneLog
        fields = '__all__'
        read_only_fields = [f.name for f in DroneLog._meta.get_fields()]

    def create(self, validated_data):
        raise Exception('You can\'t create a DroneLog object.')

    def update(self, instance, validated_data):
        raise Exception('You can\'t update a DroneLog object.')
