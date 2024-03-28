from rest_framework import serializers

from core.models import Vehicle


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
