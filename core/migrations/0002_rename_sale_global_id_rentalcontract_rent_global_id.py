# Generated by Django 3.2.5 on 2024-03-28 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rentalcontract',
            old_name='sale_global_id',
            new_name='rent_global_id',
        ),
    ]