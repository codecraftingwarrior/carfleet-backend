import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import ApplicationUser
from core.models.Brand import Brand
from core.models.Manufacturer import Manufacturer


class Vehicle(models.Model):
    class VehicleTypes(models.TextChoices):
        SUV = 'SUV', _('SUV')
        SEDAN = 'Sedan', _('SEDAN')
        COUPE = 'Coupe', _('COUPE')
        CONVERTIBLE = 'Convertible', _('CONVERTIBLE')
        PICKUP = 'Pickup', _('PICKUP')
        MINIVAN = 'Minivan', _('MINIVAN')
        VAN = 'Van', _('VAN')
        MOTORCYCLE = 'Motorcycle', _('MOTORCYCLE')

    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, related_name='vehicles', null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, related_name='vehicles', null=True)
    owner = models.ForeignKey('ApplicationUser', on_delete=models.SET_NULL, related_name='vehicles', null=True)

    model = models.CharField(max_length=100)
    global_id = models.UUIDField(default=uuid.uuid4)
    type = models.CharField(max_length=20, choices=VehicleTypes.choices, default=VehicleTypes.SEDAN)
    year = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.model
