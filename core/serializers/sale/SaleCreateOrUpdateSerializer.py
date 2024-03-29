from rest_framework import serializers

from core.models import Sale


class SaleCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['sale_date', 'price']