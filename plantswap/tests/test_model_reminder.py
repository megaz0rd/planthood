import pytest

from plantswap.models import Plant, Reminder
from plantswap.tests.utils import random_care


@pytest.mark.django_db
def test_create_reminder(client, create_own_plant):
    plant = Plant.objects.first()
    response = client.get('/reminders/')
    assert response.status_code == 200
    assert len(Reminder.objects.all()) == 0
    response = client.get('/reminders/new/')
    assert response.status_code == 200
    reminder_data = {
        'name': random_care(),
        'plant': plant,
        'cycle': 5,
        'previous_care_day': '2021-05-10',
    }

    response = client.post('/reminders/new/', reminder_data)
    assert response.status_code == 200
    assert len(Reminder.objects.all()) == 1


@pytest.mark.django_db
def test_update_reminder(client, create_own_plant, create_reminder):
    plant = Plant.objects.first()
    reminder = create_reminder(plant=plant)
    assert len(Reminder.objects.all()) == 1

    response = client.get(f"/reminders/edit/{reminder.pk}/")
    assert response.status_code == 200
    reminder_data = {
        'name': random_care(),
        'cycle': 14,
        'previous_care_day': '2021-05-10'
    }
    response = client.post(f"/reminders/edit/{reminder.pk}/", reminder_data)
    assert response.status_code == 200
    assert len(Reminder.objects.all()) == 1
    reminder_obj = Reminder.objects.get(pk=reminder.pk)
    assert reminder_obj.cycle == reminder_data['cycle']
