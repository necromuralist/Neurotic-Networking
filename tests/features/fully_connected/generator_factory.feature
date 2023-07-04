Feature: A Fully Connected Generator factory
  A builder of fully-connected multi-layer perceptrons to generate images.

Scenario: The default fully-connected generator factory
  Given a default fully-connected-generator-factory
  When the input_size is checked
  And the hidden_size is checked
  Then the input_size is the default
  And the hidden_size is the default
