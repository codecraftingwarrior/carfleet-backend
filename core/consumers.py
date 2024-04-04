import json
from uuid import UUID

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404

from core.serializers.vehicle.VehicleDetailSerializer import VehicleDetailSerializer
from core.models import Vehicle

VEHICLE_SUBSCRIBER_GROUP_NAME = 'vehicle_subscribers'

WEBSOCKET_INSERTION_ACTION = 'insertion'
WEBSOCKET_UPDATE_ACTION = 'update'


class VehicleConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(VEHICLE_SUBSCRIBER_GROUP_NAME, self.channel_name)

        if 'user' not in self.scope or isinstance(self.scope['user'], AnonymousUser):
            await self.close(code=403)
        else:
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            VEHICLE_SUBSCRIBER_GROUP_NAME,
            self.channel_name
        )

    async def vehicle_added(self, event):
        await self.send(text_data=json.dumps(event))


class SingleVehicleConsumer(AsyncWebsocketConsumer):
    vehicle_global_id = None
    current_channel_name = None
    instance = None

    async def connect(self):
        self.vehicle_global_id = self.scope['url_route']['kwargs']['global_id']
        self.instance = await self.fetch_vehicle()
        self.current_channel_name = VEHICLE_SUBSCRIBER_GROUP_NAME + '_target_' + str(self.instance.id)

        await self.channel_layer.group_add(
            self.current_channel_name,
            self.channel_name
        )

        if isinstance(self.scope['user'], AnonymousUser):
            await self.close(code=403)
        else:
            await self.accept()

    async def disconnect(self, close_code):
        if self.vehicle_global_id is not None:
            await self.channel_layer.group_discard(
                self.current_channel_name,
                self.channel_name
            )

    async def vehicle_updated(self, event):
        event['data'] = await self.get_data()

        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def fetch_vehicle(self):
        return get_object_or_404(Vehicle, global_id=self.vehicle_global_id)

    @database_sync_to_async
    def get_data(self):
        serializer = VehicleDetailSerializer(get_object_or_404(Vehicle, global_id=self.vehicle_global_id))
        return serializer.data
