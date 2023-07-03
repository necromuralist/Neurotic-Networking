"""A Fully Connected Generator factory feature tests."""

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)


@scenario("fully_connected/generator_factory.feature", "The default fully-connected generator factory")
def test_the_default_fullyconnected_generator_factory():
    """The default fully-connected generator factory."""


@given('a default fully-connected-generator-factory')
def _():
    """a default fully-connected-generator-factory."""
    raise NotImplementedError


@when('the input_size is checked')
def _():
    """the input_size is checked."""
    raise NotImplementedError


@then('the input_size is the default')
def _():
    """the input_size is the default."""
    raise NotImplementedError
