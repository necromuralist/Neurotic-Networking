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
  And the block output has three layers
  And the block output has the expected Linear layer
  And the block output has the expected Normalization Layer
  And the block output has the expected activation layer

Scenario: The Default Factory Builds the Blocks
  Given a default fully-connected-generator-factory
  When the blocks property is checked
  Then the blocks are a Sequential
  And the blocks have the right number of layers
  And all but the last two blocks layers match the block call
  And the second to the last blocks layer is a linear layer
  And the blocks linear layer has the right input and output dimensions
  And the last blocks layer is a sigmoid

Scenario: The Factory Builds With No Generator Blocks
  Given a fully-connected-generator-factory with no block_count
  When the blocks property is checked
  Then the blocks have the right number of layers
  And the second to the last blocks layer is a linear layer
  And the blocks linear layer has the right input and output dimensions
  And the last blocks layer is a sigmoid

Scenario: The Factory Builds With Arbitrary Generator Blocks
  Given a fully-connected-generator-factory with an arbitrary block_count
  When the blocks property is checked
  Then the blocks have the right number of layers
  And the second to the last blocks layer is a linear layer
  And the blocks linear layer has the right input and output dimensions
  And the last blocks layer is a sigmoid

Scenario: The Factory Builds with Arbitrary Size Multiplier
  Given a fully-connected-generator-factory with an arbitrary size_multiplier
  When the blocks property is checked
  Then the blocks have the right number of layers
  And the second to the last blocks layer is a linear layer
  And the blocks linear layer has the right input and output dimensions
  And the last blocks layer is a sigmoid
