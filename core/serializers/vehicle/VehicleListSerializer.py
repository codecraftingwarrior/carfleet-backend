from rest_framework import serializers

from core.models import Vehicle
from core.serializers.brand.BrandListSerializer import BrandListSerializer


class VehicleListSerializer(serializers.ModelSerializer):
    #brand = serializers.SerializerMethodField()
    class Meta:
        model = Vehicle
        fields = ['id', 'model', 'global_id', 'type', 'year', 'brand']

    def validate(self, data):
        queryset = Vehicle.objects.filter(model=data['model'], type=data['type'], year=data['year'])
        if (self.instance is None and queryset.exists()) or (
                self.instance is not None and queryset.exclude(id=self.instance.id).exists()):
            raise serializers.ValidationError('This vehicle has already been registered')

        return data

    def get_brand(self, obj):
        return BrandListSerializer(obj.brand).data
