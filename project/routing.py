from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from core.consumers import VehicleConsumer, SingleVehicleConsumer

websocket_urlpatterns = [
    path('ws/vehicles/', VehicleConsumer.as_asgi()),
    path('ws/vehicles/<str:global_id>/observe/', SingleVehicleConsumer.as_asgi())
]
