import pytest

from members.models import User, UserProfile


@pytest.mark.django_db
def test_new_user(create_user):
    create_user()
    assert len(User.objects.all()) == 1


@pytest.mark.django_db
def test_an_admin_view(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_non_authenticated_views(client):
    """Tests that a non-logged in user can see main, register, login and
    reset password pages"""

    response = client.get('/')
    assert response.status_code == 200
    response = client.get('/accounts/register/')
    assert response.status_code == 200
    response = client.get('/accounts/login/')
    assert response.status_code == 200
    response = client.get('/accounts/password_reset/')
    assert response.status_code == 200
    response = client.get('/accounts/password_reset/done/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_views_with_non_authenticated_client(client):
    """Tests that a non-logged in user is redirected"""

    response = client.get('/accounts/address/')
    assert response.status_code == 302
    response = client.get('/accounts/password/')
    assert response.status_code == 302
    response = client.get('/accounts/edit_profile/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_profile_views_with_authenticated_client(client, create_profile):
    """Tests that a logged in user can access user profile views"""

    assert len(UserProfile.objects.all()) == 1
    response = client.get('/accounts/address/')
    assert response.status_code == 200
    response = client.get('/accounts/password/')
    assert response.status_code == 200
    response = client.get('/accounts/edit_profile/')
    assert response.status_code == 200
