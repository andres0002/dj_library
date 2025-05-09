# third
import pytest
# F -> para crear una instance del model indicado, pero que contengan Foreign Key, SI requiere de DB por eso se usa el G y no el N(que no requiere de DB).
from ddf import G, F
# own
from apps.user.models import User
from apps.book.models import Author, Book, Reservation

# ---------------------------django dynamic fixture F Foreign Key---------------------------
@pytest.fixture
def common_reservation_creation_with_F():
    book = G(Book)
    user = G(User)
    # return G(Reservation, book=F(title='book 1'), user=F(username='username')) # para hacer referencia a las Foreign Key. -> forma 1 with F.
    return G(Reservation, book=book, user=user) # para hacer referencia a las Foreign Key. -> forma 2 sin F.

@pytest.mark.django_db
def test_reservation_creation_with_django_dynamic_fixture_with_F(common_reservation_creation_with_F): # para usar fixture.
    common_reservation_creation_with_F.save()
    assert common_reservation_creation_with_F.book and common_reservation_creation_with_F.user

@pytest.mark.django_db
def test_reservation_creation_fail_with_django_dynamic_fixture_with_F(common_reservation_creation_with_F):
    common_reservation_creation_with_F.user = None
    with pytest.raises(Exception): # para manejar los errors con raises.
        # print(common_reservation_creation_with_F.user)
        common_reservation_creation_with_F.full_clean()

# ---------------------------django dynamic fixture F ManyToMany---------------------------
@pytest.fixture
def common_book_creation():
    # return G(Book, authors=2) # forma uno sin F.
    author = G(Author)
    return G(Book, authors=[F(name='Author 1'), F(name='Author 2'), author]) # forma dos with F.

# @pytest.mark.django_db
# def test_book_creation_with_django_dynamic_fixture(common_book_creation): # para usar fixture.
#     common_book_creation.save()
#     # print(common_book_creation.authors.all())
#     assert common_book_creation.title

# @pytest.mark.django_db
# def test_book_creation_fail_with_django_dynamic_fixture(common_book_creation):
#     common_book_creation.title = None
#     with pytest.raises(Exception): # para manejar los errors con raises.
#         # print(common_book_creation.user)
#         common_book_creation.full_clean()

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