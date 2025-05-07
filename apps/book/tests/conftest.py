# py
# django
# third
import pytest
# own
from apps.book.tests.factories import AuthorFactory, AuthorTwoFactory, ReservationFactory

@pytest.fixture
def common_author_creation_from_conftest():
    # return AuthorFactory() # crea la instancea.
    return AuthorFactory.build() # build() -> crea la instance y no la guarda (no tendra id).

@pytest.fixture
def common_author_two_creation_from_conftest():
    # 'factory.django.DjangoModelFactory' -> con esta herencia a el factory se puede acceder a funcionalidad del ORM.
    return AuthorTwoFactory.create() # crea la instance y si la guarda (si tendra id).

@pytest.fixture
def common_reservation_creation_from_conftest():
    return ReservationFactory.build()