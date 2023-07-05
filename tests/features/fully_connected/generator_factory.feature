Feature: A Fully Connected Generator factory
  A builder of fully-connected multi-layer perceptrons to generate images.

Scenario: The default fully-connected generator factory
  Given a default fully-connected-generator-factory
  When the input_size is checked
  And the hidden_size is checked
  And the output_size is checked
  And the block_count is checked
  And the size_multiplier is checked

  Then the input_size is the default
  And the hidden_size is the default
  And the image_size is the default
  And the block_count is the default
  And the size_multiplier is the default

Scenario: The Default Factory Builds a Block
  Given a default fully-connected-generator-factory
  When the block method is called
  Then the block output is a Sequential
  And the block output has the expected Linear layer
  And the block output has the expected Normalization Layer
  And the block output has the expected activation layer
