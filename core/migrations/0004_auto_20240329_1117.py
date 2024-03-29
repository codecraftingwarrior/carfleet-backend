# Generated by Django 3.2.5 on 2024-03-29 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_rentalcontract_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='sold_by',
        ),
        migrations.AlterField(
            model_name='sale',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchases', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sale',
            name='vehicle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales', to='core.vehicleunit'),
        ),
    ]