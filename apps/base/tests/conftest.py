# third
import pytest
from ddf import G
# own
from apps.book.models import Author

# conftest -> para crear los fixture globals ya que el conftest es el firt file que se execute de las tests.

# ---------------------------django dynamic fixture from conftest---------------------------
@pytest.fixture
def common_author_creation_from_conftest():
    return G(Author)