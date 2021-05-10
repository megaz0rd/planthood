from datetime import datetime

import pytest

from faker import Faker

from django.test import Client
from django.contrib.auth.models import User

from plantswap.models import Plant, Reminder, Transaction
from plantswap.tests.utils import (
    random_user,
    random_status,
    random_care,
    random_plant, random_plant_for_transaction
)

RECORD_COUNT = 50
fake = Faker("pl_PL")


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def set_up():
    for i in range(RECORD_COUNT):
        User.objects.create(username=fake.name(),
                            email=fake.email(),
                            password=fake.password())
    for i in range(RECORD_COUNT):
        Plant.objects.create(name=fake.name(), description=fake.sentence(),
                             added=fake.date(), status=random_status(),
                             owner=random_user())
    for i in range(RECORD_COUNT):
        plant = random_plant()
        Reminder.objects.create(name=random_care(), plant=plant,
                                previous_care_day=datetime.strptime(
                                    fake.date(), '%Y-%m-%d'),
                                cycle=fake.random_int(min=1, max=14),
                                creator=plant.owner)
    for i in range(RECORD_COUNT):
        plant = random_plant_for_transaction()
        user = random_user()
        while user == plant.owner:
            user = random_user()

        if plant.status == 1:
            Transaction.objects.create(plant=plant, from_user=plant.owner,
                                       to_user=user)
        elif plant.status == 2:
            Transaction.objects.create(plant=plant, from_user=user,
                                       to_user=plant.owner)


@pytest.fixture
def other_user_plant():
    user = User.objects.create(username='foo', password='bar')

    plant_1 = Plant.objects.create(name='Kwiat', description='None',
                                   status=1, owner=user)
    plant_2 = Plant.objects.create(name='Kwiat', description='None',
                                   status=2, owner=user)
    plant_3 = Plant.objects.create(name='Kwiat', description='None',
                                   status=3, owner=user)
    plant_4 = Plant.objects.create(name='Kwiat', description='None',
                                   status=4, owner=user)
    other = {
        'user': user,
        'plant1': plant_1,
        'plant2': plant_2,
        'plant3': plant_3,
        'plant4': plant_4
    }
    return other
