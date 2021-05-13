import pytest
from django.core import mail

from plantswap.models import Transaction, Message


@pytest.mark.django_db
def test_object_str_method_is_plant_name_and_care_name(create_transaction):
    transaction = Transaction.objects.first()
    expected_object_name = f'Transaction between: {transaction.to_user.username}' \
                           f' and {transaction.from_user.username}'
    assert str(transaction) == expected_object_name


@pytest.mark.django_db
def test_get_absolute_url(create_transaction):
    transaction = Transaction.objects.first()
    expected_url = f'/transactions/detail/{transaction.pk}/'
    assert transaction.get_absolute_url() == expected_url


@pytest.mark.django_db
def test_add_message_to_transaction(client, create_transaction, mailoutbox):
    assert Transaction.objects.count() == 2
    transaction = Transaction.objects.first()
    assert transaction.message.count() == 0
    message_data = {
        'plant': transaction.plant.pk,
        'from_user': transaction.from_user.pk,
        'to_user': transaction.to_user.pk,
        'content': 'test_message'
    }
    url = f'/transactions/message/{transaction.pk}/'
    response = client.post(url, data=message_data)
    assert response.status_code == 302
    assert transaction.message.filter(content='test_message').exists()
    assert Message.objects.count() == 1

    # mail.send_mail(f'Zainteresowanie rośliną: {transaction.plant.name}',
    #                f'{message_data["content"]}',
    #                'planthood.mokotow@gmail.com',
    #                ['test@wp.pl'])
    # # users in db dont have emails - in mailTo should be
    # # [transaction.to_user.email]
    # assert len(mailoutbox) == 1
    # m = mailoutbox[0]
    # assert m.subject == f'Zainteresowanie rośliną: {transaction.plant.name}'
    # assert m.body == 'test_message'
    # assert m.from_email == 'planthood.mokotow@gmail.com'
    # assert list(m.to) == ['test@wp.pl']
