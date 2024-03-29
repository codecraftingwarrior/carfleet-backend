from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import VehicleUnit


class ApplicationUser(AbstractUser):
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    rented_vehicles = models.ManyToManyField('VehicleUnit', through='RentalContract', related_name='rented_by')
    purchased_vehicles = models.ManyToManyField('VehicleUnit', through='Sale', related_name='customer')

    class Meta:
        ordering = ('first_name', 'last_name',)
