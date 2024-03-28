from rest_framework import viewsets, status
from rest_framework.response import Response

from core.models import Vehicle
from core.serializers.vehicle.VehicleCreateOrUpdateSerializer import VehicleCreateOrUpdateSerializer
from core.serializers.vehicle.VehicleDetailSerializer import VehicleDetailSerializer
from core.serializers.vehicle.VehicleListSerializer import VehicleListSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleListSerializer

    def get_queryset(self):
        return Vehicle.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return VehicleCreateOrUpdateSerializer
        elif self.action == 'retrieve':
            return VehicleDetailSerializer
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        vehicle = self.get_object()
        update_serializer = VehicleCreateOrUpdateSerializer(vehicle, data=request.data)

        if update_serializer.is_valid():
            self.perform_update(update_serializer)

            detail_serializer = VehicleDetailSerializer(vehicle)
            return Response(detail_serializer.data)

        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
