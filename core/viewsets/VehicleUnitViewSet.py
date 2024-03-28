from rest_framework import viewsets, status
from rest_framework.response import Response

from core.models import VehicleUnit
from core.serializers.vehicle_unit.VehicleUnitCreateOrUpdateSerializer import VehicleUnitCreateOrUpdateSerializer
from core.serializers.vehicle_unit.VehicleUnitDetailSerializer import VehicleUnitDetailSerializer
from core.serializers.vehicle_unit.VehicleUnitListSerializer import VehicleUnitListSerializer


class VehicleUnitViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleUnitListSerializer

    def get_queryset(self):
        return VehicleUnit.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return VehicleUnitCreateOrUpdateSerializer
        elif self.action == 'retrieve':
            return VehicleUnitDetailSerializer
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        vehicle = self.get_object()
        update_serializer = VehicleUnitCreateOrUpdateSerializer(vehicle, data=request.data)

        if update_serializer.is_valid():
            self.perform_update(update_serializer)

            detail_serializer = VehicleUnitDetailSerializer(vehicle)
            return Response(detail_serializer.data)

        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
