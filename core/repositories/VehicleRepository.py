from core.models import Vehicle


class VehicleRepository:

    @staticmethod
    def find_by_id(vehicle_id):
        return Vehicle.objects.get(pk=vehicle_id)