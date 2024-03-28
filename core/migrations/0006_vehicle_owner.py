# Generated by Django 3.2.5 on 2024-03-28 07:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_vehicleunit_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vehicles', to=settings.AUTH_USER_MODEL),
        ),
    ]
