from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class TestAuth(APITestCase):

    def test_customer_registration(self):
        path = reverse_lazy('auth-register')

        payload = {
            'first_name': 'John',
            'last_name': 'Smith',
            'address': '123 Main Street',
            'phone': '0123456789',
            'email': 'test@test.fr',
            'password': 'thereisapassword'
        }

        response = self.client.post(path, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=payload.get('email')).exists())
        self.assertTrue(User.objects.filter(email=payload.get('email')).get().groups.filter(name='Customer').exists())
        self.assertTrue("groups" in response.json())
