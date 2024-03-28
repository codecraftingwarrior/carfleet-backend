from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from rest_framework.test import APITestCase

User = get_user_model()


class AuthenticationAwareTestCase(APITestCase):
    authenticate_before_each = True

    def setUp(self):
        if self.authenticate_before_each:
            response = self.authenticate_and_get_response(is_admin=True)
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.json().get('access'))

    def authenticate_and_get_response(self, is_admin=False):
        mock_username = "test_username"
        mock_password = "test_password"
        mock_email = "test_email@test.fr"

        if is_admin:
            user = User.objects.create_user(username=mock_username, email=mock_email, password=mock_password)
            admin_group, _ = Group.objects.get_or_create(name="Admin")
            admin_group.user_set.add(user)
        else:
            user = User.objects.create_user(username=mock_username, email=mock_email, password=mock_password)
            customer_group, _ = Group.objects.get_or_create(name="Customer")
            customer_group.user_set.add(user)

        login_check_url = reverse_lazy('token-obtain-pair')

        credentials = {
            "username": mock_username,
            "password": mock_password
        }

        response = self.client.post(login_check_url, data=credentials, format='json')

        return response
