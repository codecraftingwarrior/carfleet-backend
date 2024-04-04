from django.contrib.auth import get_user_model
from rest_framework import serializers

from core import services, enums
from core.serializers.group_serializers import GroupListSerializer

User = get_user_model()


class RegistrationResponseSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'address', 'phone', 'groups']

    def get_groups(self, instance):
        return GroupListSerializer(instance.groups.all(), many=True).data


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    user_type = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'address', 'phone', 'email', 'password', 'user_type']

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')

        role = enums.BasicRole.ADMIN if user_type == 'admin' else enums.BasicRole.CUSTOMER

        return services.ApplicationUserService.create_user(
            role=role,
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            address=validated_data['address'],
            phone=validated_data['phone'],
            password=validated_data['password']
        )
