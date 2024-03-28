from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Brand
from core.tests.AuthenticationAwareTestCase import AuthenticationAwareTestCase


class TestBrand(AuthenticationAwareTestCase):

    def test_list_brands(self):
        path = reverse_lazy('brands-list')

        response = self.client.get(path, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_brand(self):
        brand = Brand.objects.create(
            name='Brand',
            origin_country='Japan'
        )
        path = reverse_lazy('brands-detail', kwargs={'pk': brand.pk})

        response = self.client.get(path, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(brand.pk, response.json().get('id'))

    def test_create_brand(self):
        self.assertFalse(Brand.objects.exists())

        path = reverse_lazy('brands-list')

        payload = {
            'name': 'New Brand',
            'origin_country': 'Japan'
        }

        response = self.client.post(path, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Brand.objects.exists())
        self.assertEqual(Brand.objects.get().pk, response.json().get('id'))

    def test_create_with_name_already_exists_fails(self):
        self.assertFalse(Brand.objects.exists())

        path = reverse_lazy('brands-list')

        volkswagen_brand = Brand.objects.create(
            name='Volkswagen',
            origin_country='Germany'
        )

        self.assertEqual(Brand.objects.count(), 1)

        response = self.client.post(path, data={
            'name': volkswagen_brand.name,
            'origin_country': 'Japan'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.json())
        self.assertIn('already exists', response.json().get('name')[0])

    def test_update_brand(self):
        brand = Brand.objects.create(name='New Brand', origin_country='Country')

        path = reverse_lazy('brands-detail', kwargs={'pk': brand.id})

        response = self.client.put(path, data={'name': 'New Brand Name'})

        updated_brand = Brand.objects.first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_brand.name, response.json().get('name'))
        self.assertEqual(brand.id, updated_brand.id)

    def test_update_with_already_exists_name_fails(self):
        self.assertFalse(Brand.objects.exists())

        brand = Brand.objects.create(name='New Brand', origin_country='Country')
        Brand.objects.create(name='Given Brand', origin_country='Given Country')

        path = reverse_lazy('brands-detail', kwargs={'pk': brand.id})

        response = self.client.put(path, data={'name': 'Given Brand'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.json())
        self.assertIn('already exists', response.json().get('name')[0])

    def test_delete_brand(self):
        self.assertFalse(Brand.objects.exists())

        brand = Brand.objects.create(name='New Brand', origin_country='Country')

        self.assertEqual(Brand.objects.count(), 1)

        path = reverse_lazy('brands-detail', kwargs={'pk': brand.id})
        response = self.client.delete(path, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Brand.objects.exists())
