# third
import pytest
from faker import Faker
from faker.providers import BaseProvider
# own
from apps.user.models import User

# ---------------------------Faker---------------------------
# instance de faker.
fake = Faker()

# custom fake (provider).
class EmailProvider(BaseProvider):
    def custom_email(self):
        return f'{fake.user_name()}@gmail.com'
fake.add_provider(EmailProvider)

@pytest.fixture
def common_user_creation_with_faker():
    # 'pytest -rP' -> para que muestre los prints en console solo de Passed.
    # 'pytest -rA' -> para que muestre los prints en console de todos All.
    # print(f'username -> "{fake.user_name()}".')
    # print(f'email -> "{fake.email()}".')
    # print(f'custom_email -> "{fake.custom_email()}".')
    # print(f'name -> "{fake.name()}".')
    # print(f'lastname -> "{fake.last_name()}".')
    # print(f'password -> "{fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)}".')
    return User(
        username=fake.user_name(),
        email=fake.email(),
        name=fake.name(),
        lastname=fake.last_name(),
        # password=fake.password()
        password=fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
    )

@pytest.mark.django_db
def test_user_creation_with_fixture_with_faker(common_user_creation_with_faker): # para usar fixture.
    common_user_creation_with_faker.save()
    assert common_user_creation_with_faker.is_active

@pytest.mark.django_db
def test_superuser_creation_with_fixture_with_faker(common_user_creation_with_faker):
    common_user_creation_with_faker.is_staff = True
    common_user_creation_with_faker.is_superuser = True
    common_user_creation_with_faker.save()
    assert common_user_creation_with_faker.is_staff and common_user_creation_with_faker.is_superuser

@pytest.mark.django_db
def test_user_creation_fail_with_fixture_with_faker(common_user_creation_with_faker):
    delattr(common_user_creation_with_faker,'username')
    delattr(common_user_creation_with_faker,'email')
    delattr(common_user_creation_with_faker,'name')
    delattr(common_user_creation_with_faker,'lastname')
    with pytest.raises(Exception): # para manejar los errors con raises.
        common_user_creation_with_faker.save()

# 'pytest -rP' -> para que muestre los prints en console solo de Passed.
# 'pytest -rA' -> para que muestre los prints en console de todos All.

# | Código | Significado                         | ¿Qué muestra?                                                       |
# | ------ | ----------------------------------- | ------------------------------------------------------------------- |
# | `P`    | Passed                              | Muestra `print()` de pruebas que pasaron                            |
# | `F`    | Failed                              | Muestra `print()` de pruebas que fallaron                           |
# | `E`    | Error                               | Muestra errores que ocurrieron fuera del test (ej. fixture fallida) |
# | `X`    | Skipped (por condición)             | Muestra razones por las que se saltó                                |
# | `s`    | Setup failed                        | Errores durante el setup                                            |
# | `x`    | XFailed (esperadamente fallada)     | Muestra info de pruebas que fallaron "esperadamente"                |
# | `Xf`   | XPassed (esperaba fallo, pero pasó) | Pruebas que no deberían haber pasado                                |
# | `A`    | **All**                             | Muestra todo lo anterior                                            |