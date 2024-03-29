import random

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import BaseCommand, call_command
from django.db import transaction
from django.contrib.auth.hashers import make_password
from faker import Faker

from core.models import ApplicationUser, Brand, RentalContract, Manufacturer, Sale, Vehicle, VehicleUnit

User = get_user_model()


class Command(BaseCommand):
    help = 'Populates the database with dummy data'
    fake = Faker('en_US')
    item_size = 0

    def add_arguments(self, parser):
        parser.add_argument('--purge-db', action='store_true', help="Purges the database before populate it")
        parser.add_argument('item_size', type=int, help="Minimum number of items to generate for each table")

    def handle(self, *args, **options):
        if options['purge_db']:
            confirm = input("Do you really want to purge the database before populating it ? (Yes/No) ")
            if confirm.lower() == 'yes':
                self.stdout.write(self.style.SUCCESS('Start purging the database'))
                call_command('flush', interactive=False)
                self.stdout.write(self.style.SUCCESS('Database purged successfully'))

        if options['item_size']:
            self.item_size = options['item_size']
            self.stdout.write(self.style.SUCCESS(f'Populating {self.item_size} items on each table......'))

            self.populate()

            self.stdout.write(self.style.SUCCESS('Database populated successfully'))

    def populate(self):
        groups = [
            Group(name='Admin'),
            Group(name='Customer')
        ]
        brands = ["Toyota", "Honda", "BMW", "Ducati", "Ford", "Harley-Davidson", "Nissan", "Kawasaki", "Tesla",
                  "Yamaha"]
        manufacturers = ["Peugeot", "Renault", "Volkswagen", "Mercedes-Benz", "Audi", "Chevrolet", "Fiat", "Ford",
                         "Hyundai", "Toyota"]
        vehicle_models = [
            "Mustang",
            "Camaro",
            "Corolla",
            "Civic",
            "3 Series",
            "A4",
            "C-Class",
            "Golf",
            "Elantra",
            "Optima",
            "Altima",
            "3",
            "Impreza",
            "Clio",
            "208",
            "500",
            "Charger",
            "Multistrada",  # Modèle de moto Ducati
            "Ninja 650",  # Modèle de moto Kawasaki
            "Bonneville"  # Modèle de moto Triumph
        ]

        models_by_inserter = {
            'ApplicationUser': lambda: ApplicationUser.objects.create(
                first_name=self.fake.first_name(),
                last_name=self.fake.last_name(),
                email=self.fake.unique.email(),
                username=self.fake.unique.email(),
                address=self.fake.address(),
                phone=self.fake.bothify('############'),
                password=make_password('thereisapwd'),
            ),
            'Manufacturer': lambda: Manufacturer.objects.create(
                name=random.choice(manufacturers),
                address=self.fake.address(),
                contact=self.fake.phone_number()
            ),
            'Brand': lambda: Brand.objects.create(
                name=random.choice(brands),
                origin_country=self.fake.country(),
                manufacturer=random.choice(Manufacturer.objects.all())
            ),
            'Vehicle': lambda: Vehicle.objects.create(
                manufacturer=random.choice(Manufacturer.objects.all()),
                brand=random.choice(Brand.objects.all()),
                owner=random.choice(User.objects.all()),
                model=random.choice(vehicle_models),
                year=self.fake.year(),
                description=self.fake.text()
            ),
            'VehicleUnit': lambda: VehicleUnit.objects.create(
                vehicle=random.choice(Vehicle.objects.all()),
                plate_number=self.fake.bothify(text='??-###-??'),
                mileage=self.fake.bothify(text='######'),
                color=self.fake.color_name(),
                price=float(self.fake.bothify(text='##.##')),
            )
        }

        with transaction.atomic():
            Group.objects.bulk_create(groups)

            for i in range(self.item_size):
                for model in models_by_inserter:
                    instance = models_by_inserter.get(model)()
                    if model == 'ApplicationUser':
                        group = random.choice(Group.objects.all())
                        group.user_set.add(instance)
