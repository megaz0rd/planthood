from members.models import User
from plantswap.models import Transaction
from plantswap.tests.utils import (
    random_plant,
    random_reminder,
    random_transaction
)


def test_plant_views_with_non_authenticated_client(client, set_up):
    """Tests that a non-logged in user is redirected"""

    response = client.get('/plants/')
    assert response.status_code == 302
    response = client.get(f'/plants/edit/{random_plant().pk}/')
    assert response.status_code == 302
    response = client.get(f'/plants/detail/{random_plant().pk}/')
    assert response.status_code == 302
    response = client.get('/plants/new/')
    assert response.status_code == 302
    response = client.get(f'/add-to-transaction/{random_plant().pk}')
    assert response.status_code == 301
    redirect = client.get(response.url)
    assert redirect.status_code == 302


def test_reminder_views_with_non_authenticated_client(client, set_up):
    """Tests that a non-logged in user is redirected"""

    response = client.get('/reminders/')
    assert response.status_code == 302
    response = client.get('/reminders/new/')
    assert response.status_code == 302
    response = client.get(f'/reminders/edit/{random_reminder().pk}/')
    assert response.status_code == 302
    response = client.get(f'/reminders/confirm/{random_reminder().pk}/')
    assert response.status_code == 302
    response = client.get(f'/reminders/delete/{random_reminder().pk}/')
    assert response.status_code == 302


def test_transaction_views_with_non_authenticated_client(client, set_up):
    """Tests that a non-logged in user is redirected"""

    response = client.get('/transactions/')
    assert response.status_code == 302
    response = client.get(
        f'/transactions/detail/{random_transaction().pk}/')
    assert response.status_code == 302
    response = client.get(
        f'/transactions/message/{random_transaction().pk}/')
    assert response.status_code == 302
    response = client.get(
        f'/transactions/finalize/{random_transaction().pk}/')
    assert response.status_code == 302
    response = client.get(
        f'/transactions/delete/{random_transaction().pk}/')
    assert response.status_code == 302


def test_profile_views_with_non_authenticated_client(client):
    """Tests that a non-logged in user is redirected"""

    response = client.get('/accounts/address/')
    assert response.status_code == 302
    response = client.get('/accounts/password/')
    assert response.status_code == 302
    response = client.get('/accounts/edit_profile/')
    assert response.status_code == 302


def test_plant_views_with_authenticated_client(client, set_up):
    """Tests that a logged in user can views plants"""

    plant = random_plant()
    user = plant.owner
    client.force_login(user)
    response = client.get('/plants/')
    assert response.status_code == 200
    response = client.get('/plants/new/')
    assert response.status_code == 200

    if plant.status == 4:
        # User is forbidden to see plant that user owns no more
        response = client.get(f'/plants/detail/{plant.pk}/')
        assert response.status_code == 403
        response = client.get(f'/plants/edit/{plant.pk}/')
        assert response.status_code == 403
    else:
        # User can access to edit form or detail page of user's own plant
        response = client.get(f'/plants/edit/{plant.pk}/')
        assert response.status_code == 200
        response = client.get(f'/plants/detail/{plant.pk}/')
        assert response.status_code == 200


def test_plant_views_permissions_with_authenticated_client(client, set_up,
                                                           other_user_plant):
    """Tests a logged user's permissions to view an others' plants"""

    user = User.objects.first()
    client.force_login(user)

    # User can see details of an others' users plants if plant status is 1 or 2
    response = client.get(f"/plants/detail/{other_user_plant['plant1'].pk}/")
    assert response.status_code == 200
    response = client.get(f"/plants/detail/{other_user_plant['plant2'].pk}/")
    assert response.status_code == 200

    # User is forbidden to access form to edit an others' users plants or to see
    # details of them if a plant status is 3 or 4
    response = client.get(f"/plants/edit/{other_user_plant['plant1'].pk}/")
    assert response.status_code == 403
    response = client.get(f"/plants/edit/{other_user_plant['plant2'].pk}/")
    assert response.status_code == 403
    response = client.get(f"/plants/edit/{other_user_plant['plant3'].pk}/")
    assert response.status_code == 403
    response = client.get(f"/plants/edit/{other_user_plant['plant4'].pk}/")
    assert response.status_code == 403
    response = client.get(f"/plants/detail/{other_user_plant['plant3'].pk}/")
    assert response.status_code == 403
    response = client.get(f"/plants/detail/{other_user_plant['plant4'].pk}/")
    assert response.status_code == 403


def test_add_plant_to_transaction_view_with_authenticated_client(client,
                                                                 set_up,
                                                                 other_user_plant):
    """Tests that a logged in user can add an other plant to transaction"""

    user = User.objects.first()
    client.force_login(user)

    response = client.get(f"/add-to-transaction/"
                          f"{other_user_plant['plant1'].pk}")
    assert response.status_code == 301
    redirect = client.get(response.url)
    assert redirect.status_code == 302

    # Get a recently created transaction
    transaction_query = Transaction.objects.filter(
        plant=other_user_plant['plant1'])
    assert redirect.url == f'/transactions/message/{transaction_query[0].pk}/'
    # Check if user can create message to transaction
    response = client.post(redirect.url)
    assert response.status_code == 200


def test_reminder_views_with_authenticated_client(client, set_up):
    """Tests that a logged in user can views reminders"""
    reminder = random_reminder()
    user = reminder.creator
    client.force_login(user)

    response = client.get('/reminders/')
    assert response.status_code == 200
    response = client.get('/reminders/new/')
    assert response.status_code == 200
    response = client.get(f'/reminders/edit/{reminder.pk}/')
    assert response.status_code == 200
    response = client.get(f'/reminders/confirm/{reminder.pk}/')
    assert response.status_code == 200
    response = client.get(f'/reminders/delete/{reminder.pk}/')
    assert response.status_code == 200

    while reminder.creator == user:
        # Change reminder to see if user can see reminder set by an other user
        reminder = random_reminder()

    response = client.get(f'/reminders/edit/{reminder.pk}/')
    assert response.status_code == 403
    response = client.get(f'/reminders/confirm/{reminder.pk}/')
    assert response.status_code == 403
    response = client.get(f'/reminders/delete/{reminder.pk}/')
    assert response.status_code == 403
