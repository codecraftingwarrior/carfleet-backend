from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core import services
from core.consumers import VEHICLE_SUBSCRIBER_GROUP_NAME
from core.models import Vehicle
from core.permissions.IsAdmin import IsAdmin
from core.serializers import VehicleListSerializer, VehicleCreateOrUpdateSerializer, VehicleDetailSerializer


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
            payload = services.VehicleService.get_add_websocket_payload(vehicle_id=response.data['id'])

            services.WebsocketManager.send_to_channel(
                VEHICLE_SUBSCRIBER_GROUP_NAME,
                event_type='vehicle_added',
                payload=payload
            )

        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, args, kwargs)
        instance = self.get_object()

        if response.status_code == status.HTTP_200_OK:
            payload = services.VehicleService.get_update_websocket_payload(user_username=request.user.username,
                                                                           instance=instance)
            services.WebsocketManager.send_to_channel(
                VEHICLE_SUBSCRIBER_GROUP_NAME + '_target_' + str(instance.id),
                payload=payload,
                event_type='vehicle_updated'
            )

        return Response(VehicleDetailSerializer(instance).data)
