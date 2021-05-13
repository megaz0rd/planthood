import json

import pytest

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
def test_add_message_to_transaction(client, create_transaction):
    assert Transaction.objects.count() == 2
    transaction = Transaction.objects.first()
    assert transaction.message.count() == 0
    message_data = {
        'plant': transaction.plant,
        'from_user': transaction.from_user,
        'to_user': transaction.to_user,
        'content': 'test_message'
    }
    url = f'/transactions/message/{transaction.pk}/'
    response = client.post(url, data=message_data)
    assert response.status_code == 200
    assert transaction.message.count() == 1
