"""Fully Connected Generator factory feature tests."""
# python

import math
import random
# from pypi

from expects import (
    be,
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
                                           GeneratorFactory,
                                           FullyConnectedGenerator)


class FakeSequential(nn.Module):
    """A fake module to check blocks"""


scenarios("fully_connected/generator_factory.feature")

#* Scenario: The default fully-connected generator factory *#

@given("a default fully-connected-generator-factory",
       target_fixture="test_thing")
def _(katamari):
    katamari.factory =  GeneratorFactory()
    return katamari


@when("the input_size is checked", target_fixture="input_size")
def _(test_thing):
    return test_thing.factory.input_size


@and_when("the hidden_size is checked", target_fixture="hidden_size")
def _(test_thing):
    return test_thing.factory.hidden_layer_size


@and_when("the output_size is checked", target_fixture="output_size")
def _(test_thing):
    return test_thing.factory.output_size


@and_when("the block_count is checked", target_fixture="block_count")
def _(test_thing):
    return test_thing.factory.block_count


@and_when("the size_multiplier is checked", target_fixture="size_multiplier")
def _(test_thing):
    return test_thing.factory.size_multiplier


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

@when("the block method is called", target_fixture="block_output" )
def _(test_thing):
    test_thing.input_size = random.randrange(10, 100)
    test_thing.output_size = random.randrange(10, 100)
    return test_thing.factory.block(input_size=test_thing.input_size,
                                    output_size=test_thing.output_size)


@then("the block output is a Sequential")
def _(block_output):
    expect(block_output).to(be_a(nn.Sequential))
    return


@And("the block output has three layers")
def _(block_output):
    expect(block_output).to(have_length(3))
    return


@And("the block output has the expected Linear layer")
def _(block_output, test_thing):
    first_layer = block_output[0]
    expect(first_layer).to(be_a(nn.Linear))
    expect(first_layer.in_features).to(equal(test_thing.input_size))
    expect(first_layer.out_features).to(equal(test_thing.output_size))
    return


@And("the block output has the expected Normalization Layer")
def _(block_output, test_thing):
    second_layer = block_output[1]
    expect(second_layer).to(be_a(nn.BatchNorm1d))
    expect(second_layer.num_features).to(equal(test_thing.output_size))
    return


@And("the block output has the expected activation layer")
def _(block_output):
    third_layer = block_output[2]
    expect(third_layer).to(be_a(nn.ReLU))
    expect(third_layer.inplace).to(be_true)
    return


#** Scenario: The Default Factory Builds the Blocks **#

#  Given a default fully-connected-generator-factory


@when("the blocks property is checked", target_fixture="blocks")
def _(test_thing, monkeypatch):
    def mock_blocks(input_size, output_size):
        return FakeSequential()
    monkeypatch.setattr(test_thing.factory, "block", mock_blocks)
    return test_thing.factory.blocks


@then("the blocks are a Sequential")
def _(blocks):
    expect(blocks).to(be_a(nn.Sequential))
    return


@And("the blocks have the right number of layers")
def _(blocks, test_thing):
    expect(blocks).to(have_length(test_thing.factory.block_count + 2))
    return


@And("all but the last two blocks layers match the block call")
def _(blocks):
    for layer in blocks[:-2]:
        expect(layer).to(be_a(FakeSequential))
    return


@And("the second to the last blocks layer is a linear layer")
def _(blocks):
    expect(blocks[-2]).to(be_a(nn.Linear))
    return


@And("the blocks linear layer has the right input and output dimensions")
def _(blocks, test_thing):
    almost_last = blocks[-2]
    expected_input_size = (math.ceil(
        test_thing.factory.size_multiplier** (test_thing.factory.block_count - 1))
        * test_thing.factory.hidden_layer_size)
    expected_output_size = test_thing.factory.output_size
    expect(almost_last.in_features).to(equal(expected_input_size))
    expect(almost_last.out_features).to(equal(expected_output_size))
    return


@And("the last blocks layer is a sigmoid")
def _(blocks):
    expect(blocks[-1]).to(be_a(nn.Sigmoid))
    return


#** Scenario: The Factory Builds With No Generator Blocks **#

@given("a fully-connected-generator-factory with no block_count",
       target_fixture="test_thing")
def _(katamari):
    katamari.factory = GeneratorFactory(block_count=0)
    return katamari

#  When the blocks property is checked
#  Then the blocks have the right number of layers
#  And the blocks linear layer has the right input and output dimensions
#  And the second to the last blocks layer is a linear layer
#  And the last blocks layer is a sigmoid

# ** Scenario: The Factory Builds With Arbitrary Generator Blocks ** #

@given("a fully-connected-generator-factory with an arbitrary block_count",
       target_fixture="test_thing")
def _(katamari):
    katamari.factory = GeneratorFactory(
        block_count=random.randrange(10)
    )
    return katamari

#  When the blocks property is checked
#  Then the blocks have the right number of layers
#  And the second to the last blocks layer is a linear layer
#  And the blocks linear layer has the right input and output dimensions
#  And the last blocks layer is a sigmoid

# ** Scenario: The Factory Builds with Arbitrary Size Multiplier ** #


@given("a fully-connected-generator-factory with an arbitrary size_multiplier",
       target_fixture="test_thing")
def _(katamari):
    katamari.factory = GeneratorFactory(size_multiplier=random.randint(2, 10))
    return katamari

#  When the blocks property is checked
#  Then the blocks have the right number of layers
#  And the second to the last blocks layer is a linear layer
#  And the blocks linear layer has the right input and output dimensions
#  And the last blocks layer is a sigmoid


# ** Scenario: The factory builds the Generator ** #

#  Given a default fully-connected-generator-factory


@when("the generator is checked", target_fixture="el_generator")
def _(test_thing):
    return test_thing.factory.generator


@then("the generator is a Fully Connected Generator")
def _(el_generator):
    expect(el_generator).to(be_a(FullyConnectedGenerator))
    return


@And("the generator has the factory's blocks")
def _(test_thing, el_generator):
    expect(el_generator.network).to(be(test_thing.factory.blocks))
    return
