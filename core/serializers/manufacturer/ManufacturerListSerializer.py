from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.models import Manufacturer


class ManufacturerListSerializer(ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'address', 'contact', 'created_at', 'updated_at']

    def validate_name(self, value):
        queryset = Manufacturer.objects.filter(name=value)
        if (self.instance is None and queryset.exists()) or (
                self.instance is not None and queryset.exclude(id=self.instance.id).exists()):
            raise serializers.ValidationError('Manufacturer with this name already exists')

        return value
