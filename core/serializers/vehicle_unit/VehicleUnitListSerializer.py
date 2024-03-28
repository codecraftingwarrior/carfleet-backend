from rest_framework import serializers

from core.models import VehicleUnit


class VehicleUnitListSerializer(serializers.ModelSerializer):
    mileage = serializers.SerializerMethodField()

    class Meta:
        model = VehicleUnit
        fields = ['id', 'global_id', 'plate_number', 'status', 'mileage', 'color', 'price', 'created_at', 'updated_at']


    def get_mileage(self, instance):
        return round(instance.mileage, 2)


