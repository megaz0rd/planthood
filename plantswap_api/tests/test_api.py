import pytest


@pytest.mark.django_db
def test_non_authorized_request(api_client):
    response = api_client.get('/api/plants/')
    assert response.status_code == 403
