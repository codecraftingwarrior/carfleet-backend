import json

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

VEHICLE_SUBSCRIBER_GROUP_NAME = 'vehicle_subscribers'


class VehicleConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(VEHICLE_SUBSCRIBER_GROUP_NAME, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            VEHICLE_SUBSCRIBER_GROUP_NAME,
            self.channel_name
        )

    async def vehicle_added(self, event):
        await self.send(text_data=json.dumps(event))
