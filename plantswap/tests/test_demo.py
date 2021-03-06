import pytest
from django.core import mail
from django.contrib.auth.models import User

from plantswap.models import Plant, Reminder, Transaction

from plantswap_api.utils import today


@pytest.mark.django_db
def test_new_user(create_user):
    create_user()
    assert len(User.objects.all()) == 1


@pytest.mark.django_db
def test_an_admin_view(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_prepopulated_db(set_up):
    assert len(User.objects.all()) == 50
    assert len(Plant.objects.all()) == 50
    assert len(Reminder.objects.all()) == 50
    assert len(Transaction.objects.all()) == 50


@pytest.mark.django_db
def test_send_reminder(mailoutbox, set_up):
    recipients = []

    for reminder in Reminder.objects.all():
        if reminder.next_care_day == today:
            recipient = reminder.creator.email
            if recipient not in recipients:
                recipients.append(reminder.creator.email)

    if recipients:
        mail.send_mail('reminder', 'content', 'planthood.mokotow@gmail.com',
                       recipients)
        assert len(mailoutbox) == 1
        m = mailoutbox[0]
        assert m.subject == 'reminder'
        assert m.body == 'content'
        assert m.from_email == 'planthood.mokotow@gmail.com'
        assert list(m.to) == recipients
