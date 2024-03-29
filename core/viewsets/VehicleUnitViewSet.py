from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from core.models import VehicleUnit
from core.models.VehicleUnit import VehicleUnitStatuses
from core.permissions import IsAdminOrReadOnly
from core.serializers.rental_contract.RentalContractCreateOrUpdateSerializer import \
    RentalContractCreateOrUpdateSerializer
from core.serializers.sale.SaleCreateOrUpdateSerializer import SaleCreateOrUpdateSerializer
from core.serializers.vehicle_unit.VehicleUnitCreateOrUpdateSerializer import VehicleUnitCreateOrUpdateSerializer
from core.serializers.vehicle_unit.VehicleUnitDetailSerializer import VehicleUnitDetailSerializer
from core.serializers.vehicle_unit.VehicleUnitListSerializer import VehicleUnitListSerializer

User = get_user_model()


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
        rented_vehicle = VehicleUnit.objects.get(pk=pk)

        if serializer.is_valid():
            rental_contract = serializer.save()
            if rental_contract:
                with transaction.atomic():
                    rental_contract.rented_by = User.objects.filter(id=request.user.id).first()
                    rental_contract.vehicle = rented_vehicle

                    rented_vehicle.status = VehicleUnitStatuses.RENTED
                    rented_vehicle.save()

                    return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def sale(self, request, pk):
        serializer = SaleCreateOrUpdateSerializer(data=request.data)
        sold_vehicle = VehicleUnit.objects.get(pk=pk)

        if serializer.is_valid():
            sale = serializer.save()
            if sale:
                sale.customer = User.objects.filter(id=request.user.id).first()
                sale.vehicle = sold_vehicle

                sold_vehicle.status = VehicleUnitStatuses.SOLD
                sold_vehicle.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
