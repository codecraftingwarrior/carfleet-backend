from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.models import Manufacturer
from core.permissions.IsAdmin import IsAdmin
from core.serializers.manufacturer.ManufacturerListSerializer import ManufacturerListSerializer

from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema(
    tags=['Manufacturer']
)
@extend_schema_view(
    list=extend_schema(description='Retrieves the list of the manufacturers'),
    retrieve=extend_schema(description='Retrieves a single manufacturer by id'),
    create=extend_schema(description='Creates a new manufacturer'),
    update=extend_schema(description='Updates a single manufacturer by id'),
    partial_update=extend_schema(description='Updates a specific field for a manufacturer by id'),
    destroy=extend_schema(description='Deletes a specific manufacturer by id')
)
class ManufacturerViewSet(viewsets.ModelViewSet):
    serializer_class = ManufacturerListSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return Manufacturer.objects.all()
