# from pypi
import pytest

# software under test
from neurotic.nlp.twitter.processor import TwitterProcessor

class Katamari:
    """Something to stick values into"""

@pytest.fixture
def katamari():
    return Katamari()


@pytest.fixture
def processor():
    return TwitterProcessor()
