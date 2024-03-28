from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.models import Manufacturer
from core.permissions.IsAdmin import IsAdmin
from core.serializers.manufacturer.ManufacturerListSerializer import ManufacturerListSerializer


class ManufacturerViewSet(viewsets.ModelViewSet):
    serializer_class = ManufacturerListSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return Manufacturer.objects.all()
