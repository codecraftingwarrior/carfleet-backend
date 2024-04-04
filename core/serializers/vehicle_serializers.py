from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from core.models import Vehicle
from core.serializers.brand_serializers import BrandListSerializer
from core.serializers.manufacturer_serializers import ManufacturerListSerializer


class VehicleCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'model', 'type', 'year', 'brand', 'description', 'manufacturer']

    def validate(self, attrs):
        queryset = Vehicle.objects.filter(model=attrs['model'], type=attrs['type'], year=attrs['year'])
        if (self.instance is None and queryset.exists()) or (
                self.instance is not None and queryset.exclude(id=self.instance.id).exists()):
            raise serializers.ValidationError("This vehicle already exists")

        return attrs


class VehicleDetailSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField()
    manufacturer = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = ['id', 'model', 'global_id', 'type', 'year', 'brand', 'manufacturer']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_brand(self, instance):
        return BrandListSerializer(instance.brand).data

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_manufacturer(self, instance):
        return ManufacturerListSerializer(instance.manufacturer).data


class VehicleListSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = ['id', 'model', 'global_id', 'type', 'year', 'brand']

    def validate(self, data):
        queryset = Vehicle.objects.filter(model=data['model'], type=data['type'], year=data['year'])
        if (self.instance is None and queryset.exists()) or (
                self.instance is not None and queryset.exclude(id=self.instance.id).exists()):
            raise serializers.ValidationError('This vehicle has already been registered')

        return data

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_brand(self, obj):
        return BrandListSerializer(obj.brand).data
