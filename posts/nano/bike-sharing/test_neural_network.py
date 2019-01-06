# coding=utf-8
"""A Neural Network with One Hidden Layer feature tests."""
# python standard library
from functools import partial
from random import (
    random,
    randint,
    randrange
)

# from pypi
from expects import (
    be_true,
    equal,
    expect,
)
from pytest_bdd import (
    given,
    then,
    when,
)

import numpy
import pytest_bdd

# this project
from neurotic.testing.fixtures import katamari

# software under test
from my_answers import NeuralNetwork

scenario = partial(pytest_bdd.scenario, 'neural_network.feature')
And = when

# ******************** Constructor ******************** #
@scenario('The Network is created')
def test_the_network_is_created():
    return


@given('a set of valid parameters')
def a_set_of_valid_parameters(katamari):
    katamari.parameters = dict(
        input_nodes=randrange(1, 20),
        hidden_nodes=randrange(1, 20),
        output_nodes=1,
        learning_rate = random(),
    )
    return


@when('the network is created')
def the_network_is_created(katamari):
    katamari.network = NeuralNetwork(**katamari.parameters)
    return


@then('it has the expected values')
def it_has_the_expected_values(katamari):
    for key, value in katamari.parameters.items():
        expect(getattr(katamari.network, key)).to(equal(value))
    return

# ******************** Weights ******************** #
# ********** Input to Hidden ********** #


@scenario("The input to hidden weights are retrieved")
def test_hidden_weights():
    return

#  Given a set of valid parameters
#  When the network is created

@And("the input to hidden weights are retrieved")
def get_input_to_hidden_weights(katamari):
    katamari.actual = katamari.network.weights_input_to_hidden.shape
    katamari.expected = (katamari.parameters["input_nodes"],
                         katamari.parameters["hidden_nodes"])
    return


@then("they are have the correct shape")
def check_shape(katamari):
    expect(katamari.actual).to(equal(katamari.expected))
    return

# ***** Set ***** #


@scenario("The input to hidden weights are set")
def test_set_input_to_hidden_weights():
    return

#  Given a set of valid parameters
#  When the network is created


@And("the input to hidden weights are set")
def set_input_hidden_weights(katamari):
    katamari.expected = numpy.random.random((
        katamari.parameters["input_nodes"],
        katamari.parameters["hidden_nodes"]))
    katamari.network.weights_input_to_hidden = katamari.expected
    katamari.actual = katamari.network.weights_input_to_hidden
    return

@then("they are the correct values")
def check_array_values(katamari):
    expect(bool(
        (katamari.actual==katamari.expected).all())).to(be_true)
    return

# ********** Hidden to Output ********** #


@scenario("The hidden to output weights are retrieved")
def test_hidden_to_output_weights():
    return

#  Given a set of valid parameters
#  When the network is created


@And("the hidden to output weights are retrieved")
def get_hidden_to_output_weights(katamari):
    katamari.actual = katamari.network.weights_hidden_to_output.shape
    katamari.expected = (katamari.parameters["hidden_nodes"],
                         katamari.parameters["output_nodes"])
    return

#  Then they are have the correct shape

# ***** Set ***** #


@scenario("The hidden to output weights are set")
def test_set_hidden_to_output():
    return

#  Given a set of valid parameters
#  When the network is created


@And("the hidden to output weights are set")
def set_hidden_to_output_weights(katamari):
    katamari.expected = numpy.random.random((katamari.parameters["hidden_nodes"],
                                             katamari.parameters["output_nodes"]))
    katamari.network.weights_hidden_to_output = katamari.expected
    katamari.actual = katamari.network.weights_hidden_to_output
    return

#  Then they are the correct values

# ******************** Activation Function ******************** #


@scenario("The activation function is called")
def test_activation_function():
    return

#  Given a set of valid parameters
#  When the network is created


@And("the activation function is called")
def call_the_activation_function(katamari, mocker):
    katamari.network.sigmoid = mocker.Mock()
    katamari.expected = randint(1, 100)
    katamari.value = randint(1, 1000)
    katamari.network.sigmoid.return_value = katamari.expected
    katamari.actual = katamari.network.activation_function(katamari.value)
    return


@then("it calls the sigmoid function")
def check_sigmoid_call(katamari):
    expect(katamari.actual).to(equal(katamari.expected))
    katamari.network.sigmoid.assert_called_once_with(katamari.value)
    return

# ******************** sigmoid ******************** #


@scenario("The sigmoid function is called")
def test_sigmoid():
    return

#  Given a set of valid parameters
#  When the network is created


@And("the sigmoid function is called")
def call_sigmoid(katamari, mocker):
    katamari.inputs = numpy.random.random((3, 2))
    katamari.outputs = katamari.network.sigmoid(katamari.inputs)
    katamari.expected = numpy.exp(katamari.inputs)/(
        numpy.exp(katamari.inputs) + 1)
    return


@then("it returns the expected values")
def check_returned_values(katamari):
    expect(numpy.allclose(katamari.outputs, katamari.expected)).to(be_true)
    return
