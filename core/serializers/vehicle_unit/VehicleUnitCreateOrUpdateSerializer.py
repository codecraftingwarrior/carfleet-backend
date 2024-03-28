from rest_framework import serializers

from core.models import VehicleUnit


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

