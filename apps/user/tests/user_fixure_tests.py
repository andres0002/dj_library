# third
import pytest
# own
from apps.user.models import User

# ---------------------------fixture---------------------------
@pytest.fixture
def common_user_creation():
    return User(
        username='username',
        email='username@gmail.com',
        name='name',
        lastname='lastname',
        password='12345'
    )

@pytest.mark.django_db
def test_user_creation_with_fixture(common_user_creation): # para usar fixture.
    common_user_creation.save()
    assert common_user_creation.is_active and common_user_creation.username == 'username'

@pytest.mark.django_db
def test_superuser_creation_with_fixture(common_user_creation):
    common_user_creation.is_staff = True
    common_user_creation.is_superuser = True
    common_user_creation.save()
    assert common_user_creation.is_staff and common_user_creation.is_superuser

@pytest.mark.django_db
def test_user_creation_fail_with_fixture(common_user_creation):
    delattr(common_user_creation,'username')
    delattr(common_user_creation,'email')
    delattr(common_user_creation,'name')
    delattr(common_user_creation,'lastname')
    with pytest.raises(Exception): # para manejar los errors con raises.
        common_user_creation.save()

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