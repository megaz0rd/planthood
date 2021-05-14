import pytest

from plantswap.models import Transaction, Reminder, Plant
from plantswap.tests.utils import random_reminder, random_transaction


@pytest.mark.django_db
@pytest.mark.parametrize("url, status_code", (
        ('/plants/', 302),
        ('/plants/new/', 302),
        ('/plants/edit/1/', 302),
        ('/add-to-transaction/1/', 302),
        ('/reminders/', 302),
        ('/reminders/new/', 302),
        ('/reminders/edit/1/', 302),
        ('/reminders/confirm/1/', 302),
        ('/reminders/delete/1/', 302),
        ('/transactions/', 302),
        ('/transactions/detail/1/', 302),
        ('/transactions/message/1/', 302),
        ('/transactions/finalize/1/', 302),
        ('/transactions/delete/1/', 302),
        ('/accounts/address/', 302),
        ('/accounts/password/', 302),
        ('/accounts/edit_profile/', 302),
        ('/', 200),
        ('/accounts/register/', 200),
        ('/accounts/login/', 200),
        ('/accounts/password_reset/', 200),
        ('/accounts/password_reset/done/', 200),
))
def test_get_request_with_non_authenticated_client(client, set_up,
                                                   url, status_code):
    """Tests that a non-logged in user is redirected to /accounts/login/"""
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("url, status_code", (
        ('/plants/', 200),
        ('/plants/new/', 200),
        ('/reminders/', 200),
        ('/reminders/new/', 200),
        ('/transactions/', 200),
        ('/accounts/address/', 200),
        ('/accounts/password/', 200),
        ('/accounts/edit_profile/', 200),
        ('/', 200),
))
def test_basic_views_with_authenticated_client(client, create_profile, url,
                                               status_code):
    """Tests that a logged in user can access to landing page, profile views
    and models' create form"""

    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("url, status_code", (
        ('/plants/detail/', 200),
        ('/plants/edit/', 200),
))
def test_specific_plant_with_authenticated_client(client, create_plant, url,
                                                  status_code):
    """Tests that a logged in user is allowed to see and edit an owned plant"""
    response = client.get(f'{url}{Plant.objects.get(status=3).pk}/')
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("url, status_code", (
        ('/transactions/detail/', 200),
        ('/transactions/message/', 200),
        ('/transactions/finalize/', 200),
        ('/transactions/delete/', 200)
))
def test_specific_transaction_view_with_authenticated_client(client,
                                                             create_transaction,
                                                             url,
                                                             status_code):
    """Tests that a logged in user is allowed to view transaction which user
    is a part of"""
    response = client.get(f'{url}{Transaction.objects.first().pk}/')
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("url, status_code", (
        ('/reminders/edit/', 200),
        ('/reminders/confirm/', 200),
        ('/reminders/delete/', 200)
))
def test_specific_reminder_view_with_authenticated_client(client,
                                                          create_reminder,
                                                          url,
                                                          status_code):
    """Tests that a logged in user is allowed to view reminder which user
    is a creator"""
    response = client.get(f'{url}{Reminder.objects.first().pk}/')
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("url, status_code", (
        ('/reminders/edit/', 403),
        ('/reminders/confirm/', 403),
        ('/reminders/delete/', 403)
))
def test_other_user_reminders_views_with_authenticated_client(client,
                                                              set_up,
                                                              auto_login_user,
                                                              url,
                                                              status_code):
    """Tests that a logged in user is forbidden to view a reminder which user
    is not a creator"""
    client, user = auto_login_user()
    response = client.get(f'{url}{random_reminder().pk}/')
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("url, status_code", (
        ('/transactions/detail/', 403),
        ('/transactions/message/', 403),
        ('/transactions/finalize/', 403),
        ('/transactions/delete/', 403)
))
def test_other_user_transactions_views_with_authenticated_client(client,
                                                                 set_up,
                                                                 auto_login_user,
                                                                 url,
                                                                 status_code):
    """Tests that a logged in user is forbidden to view transactions which user
    is not a part of"""
    client, user = auto_login_user()
    response = client.get(f'{url}{random_transaction().pk}/')
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("url, status_code", (
        ('/plants/detail/', 403),
        ('/plants/edit/', 403),
))
def test_other_user_plants_views_with_authenticated_client(client,
                                                           set_up,
                                                           url,
                                                           status_code):
    """Test thad user is forbidden to:
     - access form to edit the others' users plants
     - see details of the others' users plants if their status is 3 and 4"""
    response = client.get(f'{url}{Plant.objects.filter(status=3).first().pk}/')
    assert response.status_code == status_code
    response = client.get(f'{url}{Plant.objects.filter(status=4).first().pk}/')
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("url, status_code", (
        ('/plants/detail/', 403),
        ('/plants/edit/', 403),
))
def test_forbidden_plant_view_with_authenticated_client(client,
                                                        create_plant,
                                                        url,
                                                        status_code):
    """Test that a logged user is forbidden to see and edit plant that user
    was a previous owner"""
    response = client.get(f'{url}{Plant.objects.get(status=4).pk}/')
    assert response.status_code == status_code


@pytest.mark.django_db
def test_add_plant_to_transaction_view_with_authenticated_client(
        auto_login_user,
        other_user_plant):
    """Tests that a logged in user can add an available or wanted plant to
    transaction"""

    client, user = auto_login_user()

    response = client.get(f"/add-to-transaction/"
                          f"{other_user_plant['plant1'].pk}")
    assert response.status_code == 301
    redirect = client.get(response.url)
    assert redirect.status_code == 302

    # Get a recently created transaction
    transaction_query = Transaction.objects.filter(
        plant=other_user_plant['plant1'])
    assert redirect.url == f'/transactions/message/{transaction_query[0].pk}/'
