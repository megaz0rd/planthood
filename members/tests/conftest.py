import pytest

from members.models import UserProfile
from plantswap.tests.conftest import create_user, test_password, auto_login_user


@pytest.fixture
def create_profile(db, client, auto_login_user):
    client, user = auto_login_user()
    return UserProfile.objects.create(user=user,
                                      street='street',
                                      building_number=1)


# @pytest.fixture(autouse=True)
# def enable_db_access_for_all_tests(db):
#     pass
