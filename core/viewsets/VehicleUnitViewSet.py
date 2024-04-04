from django.contrib.auth import get_user_model
from django.db import transaction
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from core import repositories, services
from core.models import VehicleUnit
from core.models.VehicleUnit import VehicleUnitStatuses
from core.permissions import IsAdminOrReadOnly
from core.serializers import SaleCreateOrUpdateSerializer
from core.serializers.rental_contract_serializers import RentalContractCreateOrUpdateSerializer
from core.serializers.vehicle_unit_serializers import VehicleUnitListSerializer, VehicleUnitCreateOrUpdateSerializer, \
    VehicleUnitDetailSerializer

User = get_user_model()


@extend_schema(
    tags=['VehicleUnit']
)
@extend_schema_view(
    rent=extend_schema(
        request=RentalContractCreateOrUpdateSerializer,
        description='Use this endpoint to rent a specific vehicle unit.'
    ),
    sale=extend_schema(
        request=SaleCreateOrUpdateSerializer,
        description='Use this endpoint to sale a specific vehicle unit'
    )
)
class VehicleUnitViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleUnitListSerializer
    permission_classes = [IsAdminOrReadOnly]

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

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def rent(self, request, pk):
        serializer = RentalContractCreateOrUpdateSerializer(data=request.data)
        data, success = services.VehicleUnitService.rent(serializer, vehicle_unit_id=pk, customer_id=request.user.id)

        if success:
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def sale(self, request, pk):
        serializer = SaleCreateOrUpdateSerializer(data=request.data)
        data, success = services.VehicleUnitService.sale(serializer, vehicle_unit_id=pk, customer_id=request.user.id)

        if success:
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(data, status=status.HTTP_400_BAD_REQUEST)
