import pytest

from plantswap.models import Reminder, Plant


@pytest.mark.django_db
def test_name_max_length(create_reminder):
    reminder = Reminder.objects.first()
    max_length = reminder._meta.get_field('name').max_length
    assert max_length == 9


@pytest.mark.django_db
def test_object_str_method_is_plant_name_and_care_name(create_reminder):
    reminder = Reminder.objects.first()
    expected_object_name = f'{reminder.plant.name} {reminder.name}'
    assert str(reminder) == expected_object_name


@pytest.mark.django_db
def test_create_reminder(client, create_reminder):
    reminders_count = Reminder.objects.count()
    assert reminders_count == 1
    response = client.get('/reminders/')
    assert response.status_code == 200
    response = client.get('/reminders/new/')
    assert response.status_code == 200
    plant = Plant.objects.get(status=3)
    reminder_data = {
        'name': 'WATER',
        'plant': plant.pk,
        'previous_care_day': '2021-05-13',
        'cycle': 5,
        'creator': response.context["user"].pk,
        'next_care_day': '2021-05-18'
    }

    response = client.post('/reminders/new/', data=reminder_data,
                           headers={"Content-Type": "application/html"})
    assert response.status_code == 302
    assert len(Reminder.objects.all()) == 2


@pytest.mark.django_db
def test_update_reminder(client, create_reminder):
    reminder = Reminder.objects.first()
    assert len(Reminder.objects.all()) == 1
    response = client.get(f"/reminders/edit/{reminder.pk}/")
    assert response.status_code == 200

    reminder_data = {
        'name': reminder.name,
        'plant': reminder.plant,
        'cycle': 14,
        'previous_care_day': reminder.previous_care_day,
        'creator': response.context["user"]
    }
    response = client.post(f"/reminders/edit/{reminder.pk}/",
                           data=reminder_data)
    assert response.status_code == 302
    assert len(Reminder.objects.all()) == 1
    reminder_obj = Reminder.objects.get(pk=reminder.pk)
    assert reminder_obj.cycle == reminder_data['cycle']
