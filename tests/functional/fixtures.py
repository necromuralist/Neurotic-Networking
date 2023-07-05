# from pypi
import pytest

class Katamari:
    """Something to stick values into"""

@pytest.fixture
def katamari():
    return Katamari()
