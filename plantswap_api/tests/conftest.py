import pytest
from rest_framework.test import APIClient

from plantswap.tests.conftest import create_user, test_password


@pytest.fixture
def api_client():
    return APIClient()
