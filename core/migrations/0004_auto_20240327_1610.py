# Generated by Django 3.2.5 on 2024-03-27 15:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_brand_manufacturer'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalcontract',
            name='sale_global_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='sale',
            name='sale_global_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='global_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='vehicleunit',
            name='global_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
