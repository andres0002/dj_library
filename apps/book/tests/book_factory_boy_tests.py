# py
# django
# third
import pytest
# own
from apps.book.tests.conftest import common_author_creation_from_conftest, common_author_two_creation_from_conftest, common_reservation_creation_from_conftest

@pytest.mark.django_db
def test_author_creation_with_factory_boy(common_author_creation_from_conftest):
    common_author_creation_from_conftest.save()
    print(f'name author -> {common_author_creation_from_conftest.name}')
    assert common_author_creation_from_conftest.is_active

@pytest.mark.django_db
def test_author_two_creation_with_factory_boy(common_author_two_creation_from_conftest):
    common_author_two_creation_from_conftest.save()
    print(f'name author two -> {common_author_two_creation_from_conftest.name}')
    assert common_author_two_creation_from_conftest.is_active

@pytest.mark.django_db
def test_reservation_creation_with_factory_boy(common_reservation_creation_from_conftest):
    # common_reservation_creation_from_conftest.save()
    print(f'amount days -> {common_reservation_creation_from_conftest.amount_days}')
    print(f'book -> {common_reservation_creation_from_conftest.book.title}')
    print(f'user -> {common_reservation_creation_from_conftest.user.name}')
    assert common_reservation_creation_from_conftest.status