from core import repositories, services
from core.models import Vehicle
from core.serializers.vehicle_serializers import VehicleDetailSerializer


class VehicleService:

    @staticmethod
    def get_add_websocket_payload(vehicle_id: int) -> dict:
        serializer = VehicleDetailSerializer(repositories.VehicleRepository.find_by_id(vehicle_id))

        payload = {
            'meta': {
                'perimeter': 'vehicle',
                'action': services.WebsocketManager.WEBSOCKET_INSERTION_ACTION
            },
            'data': serializer.data
        }

        return payload

    @staticmethod
    def get_update_websocket_payload(user_username: str, instance: Vehicle) -> dict:
        payload = {
            'meta': {
                'updated_by': user_username,
                'perimeter': 'vehicle',
                'action': services.WebsocketManager.WEBSOCKET_UPDATE_ACTION
            },
            'data': VehicleDetailSerializer(instance).data
        }

        return payload
