import uuid

from django.db import models

from core.models.Vehicle import Vehicle
from django.utils.translation import gettext_lazy as _


class VehicleUnitStatuses(models.TextChoices):
    AVAILABLE = 'AVAILABLE', _('AVAILABLE'),
    RENTED = 'RENTED', _('RENTED')
    SOLD = 'SOLD', _('SOLD')


class VehicleUnit(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, related_name='units', null=True)

    plate_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=VehicleUnitStatuses.choices, default=VehicleUnitStatuses.AVAILABLE)
    global_id = models.UUIDField(default=uuid.uuid4)
    mileage = models.DecimalField(max_digits=12, decimal_places=6)
    color = models.CharField(max_length=20, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.vehicle.brand.name} {self.vehicle.model} {self.plate_number}'

    class Meta:
        ordering = ('-created_at',)
