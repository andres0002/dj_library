# py
# django
# third
import pytest
# own
from apps.user.tests.factories import UserFactory

@pytest.fixture
def common_user_creation_from_conftest():
    return UserFactory()