import pytest

from plantswap.models import Plant
from plantswap.tests.conftest import fake


@pytest.mark.django_db
def test_name_max_length(create_plant):
    plant = Plant.objects.first()
    max_length = plant._meta.get_field('name').max_length
    assert max_length == 64


@pytest.mark.django_db
def test_get_absolute_url(create_plant):
    plant = Plant.objects.first()
    expected_url = f'/plants/detail/{plant.pk}/'
    assert plant.get_absolute_url() == expected_url


@pytest.mark.django_db
def test_object_str_method_is_name(create_plant):
    plant = Plant.objects.first()
    expected_object_name = f'{plant.name}'
    assert str(plant) == expected_object_name


@pytest.mark.django_db
def test_create_plant(client, create_plant):
    """Test that logged in user can add a new plant"""
    plants_count = Plant.objects.count()
    assert plants_count == 4
    response = client.get('/plants/new/')
    assert response.status_code == 200
    new_plant = {
        'name': 'created_plant',
        'status': 1,
        'photo': '',
        'description': fake.sentence(),
        'owner': response.context["user"]
    }
    response = client.post('/plants/new/', data=new_plant)
    assert response.status_code == 302
    last_plant = Plant.objects.get(name='created_plant')
    assert response.url == f'/plants/detail/{last_plant.pk}/'
    response = client.get(response.url)
    assert response.status_code == 200
    assert len(Plant.objects.all()) == 5


@pytest.mark.django_db
def test_update_plant(client, create_plant):
    """Test that logged in user can edit an owned plant"""
    plant = Plant.objects.get(status=3)
    response = client.get(f"/plants/edit/{plant.pk}/")
    assert response.status_code == 200
    plant_data = {
        'name': fake.sentence(nb_words=2),
        'status': 2,
        'photo': '',
        'description': fake.sentence(),
        'owner': response.context["user"]
    }
    response = client.post(f"/plants/edit/{plant.pk}/", data=plant_data)
    assert response.status_code == 302
    assert response.url == f"/plants/detail/{plant.pk}/"
    plant_obj = Plant.objects.get(pk=plant.pk)
    assert plant_obj.description == plant_data['description']
