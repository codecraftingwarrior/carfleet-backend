from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.serializers.auth_serializers import RegistrationSerializer, RegistrationResponseSerializer


@extend_schema(
    tags=['Authentication']
)
class AuthViewSet(viewsets.ViewSet):
    permission_classes_by_action = {
        'register': [AllowAny]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return super().get_permissions()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            if user:
                registration_response_serializer = RegistrationResponseSerializer(user)
                return Response(registration_response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
