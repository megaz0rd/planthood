from members.models import UserProfile, User


def test_new_user(django_user_model):
    django_user_model.objects.create(username='foo', password='bar')
    assert len(User.objects.all()) == 1


def test_an_admin_view(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200


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


def test_profile_views_with_authenticated_client(client):
    """Tests that a logged in user can access user profile views"""

    user = User.objects.create(username='foo', password='bar')
    UserProfile.objects.create(user=user, street='street', building_number=4)
    client.force_login(user)

    response = client.get('/accounts/address/')
    assert response.status_code == 200
    response = client.get('/accounts/password/')
    assert response.status_code == 200
    response = client.get('/accounts/edit_profile/')
    assert response.status_code == 200
