from django.contrib.auth.models import User
from django.db import models

from core.models.Customer import Customer
from core.models.VehicleUnit import VehicleUnit


class Sale(models.Model):
    sold_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sales', null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, related_name='sales', null=True)
    vehicle = models.ForeignKey(VehicleUnit, on_delete=models.SET_NULL, related_name='sales', null=True)

    sale_date = models.DateField()
    price = models.DecimalField(max_digits=12, decimal_places=6)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)