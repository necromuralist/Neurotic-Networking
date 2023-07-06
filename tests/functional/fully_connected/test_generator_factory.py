"""Fully Connected Generator factory feature tests."""
# python

import random
# from pypi

from expects import (
    be_a,
    be_true,
    equal,
    expect,
    have_length,
)

from pytest_bdd import (
    given,
    scenarios,
    then,
    when,
)

from torch import nn

# this project (testing only)
from ..fixtures import katamari


and_when = when
And = then

# the software under test
from neurotic.gans.fully_connected import (GeneratorDefault,
                                           GeneratorFactory)


class FakeSequential(nn.Module):
    """A fake module to check blocks"""


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
    katamari.input_size = random.randrange(10, 100)
    katamari.output_size = random.randrange(10, 100)
    katamari.output = factory.block(input_size=katamari.input_size,
                                    output_size=katamari.output_size)
    return katamari


@then("the block output is a Sequential")
def _(block_output):
    expect(block_output.output).to(be_a(nn.Sequential))
    return


@And("the block output has three layers")
def _(block_output):
    expect(block_output.output).to(have_length(3))
    return


@And("the block output has the expected Linear layer")
def _(block_output):
    first_layer = block_output.output[0]
    expect(first_layer).to(be_a(nn.Linear))
    expect(first_layer.in_features).to(equal(block_output.input_size))
    expect(first_layer.out_features).to(equal(block_output.output_size))
    return


@And("the block output has the expected Normalization Layer")
def _(block_output):
    second_layer = block_output.output[1]
    expect(second_layer).to(be_a(nn.BatchNorm1d))
    expect(second_layer.num_features).to(equal(block_output.output_size))
    return


@And("the block output has the expected activation layer")
def _(block_output):
    third_layer = block_output.output[2]
    expect(third_layer).to(be_a(nn.ReLU))
    expect(third_layer.inplace).to(be_true)
    return


#** Scenario: The Default Factory Builds the Blocks **#

#  Given a default fully-connected-generator-factory


@when("the blocks property is checked", target_fixture="blocks")
def _(factory, monkeypatch):
    def mock_blocks(input_size, output_size):
        return FakeSequential()
    monkeypatch.setattr(factory, "block", mock_blocks)
    return factory.blocks


@then("the blocks are a Sequential")
def _(blocks):
    expect(blocks).to(be_a(nn.Sequential))
    return


@And("the blocks have the right number of layers")
def _(blocks):
    expect(blocks).to(have_length(GeneratorDefault.block_count + 2))
    return


@And("all but the last two blocks layers match the block call")
def _(blocks):
    for layer in blocks[:-2]:
        expect(layer).to(be_a(FakeSequential))
    return


#  And the blocks have the right number of layers
#  And the second to the last blocks layer is a linear layer
#  And the blocks linear layer has the right input and output dimensions
#  And the last blocks layer is a sigmoid
#  And the output of a vector passed to it is the right shape
