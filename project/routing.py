from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from core import consumers

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/vehicles/', consumers.VehicleConsumer),
    ]),
})