from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255)
    origin_country = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)