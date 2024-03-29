from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from core.models import VehicleUnit
from core.serializers.vehicle.VehicleListSerializer import VehicleListSerializer


class VehicleUnitDetailSerializer(serializers.ModelSerializer):
    vehicle = serializers.SerializerMethodField()
    mileage = serializers.SerializerMethodField()

    class Meta:
        model = VehicleUnit
        fields = ['id', 'global_id', 'plate_number', 'status', 'mileage', 'color', 'price', 'created_at', 'updated_at',
                  'vehicle']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_vehicle(self, instance):
        return VehicleListSerializer(instance.vehicle).data

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_mileage(self, instance):
        return round(instance.mileage, 2)
