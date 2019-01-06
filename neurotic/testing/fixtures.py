import pytest

class Katamari:
    """A holder of things"""


@pytest.fixture
def katamari():
    """fixture to generate a Katamari object"""
    return Katamari()
