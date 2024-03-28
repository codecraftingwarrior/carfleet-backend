from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.models import Brand


class BrandListSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'origin_country', 'created_at', 'updated_at']

    def validate_name(self, value):
        queryset = Brand.objects.filter(name=value)

        if (self.instance is None and queryset.exists()) or (
                self.instance is not None and queryset.exclude(id=self.instance.id).exists()):
            raise serializers.ValidationError('Brand with this name already exists')

        return value
