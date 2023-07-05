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

from ..fixtures import katamari

and_when = when
And = then

# the software under test
from neurotic.gans.fully_connected import (GeneratorDefault,
                                           GeneratorFactory)

scenarios("fully_connected/generator_factory.feature")

#* Scenario: The default fully-connected generator factory *#

@given("a default fully-connected-generator-factory",
       target_fixture="factory")
def _():
    return GeneratorFactory()


@when("the input_size is checked", target_fixture="input_size")
def _(factory):
    return factory.input_size


@and_when("the hidden_size is checked", target_fixture="hidden_size")
def _(factory):
    return factory.hidden_layer_size


@and_when("the output_size is checked", target_fixture="output_size")
def _(factory):
    return factory.output_size


@and_when("the block_count is checked", target_fixture="block_count")
def _(factory):
    return factory.block_count


@and_when("the size_multiplier is checked", target_fixture="size_multiplier")
def _(factory):
    return factory.size_multiplier


@then('the input_size is the default')
def _(input_size):
    expect(input_size).to(equal(GeneratorDefault.input_size))
    return


@then("the hidden_size is the default")
def _(hidden_size):
    expect(hidden_size).to(equal(GeneratorDefault.hidden_layer_size))


@then("the image_size is the default")
def _(output_size):
    expect(output_size).to(equal(GeneratorDefault.output_size))


@then("the block_count is the default")
def _(block_count):
    expect(block_count).to(equal(GeneratorDefault.block_count))


@then("the size_multiplier is the default")
def _(size_multiplier):
    expect(size_multiplier).to(equal(GeneratorDefault.size_multiplier))
    return

#* Scenario: The Default Factory Builds a Block *#

#**  Given a default fully-connected-generator-factory

@when("the block method is called" , target_fixture="block_output")
def _(factory, katamari):
    katamari.input_size = 20
    katamari.output_size = 32
    return factory.block(input_size=katamari.input_size, output_size=katamari.output_size)


@then("the block output is a Sequential")
def _(block_output):
    return

@And("the block output has the expected Linear layer")
def _():
    return


@And("the block output has the expected Normalization Layer")
def _():
    return


@And("the block output has the expected activation layer")
def _():
    return
