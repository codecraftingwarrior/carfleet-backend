from core.models import Sale
from rest_framework import serializers


class SaleCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['sale_date', 'price']