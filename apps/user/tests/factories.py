# py
# django
# third
import factory
from faker import Faker
# own
from apps.user.models import User

fake = Faker()

# Factory boy -> es una herramienta para crear fixtures reutilizables de manera programática.

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    username=fake.user_name()

class SuperUserFactory(factory.Factory):
    class Meta:
        model = User
    
    username=fake.user_name()
    is_staff=True
    is_superuser=True