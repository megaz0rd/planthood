import pytest
from django.contrib.auth.models import User

from plantswap.models import Plant


@pytest.mark.django_db
def test_user_model(user):
    assert len(User.objects.all()) == 1
    assert User.objects.get(username="JohnDoe") == user


@pytest.mark.django_db
def test_plant_model(plant):
    assert len(Plant.objects.all()) == 1
    assert Plant.objects.get(name="Kwiatek") == plant


@pytest.mark.django_db
def test_login(client):
    response = client.post('/accounts/login/', {'username': 'username',
                                                'password': 'password'})
    assert response.status_code == 200


def test_logout(client):
    response = client.get('/accounts/logout/', {})
    assert response.status_code == 200


@pytest.mark.django_db
def test_index_views(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_plants_list_view(client, user):
    client.login(username=user.username, password=user.password)
    response = client.get('/plants/', follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_transactions_list_view(client, user):
    login = client.post('/accounts/login/', {'username': 'JohnDoe',
                                             'password': 'Str0ng_password!'})
    response = client.get('/transactions/')
    assert response.status_code == 200
