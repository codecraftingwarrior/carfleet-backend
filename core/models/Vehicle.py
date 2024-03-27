from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.Brand import Brand
from core.models.Manufacturer import Manufacturer


class Vehicle(models.Model):
    class VehicleTypes(models.TextChoices):
        SUV = 'SUV', _('SUV')
        SEDAN = 'Sedan', _('SED')
        COUPE = 'Coupe', _('COUPE')
        CONVERTIBLE = 'Convertible', _('CONV')
        PICKUP = 'Pickup', _('PICK')
        MINIVAN = 'Minivan', _('MINVAN')
        VAN = 'Van', _('VAN')
        MOTORCYCLE = 'Motorcycle', _('MOTC')

    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, related_name='vehicles', null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, related_name='vehicles', null=True)

    model = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=VehicleTypes.choices, default=VehicleTypes.SEDAN)
    year = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2),
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)