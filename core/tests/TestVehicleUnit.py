from django.urls import reverse_lazy
from rest_framework import status

from core.tests.AuthenticationAwareTestCase import AuthenticationAwareTestCase


class TestVehicleUnit(AuthenticationAwareTestCase):
    authenticate_before_each = False

    def test_list(self):
        path = reverse_lazy('vehicle-units-list')

        response = self.client.get(path, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_must_fail_for_guest_only(self):
        path = reverse_lazy('vehicle-units-list')

        payload = {
            'plate_number': 'FJ-799-MN',
            'mileage': '150000',
            'color': 'red',
            'price': 47
        }

        response = self.client.post(path, data=payload, format='json')
        # must fail for guest user
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        authentication_response = self.authenticate_and_get_response(is_admin=True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + authentication_response.json().get('access'))

        response = self.client.post(path, data=payload, format='json')

        # must success for admin user
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
