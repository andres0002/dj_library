# py
# django
# third
import factory
from faker import Faker
# own
from apps.user.models import User
from apps.book.models import Author, Book, Reservation

fake = Faker()

# Factory boy -> es una herramienta para crear fixtures reutilizables de manera programática.

class AuthorFactory(factory.Factory): # basic
    class Meta:
        model = Author
    
    name=fake.name()

class AuthorTwoFactory(factory.django.DjangoModelFactory): # para poder accedar a funcionalidades de django y orm.
    class Meta:
        model = Author
    
    name=fake.name()

# uso de subfactory (required una class factory example -> ClassFactory) en foreign keys.
class BookFactory(factory.Factory):
    class Meta:
        model=Book
    
    title=fake.name()

class UserFactory(factory.Factory):
    class Meta:
        model=User
    
    name=fake.name()

class ReservationFactory(factory.Factory):
    class Meta:
        model=Reservation
    
    book=factory.SubFactory(BookFactory) # para Foreign Keys.
    user=factory.SubFactory(UserFactory) # para Foreign Keys.
    amount_days=7