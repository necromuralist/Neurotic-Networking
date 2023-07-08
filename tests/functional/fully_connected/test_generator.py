from expects import (
    be,
    be_a,    
    equal,
    expect
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


# testing alias
And = then

# software under test

from neurotic.gans.fully_connected import FullyConnectedGenerator


scenarios("fully_connected/generator.feature")


# ** Scenario: The fully connected generator is built ** #

@given("a fully connected generator", target_fixture="generator")
def _(mocker):
    return FullyConnectedGenerator(mocker.MagicMock(spec=nn.Sequential))


@when("the generator is checked")
def _():
    return


@then("it is a nn Module")
def _(generator):
    expect(generator).to(be_a(nn.Module))
    return


# ** Scenario: The generator's forward method is called ** #
#  Given a fully connected generator

@when("the generator's forward method is called", target_fixture="forward_output")
def _(generator, mocker, katamari):
    katamari.noise = mocker.Mock()
    katamari.expected = mocker.Mock()
    generator.network.return_value = katamari.expected
    katamari.output = generator.forward(katamari.noise)
    return katamari


@then("it passes the input to its network")
def _(generator, forward_output, mocker):
    expect(generator.network.call_args).to(equal(
        mocker.call(forward_output.noise)))
    return

@And("it returns the output of the network")
def _(forward_output):
    expect(forward_output.output).to(be(forward_output.expected))
    return
