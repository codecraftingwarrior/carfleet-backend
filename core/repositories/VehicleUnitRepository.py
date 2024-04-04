from core.models import VehicleUnit


class VehicleUnitRepository:

    @staticmethod
    def find_by_id(vehicle_unit_id: int) -> VehicleUnit:
        return VehicleUnit.objects.get(pk=vehicle_unit_id)
