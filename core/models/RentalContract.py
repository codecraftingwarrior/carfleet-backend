from django.contrib.auth.models import User
from django.db import models

from core.models.Customer import Customer
from core.models.VehicleUnit import VehicleUnit


class RentalContract(models.Model):
    rented_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='rental_contracts', null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, related_name='rental_contracts', null=True)
    vehicle = models.ForeignKey(VehicleUnit, on_delete=models.SET_NULL, related_name='rental_contracts', null=True)

    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=12, decimal_places=6)
    conditions = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)