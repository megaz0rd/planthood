from django.test import Client
from django.contrib.auth.models import User

from plantswap.models import Plant

import pytest


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user():
    user = User.objects.create(username='JohnDoe',
                               email='johndoe@hotmail.com',
                               password='Str0ng_password!')
    return user


@pytest.fixture
def plant(user):
    plant = Plant.objects.create(name='Kwiatek', description='bratek',
                                 added='2021-02-02', status=1, owner=user)
    return plant
