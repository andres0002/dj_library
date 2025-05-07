# py
# unittest -> modulo nativo de python.
from unittest import TestCase as py_TestCase # permite agrupar varias funciones, no accede directamente a la DB.
# django
# TestCase -> subclass -> si accede a la DB por cada función que tenga esta class, de forma aislada para evitar errores y que se interrunpan las demas funciones.
from django.test import TestCase as dj_TestCase
# third
# own
from apps.book.models import Author
from apps.book.tests.factories import AuthorFactory

# Create your tests here.

class AuthorTestCase(dj_TestCase): # use DB.
    # setUp(self) -> para establcer las data inicial como el method __init__.
    def setUp(self):
        # print('from -> setUp.')
        self.author = Author.objects.create( # use DB
            name = 'name string',
            lastname = 'lastname string',
            nationality = 'nationality string',
            description = 'description string'
        )

    def test_author_creation(self):
        # print('from -> test_author_creation.')
        # print(f'is_active -> {self.author.is_active}')
        assert self.author.is_active

# use factory boy
class AuthorWithFactoryBoyTestCase(py_TestCase): # no use DB.
    # setUp(self) -> para establcer las data inicial como el method __init__.
    def setUp(self):
        # print('from -> setUp Factory Boy.')
        self.author = AuthorFactory.build() # build() -> no usa DB.

    def test_author_creation(self):
        # print('from -> test_author_creation Factory Boy.')
        # print(f'is_active -> {self.author.is_active}')
        assert self.author.is_active

# command -> para execute tests -> 'python manage.py test'