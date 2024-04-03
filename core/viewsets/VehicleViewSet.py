import json
from uuid import UUID

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.forms.models import model_to_dict

from core.consumers import VEHICLE_SUBSCRIBER_GROUP_NAME, WEBSOCKET_INSERTION_ACTION, WEBSOCKET_UPDATE_ACTION
from core.helpers import UUIDEncoder
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
            serializer = VehicleDetailSerializer(Vehicle.objects.get(id=response.data['id']))

            payload = {
                'type': 'vehicle_added',
                'perimeter': 'vehicle',
                'action': WEBSOCKET_INSERTION_ACTION,
                'meta': serializer.data
            }

            async_to_sync(channel_layer.group_send)(
                VEHICLE_SUBSCRIBER_GROUP_NAME,
                payload
            )

        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, args, kwargs)
        instance = self.get_object()

        if response.status_code == status.HTTP_200_OK:
            channel_layer = get_channel_layer()

            payload = {
                'type': 'vehicle_updated',
                'meta': {
                    'updated_by': request.user.username,
                    'perimeter': 'vehicle',
                    'action': WEBSOCKET_UPDATE_ACTION
                }
            }

            async_to_sync(channel_layer.group_send)(
                VEHICLE_SUBSCRIBER_GROUP_NAME + '_target_' + str(instance.id),
                payload
            )

        return Response(VehicleDetailSerializer(instance).data)


