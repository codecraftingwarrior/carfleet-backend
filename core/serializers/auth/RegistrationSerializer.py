from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

User = get_user_model()


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
        customer_group, _ = Group.objects.get_or_create(name='Customer')
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        user_type = validated_data.pop('user_type')

        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            address=validated_data['address'],
            phone=validated_data['phone']
        )
        user.set_password(validated_data['password'])

        if user_type == 'customer':
            customer_group.user_set.add(user)
        elif user_type == 'admin':
            customer_group.user_set.add(admin_group)

        return user
