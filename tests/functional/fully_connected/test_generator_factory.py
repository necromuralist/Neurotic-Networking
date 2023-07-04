"""Fully Connected Generator factory feature tests."""
# from pypi

from expects import (
    equal,
    expect   
)
from pytest_bdd import (
    given,
    scenarios,
    then,
    when,
)

and_when = when

# the software under test
from neurotic.gans.fully_connected import (GeneratorDefault,
                                           GeneratorFactory)

scenarios("fully_connected/generator_factory.feature")

#* Scenario: The default fully-connected generator factory *#

@given("a default fully-connected-generator-factory", target_fixture="factory")
def _():
    return GeneratorFactory()

@when("the input_size is checked", target_fixture="input_size")
def _(factory):
    return factory.input_size

@and_when("the hidden_size is checked", target_fixture="hidden_size")
def _(factory):
    return factory.hidden_layer_size

@then('the input_size is the default')
def _(input_size):
    expect(input_size).to(equal(GeneratorDefault.input_size))
    return

@then("the hidden_size is the default")
def _(hidden_size):
    expect(hidden_size).to(equal(GeneratorDefault.hidden_layer_size))
