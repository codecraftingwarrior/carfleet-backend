from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.models import Brand
from core.permissions.IsAdmin import IsAdmin
from core.serializers.brand_serializers import BrandListSerializer


@extend_schema(
    tags=['Brands']
)
class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandListSerializer

    permission_classes = [IsAdmin, IsAuthenticated]

    def get_queryset(self):
        return Brand.objects.all()
