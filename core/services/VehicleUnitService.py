from django.db import transaction
from typing import Tuple

from core import repositories
from core.models.VehicleUnit import VehicleUnitStatuses
from core.serializers.sale_serializers import SaleCreateOrUpdateSerializer
from core.serializers.rental_contract_serializers import RentalContractCreateOrUpdateSerializer


class VehicleUnitService:

    @staticmethod
    def sale(serializer: SaleCreateOrUpdateSerializer, vehicle_unit_id: int, customer_id: int) -> Tuple:

        if serializer.is_valid():
            sale = serializer.save()
            if sale:
                with transaction.atomic():
                    sold_vehicle = repositories.VehicleUnitRepository.find_by_id(vehicle_unit_id=vehicle_unit_id)
                    sale.customer = repositories.UserRepository.find_by_id(customer_id)
                    sale.vehicle = sold_vehicle

                    sold_vehicle.status = VehicleUnitStatuses.SOLD
                    sold_vehicle.save()

                    return serializer.data, True
        return serializer.errors, False

    @staticmethod
    def rent(serializer: RentalContractCreateOrUpdateSerializer, vehicle_unit_id: int, customer_id: int) -> Tuple:
        rented_vehicle = repositories.VehicleUnitRepository.find_by_id(vehicle_unit_id=vehicle_unit_id)

        if serializer.is_valid():
            rental_contract = serializer.save()
            if rental_contract:
                with transaction.atomic():
                    rental_contract.rented_by = repositories.UserRepository.find_by_id(user_id=customer_id)
                    rental_contract.vehicle = rented_vehicle

                    rented_vehicle.status = VehicleUnitStatuses.RENTED
                    rented_vehicle.save()

                    return serializer.data, True
        return serializer.errors, False
