from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from core.models import VehicleUnit
from core.serializers.vehicle_serializers import VehicleListSerializer


class VehicleUnitCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleUnit
        fields = ['plate_number', 'mileage', 'color', 'price', 'vehicle']

    def validate_plate_number(self, value):
        queryset = VehicleUnit.objects.filter(plate_number=value)

        if (self.instance is None and queryset.exists()) or (
                self.instance is not None and queryset.exclude(pk=self.instance.pk).exists()):
            raise serializers.ValidationError('Vehicle unit with this plate_number already exists')

        return value


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


class VehicleUnitListSerializer(serializers.ModelSerializer):
    mileage = serializers.SerializerMethodField()

    class Meta:
        model = VehicleUnit
        fields = ['id', 'global_id', 'plate_number', 'status', 'mileage', 'color', 'price', 'created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_mileage(self, instance):
        return round(instance.mileage, 2)
