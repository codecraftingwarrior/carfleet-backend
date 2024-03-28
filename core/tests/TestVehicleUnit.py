from django.urls import reverse_lazy
from rest_framework import status

from core.models import Vehicle, Brand, Manufacturer, VehicleUnit, RentalContract
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

    def test_rent_must_success(self):
        self.assertFalse(RentalContract.objects.exists())

        vehicle = Vehicle.objects.create(
            model='Test model',
            type='Sedan',
            year=2010,
            description='Test description',
            brand=Brand.objects.create(name='Test brand', origin_country='Test country'),
            manufacturer=Manufacturer.objects.create(name='Test manufacturer', address='Test address',
                                                     contact='Test contact')
        )

        vehicle_unit = VehicleUnit.objects.create(
            vehicle=vehicle,
            plate_number='FJ-799-MN',
            mileage='175000',
            color='black',
            price=78
        )

        authentication_response = self.authenticate_and_get_response(is_admin=False)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + authentication_response.json().get('access'))

        path = reverse_lazy('vehicle-units-rent', kwargs={'pk': vehicle_unit.id})

        payload = {
            'start_date': '2020-01-01',
            'end_date': '2020-12-31',
            'total_price': 100000,
            'conditions': 'Test conditions',
            'vehicle': vehicle.id
        }

        response = self.client.post(path, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(RentalContract.objects.exists())
