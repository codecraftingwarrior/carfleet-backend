from rest_framework import serializers

from core.models import RentalContract


class RentalContractCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalContract
        fields = ['start_date', 'end_date', 'total_price', 'conditions']