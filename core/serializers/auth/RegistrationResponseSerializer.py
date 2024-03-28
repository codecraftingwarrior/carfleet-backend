from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.serializers.group.GroupListSerializer import GroupListSerializer

User = get_user_model()


class RegistrationResponseSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'address', 'phone', 'groups']

    def get_groups(self, instance):
        return GroupListSerializer(instance.groups.all(), many=True).data
