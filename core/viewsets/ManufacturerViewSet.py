from rest_framework import viewsets

from core.models import Manufacturer
from core.serializers.manufacturer.ManufacturerListSerializer import ManufacturerListSerializer


class ManufacturerViewSet(viewsets.ModelViewSet):
    serializer_class = ManufacturerListSerializer
    # permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Manufacturer.objects.all()
