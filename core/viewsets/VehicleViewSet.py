import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core import serializers


from core.consumers import VEHICLE_SUBSCRIBER_GROUP_NAME
from core.models import Vehicle
from core.permissions.IsAdmin import IsAdmin
from core.serializers.vehicle.VehicleCreateOrUpdateSerializer import VehicleCreateOrUpdateSerializer
from core.serializers.vehicle.VehicleDetailSerializer import VehicleDetailSerializer
from core.serializers.vehicle.VehicleListSerializer import VehicleListSerializer


@extend_schema(
    tags=['Vehicles']
)
class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleListSerializer
    permission_classes = [IsAdmin, IsAuthenticated]

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

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:

            channel_layer = get_channel_layer()

            payload = {
                'perimeter': 'vehicle',
                'action': 'insertion'
            }

            async_to_sync(channel_layer.group_send)(
                VEHICLE_SUBSCRIBER_GROUP_NAME,
                payload
            )

        return response
