from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Manufacturer
from core.tests.AuthenticationAwareTestCase import AuthenticationAwareTestCase


class TestManufacturers(AuthenticationAwareTestCase):
    list_path = reverse_lazy('manufacturers-list')

    def test_list(self):
        manufacturer = Manufacturer.objects.create(name='Test Manufacturer')
        response = self.client.get(self.list_path, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(manufacturer.name, response.json()[0].get('name'))

    def test_retrieve_detail(self):
        manufacturer = Manufacturer.objects.create(name='Test Manufacturer')

        detail_path = reverse_lazy('manufacturers-detail', kwargs={'pk': manufacturer.id})
        response = self.client.get(detail_path, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(manufacturer.id, response.json().get('id'))

    def test_create(self):
        self.assertFalse(Manufacturer.objects.exists())

        manufacturer = {
            'name': 'Test Manufacturer'
        }

        response = self.client.post(self.list_path, data=manufacturer, format='json')
        created_item = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Manufacturer.objects.filter(pk=created_item.get('id')).exists())

    def test_create_with_already_existing_name_fails(self):
        self.assertFalse(Manufacturer.objects.exists())

        manufacturer = Manufacturer.objects.create(name='Test Manufacturer')

        response = self.client.post(self.list_path, data={'name': manufacturer.name}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.json())
        self.assertIn('already exists', response.json()['name'][0])
        self.assertEqual(Manufacturer.objects.count(), 1)

    def test_update(self):
        manufacturer = Manufacturer.objects.create(name='Test Manufacturer')

        update_path = reverse_lazy('manufacturers-detail', kwargs={'pk': manufacturer.id})

        payload = {'name': 'New manufacturer name'}
        response = self.client.put(update_path, data=payload, format='json')
        updated = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated.get('name'), payload.get('name'))
        self.assertEqual(Manufacturer.objects.filter(pk=manufacturer.id).get().name, payload.get('name'))

    def test_update_with_already_existing_name_fails(self):

        manufacturer = Manufacturer.objects.create(name='Test Manufacturer')
        volkswagen_manufacturer = Manufacturer.objects.create(name='Volkswagen')

        update_path = reverse_lazy('manufacturers-detail', kwargs={'pk': manufacturer.id})

        payload = {'name': volkswagen_manufacturer.name}
        response = self.client.put(update_path, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.json())
        self.assertIn('already exists', response.json().get('name')[0])

    def test_delete(self):

        manufacturer = Manufacturer.objects.create(name='Test Manufacturer')

        self.assertEqual(Manufacturer.objects.count(), 1)

        deletion_path = reverse_lazy('manufacturers-detail', kwargs={'pk': manufacturer.pk})

        response = self.client.delete(deletion_path, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

