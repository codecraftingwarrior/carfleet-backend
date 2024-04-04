from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class WebsocketManager:
    WEBSOCKET_INSERTION_ACTION = 'insertion'
    WEBSOCKET_UPDATE_ACTION = 'update'

    @staticmethod
    def send_to_channel(channel_name: str, event_type: str, payload: dict) -> None:
        channel_layer = get_channel_layer()

        payload = {
            'type': event_type,
            **payload
        }

        async_to_sync(channel_layer.group_send)(
            channel_name,
            payload
        )
