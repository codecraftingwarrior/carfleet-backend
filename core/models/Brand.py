from django.db import models

from core.models import Manufacturer


class Brand(models.Model):
    name = models.CharField(max_length=255)
    origin_country = models.CharField(max_length=100, blank=True, null=True)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.SET_NULL, null=True, related_name='brands')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
