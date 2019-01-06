Feature: A Neural Network with One Hidden Layer

Scenario: The Network is created
  Given a set of valid parameters
  When the network is created
  Then it has the expected values

Scenario: The input to hidden weights are retrieved
  Given a set of valid parameters
  When the network is created
  And the input to hidden weights are retrieved
  Then they are have the correct shape

Scenario: The input to hidden weights are set
  Given a set of valid parameters
  When the network is created
  And the input to hidden weights are set
  Then they are the correct values

Scenario: The hidden to output weights are retrieved
  Given a set of valid parameters
  When the network is created
  And the hidden to output weights are retrieved
  Then they are have the correct shape

Scenario: The hidden to output weights are set
  Given a set of valid parameters
  When the network is created
  And the hidden to output weights are set
  Then they are the correct values

Scenario: The activation function is called
  Given a set of valid parameters
  When the network is created
  And the activation function is called
  Then it calls the sigmoid function

Scenario: The sigmoid function is called
  Given a set of valid parameters
  When the network is created
  And the sigmoid function is called
  Then it returns the expected values
