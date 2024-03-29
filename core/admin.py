from django.contrib import admin
from django.contrib.admin import register

from core.models import Brand, Manufacturer, Vehicle, VehicleUnit, ApplicationUser

# Register your models here.



@register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'origin_country', 'manufacturer']

    @admin.display(empty_value='-')
    def manufacturer(self, instance):
        return instance.manufacturer.name


@register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'contact']


@register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['model', 'type', 'year', 'owner', 'brand', 'manufacturer']

    @admin.display(empty_value='-')
    def owner(self, instance):
        return instance.owner.name

    @admin.display(empty_value='-')
    def brand(self, instance):
        return instance.brand.name

    @admin.display(empty_value='-')
    def manufacturer(self, instance):
        return instance.manufacturer.name


@register(VehicleUnit)
class VehicleUnitAdmin(admin.ModelAdmin):
    list_display = ['plate_number', 'mileage', 'status', 'color', 'price', 'vehicle']

    @admin.display(empty_value='-')
    def mileage(self, instance):
        return round(instance.mileage, 2)


@register(ApplicationUser)
class ApplicationUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'is_active']
