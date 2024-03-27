from django.db import models

from core.models.Vehicle import Vehicle
from django.utils.translation import gettext_lazy as _


class VehicleUnit(models.Model):
    class VehicleUnitStatuses(models.TextChoices):
        AVAILABLE = 'AVAILABLE', _('AV'),
        RENTED = 'RENTED', _('RN')
        SOLD = 'SOLD', _('SL')

    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, related_name='units', null=True)

    plate_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=VehicleUnitStatuses.choices, default=VehicleUnitStatuses.AVAILABLE)
    mileage = models.DecimalField(max_digits=12, decimal_places=6)
    color = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
