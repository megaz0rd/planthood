import uuid
import pytest
from datetime import datetime
from django.test import Client
from django.contrib.auth.models import User
from faker import Faker

from members.models import UserProfile
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


@pytest.fixture
def test_password():
    return 'strong-test-password'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
            client.login(username=user.username, password=test_password)
            return client, user

    return make_auto_login


@pytest.fixture
def create_profile(client, auto_login_user):
    client, user = auto_login_user()
    return UserProfile.objects.create(user=user,
                                      street='street',
                                      building_number=1)


@pytest.fixture
def other_user_plant(create_user):
    user = create_user(username='other')

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


@pytest.fixture
def create_plant(auto_login_user):
    client, user = auto_login_user()
    for i in range(4):
        Plant.objects.create(
            name=fake.sentence(nb_words=2),
            status=i + 1,
            photo='',
            description=fake.sentence(),
            owner=user
        )


@pytest.fixture
def create_reminder(create_plant):
    plant = Plant.objects.get(status=3)
    Reminder.objects.create(name=random_care(), plant=plant,
                            previous_care_day=datetime.strptime(
                                fake.date(), '%Y-%m-%d'),
                            cycle=fake.random_int(min=1, max=14),
                            creator=plant.owner)


@pytest.fixture
def create_transaction(auto_login_user, create_reminder, create_user):
    user2 = create_user(username='user2transaction')
    plant_status_1 = Plant.objects.get(status=1)
    plant_status_2 = Plant.objects.get(status=2)
    transaction_1 = Transaction.objects.create(plant=plant_status_1,
                                               from_user=plant_status_1.owner,
                                               to_user=user2)
    transaction_2 = Transaction.objects.create(plant=plant_status_2,
                                               to_user=plant_status_2.owner,
                                               from_user=user2)
    return transaction_1, transaction_2


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
