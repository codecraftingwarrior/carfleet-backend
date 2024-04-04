from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse_lazy

from core.consumers import VehicleConsumer

User = get_user_model()


class TestVehicleConsumer(TestCase):
    base_path = '/ws/vehicles/'

    async def test_connection_without_token_must_fail(self):
        communicator = WebsocketCommunicator(VehicleConsumer.as_asgi(), self.base_path)
        connected, _ = await communicator.connect()

        self.assertFalse(connected)

    async def test_connection_with_token_must_succeed(self):
        async_authenticate = sync_to_async(self.authenticate, thread_sensitive=True)

        response = await async_authenticate()
        access_token = response.json().get('access')
        path = self.base_path + '?token=' + access_token
        communicator = WebsocketCommunicator(VehicleConsumer.as_asgi(), path)
        connected, _ = await communicator.connect()

        self.assertTrue(connected)

        await communicator.disconnect()

    def authenticate(self):
        user = User.objects.create_user(username='test_username', email='test_email@test.fr', password='test_password')
        login_check_url = reverse_lazy('token-obtain-pair')
        credentials = {
            "username": user.username,
            "password": 'test_password'
        }
        response = self.client.post(login_check_url, data=credentials, format='json')
        return response
