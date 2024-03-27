from rest_framework import viewsets, serializers

from core.models import Brand
from core.serializers import BrandListSerializer


class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandListSerializer

    def get_queryset(self):
        return Brand.objects.all()