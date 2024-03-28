import uuid

from django.contrib.auth.models import User
from django.db import models

from core.models.ApplicationUser import ApplicationUser
from core.models.VehicleUnit import VehicleUnit


class Sale(models.Model):
    sold_by = models.ForeignKey(ApplicationUser, on_delete=models.SET_NULL, related_name='sales', null=True)
    customer = models.ForeignKey(ApplicationUser, on_delete=models.SET_NULL, related_name='sale_customers', null=True)
    vehicle = models.ForeignKey(VehicleUnit, on_delete=models.SET_NULL, related_name='sales', null=True)

    sale_date = models.DateField()
    price = models.DecimalField(max_digits=12, decimal_places=6)
    sale_global_id = models.UUIDField(default=uuid.uuid4)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)