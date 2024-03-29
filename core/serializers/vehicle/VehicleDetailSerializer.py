from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from core.models import Vehicle
from core.serializers.brand.BrandListSerializer import BrandListSerializer
from core.serializers.manufacturer.ManufacturerListSerializer import ManufacturerListSerializer


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
