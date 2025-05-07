# third
import pytest
# own
from apps.user.models import User

@pytest.mark.django_db # para dar access a la DB.
def test_user_creation():
    user = User.objects.create_user(
        username='username',
        email='username@gmail.com',
        name='name',
        lastname='lastname',
        password='12345'
    )
    assert user.is_active and user.username == 'username' # valida si el test fue 'success' o 'error'.

@pytest.mark.django_db
def test_superuser_creation():
    user = User.objects.create_superuser(
        username='username',
        email='username@gmail.com',
        name='name',
        lastname='lastname',
        password='12345'
    )
    assert user.is_staff and user.is_superuser

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