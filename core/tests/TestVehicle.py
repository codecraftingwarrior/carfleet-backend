from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Vehicle, Brand, Manufacturer
from core.tests.AuthenticationAwareTestCase import AuthenticationAwareTestCase


class TestVehicle(AuthenticationAwareTestCase):

    def test_list(self):
        self.assertFalse(Vehicle.objects.exists())
        vehicle = Vehicle.objects.create(
            model='Test model',
            type='Sedan',
            year=2010,
            description='Test description',
            brand=Brand.objects.create(name='Test brand', origin_country='Test country'),
            manufacturer=Manufacturer.objects.create(name='Test manufacturer', address='Test address',
                                                     contact='Test contact')
        )

        path = reverse_lazy('vehicles-list')

        response = self.client.get(path, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vehicle.objects.count(), 1)
        self.assertIsNotNone(response.json())
        self.assertEqual(response.json()[0].get('id'), vehicle.id)

    def test_detail(self):
        vehicle = Vehicle.objects.create(
            model='Test model',
            type='Sedan',
            year=2010,
            description='Test description',
            brand=Brand.objects.create(name='Test brand', origin_country='Test country'),
            manufacturer=Manufacturer.objects.create(name='Test manufacturer', address='Test address',
                                                     contact='Test contact')
        )

        path = reverse_lazy('vehicles-detail', kwargs={'pk': vehicle.id})

        response = self.client.get(path, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('brand', response.json())
        self.assertIn('manufacturer', response.json())
        self.assertTrue(isinstance(response.json().get('brand'), dict))
        self.assertTrue(isinstance(response.json().get('manufacturer'), dict))

    def test_create(self):
        brand = Brand.objects.create(name='Test brand', origin_country='Test country')
        manufacturer = Manufacturer.objects.create(name='Test manufacturer', address='Test address',
                                                   contact='Test contact')
        path = reverse_lazy('vehicles-list')
        payload = {
            'model': 'Test model',
            'type': 'Sedan',
            'year': 2010,
            'description': 'Test description',
            'brand': brand.id,
            'manufacturer': manufacturer.id
        }

        response = self.client.post(path, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(isinstance(response.json(), dict))
        self.assertTrue(Vehicle.objects.filter(id=response.json().get('id')).exists())

    def test_create_with_model_type_year_already_exists_must_fail(self):
        self.assertFalse(Vehicle.objects.exists())

        brand = Brand.objects.create(name='Test brand', origin_country='Test country')
        manufacturer = Manufacturer.objects.create(name='Test manufacturer', address='Test address',
                                                   contact='Test contact')

        vehicle = Vehicle.objects.create(
            model='Test model',
            type='Sedan',
            year=2010,
            description='Test description',
            brand=brand,
            manufacturer=manufacturer
        )

        path = reverse_lazy('vehicles-list')
        payload = {
            'model': vehicle.model,
            'type': vehicle.type,
            'year': vehicle.year,
            'description': 'Test description',
            'brand': brand.id,
            'manufacturer': manufacturer.id
        }

        response = self.client.post(path, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.json())
        self.assertIn('This vehicle already exists', response.json()['non_field_errors'])

    def test_update(self):
        brand = Brand.objects.create(name='Test brand', origin_country='Test country')
        manufacturer = Manufacturer.objects.create(name='Test manufacturer', address='Test address',
                                                   contact='Test contact')
        vehicle = Vehicle.objects.create(
            model='Test model',
            type='Sedan',
            year=2010,
            description='Test description',
            brand=brand,
            manufacturer=manufacturer
        )

        update_path = reverse_lazy('vehicles-detail', kwargs={'pk': vehicle.id})
        payload = {
            'model': 'New model name',
            'type': vehicle.type,
            'year': vehicle.year,
            'description': vehicle.description,
            'brand': brand.id,
            'manufacturer': manufacturer.id
        }

        response = self.client.put(update_path, data=payload, format='json')
        updated = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Vehicle.objects.filter(id=vehicle.id).first().model == 'New model name')
        self.assertEqual(updated.get('model'), 'New model name')
        self.assertIn('brand', response.json())
        self.assertIn('manufacturer', response.json())
        self.assertTrue(isinstance(response.json().get('brand'), dict))
        self.assertTrue(isinstance(response.json().get('manufacturer'), dict))

    def test_update_with_already_existing_type_model_and_year_must_fail(self):
        brand = Brand.objects.create(name='Test brand', origin_country='Test country')
        manufacturer = Manufacturer.objects.create(name='Test manufacturer', address='Test address',
                                                   contact='Test contact')
        vehicle = Vehicle.objects.create(
            model='Test model',
            type='Sedan',
            year=2010,
            description='Test description',
            brand=brand,
            manufacturer=manufacturer
        )

        passat = Vehicle.objects.create(
            model='Passat',
            type='Sedan',
            year=2006,
            description='This is a nice car',
            brand=brand,
            manufacturer=manufacturer
        )

        path = reverse_lazy('vehicles-detail', kwargs={'pk': vehicle.id})

        response = self.client.put(path, data={'model': 'Passat', 'year': 2006, 'type': 'Sedan'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.json())
        self.assertIn('This vehicle already exists', response.json().get('non_field_errors'))

    def test_delete(self):
        self.assertFalse(Vehicle.objects.exists())

        vehicle = Vehicle.objects.create(
            model='Test model',
            type='Sedan',
            year=2010,
            description='Test description',
            brand=Brand.objects.create(name='Test brand', origin_country='Test country'),
            manufacturer=Manufacturer.objects.create(name='Test manufacturer', address='Test address',
                                                     contact='Test contact')
        )

        self.assertTrue(Vehicle.objects.exists())
        self.assertEqual(Vehicle.objects.count(), 1)

        path = reverse_lazy('vehicles-detail', kwargs={'pk': vehicle.id})

        response = self.client.delete(path, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vehicle.objects.exists())
        self.assertFalse(Vehicle.objects.filter(id=vehicle.id).exists())
