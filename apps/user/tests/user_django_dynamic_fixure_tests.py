# third
import pytest
# G -> para crear una instance del model indicado.
# N -> para crear una instance del model indicado, para casos donde no se quiera tocar la DB, solo crea la instancia y ya, se omite el '.save()'.
from ddf import G, N
# own
from apps.user.models import User

# ---------------------------django dynamic fixture G---------------------------
@pytest.fixture
def common_user_creation_with_G():
    return G(User)

@pytest.mark.django_db
def test_user_creation_with_django_dynamic_fixture_with_G(common_user_creation_with_G): # para usar fixture.
    common_user_creation_with_G.username = 'username'
    common_user_creation_with_G.save()
    assert common_user_creation_with_G.is_active and common_user_creation_with_G.username == 'username'

@pytest.mark.django_db
def test_superuser_creation_with_django_dynamic_fixture_with_G(common_user_creation_with_G):
    common_user_creation_with_G.is_staff = True
    common_user_creation_with_G.is_superuser = True
    common_user_creation_with_G.save()
    assert common_user_creation_with_G.is_staff and common_user_creation_with_G.is_superuser

@pytest.mark.django_db
def test_user_creation_fail_with_django_dynamic_fixture_with_G(common_user_creation_with_G):
    common_user_creation_with_G.username = None
    with pytest.raises(Exception): # para manejar los errors con raises.
        # print(common_user_creation_with_G.username)
        common_user_creation_with_G.full_clean()

# ---------------------------django dynamic fixture N---------------------------
@pytest.fixture
def common_user_creation_with_N():
    return N(User)

def test_user_creation_with_django_dynamic_fixture_with_N(common_user_creation_with_N): # para usar fixture.
    common_user_creation_with_N.username = 'username'
    assert common_user_creation_with_N.is_active and common_user_creation_with_N.username == 'username'

def test_superuser_creation_with_django_dynamic_fixture_with_N(common_user_creation_with_N):
    common_user_creation_with_N.is_staff = True
    common_user_creation_with_N.is_superuser = True
    assert common_user_creation_with_N.is_staff and common_user_creation_with_N.is_superuser

def test_user_creation_fail_with_django_dynamic_fixture_with_N(common_user_creation_with_N):
    common_user_creation_with_N.username = None
    with pytest.raises(Exception): # para manejar los errors con raises.
        # print(common_user_creation_with_N.username)
        common_user_creation_with_N.full_clean()

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