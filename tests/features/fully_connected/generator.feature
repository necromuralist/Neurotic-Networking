Feature: A Fully Connected Generator
  A fully-connected multilayer perceptron to generate images

Scenario: The fully connected generator is built
  Given a fully connected generator
  When the generator is checked
  Then it is a nn Module

Scenario: The generator's forward method is called
  Given a fully connected generator
  When the generator's forward method is called
  Then it passes the input to its network
  And it returns the output of the network
