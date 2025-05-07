# py
# django
# third
import pytest
# own
from apps.user.tests.conftest import common_user_creation_from_conftest

@pytest.mark.django_db
def test_user_creation_with_factory_boy(common_user_creation_from_conftest):
    common_user_creation_from_conftest.save()
    print(f'username -> {common_user_creation_from_conftest.username}')
    assert common_user_creation_from_conftest.is_active