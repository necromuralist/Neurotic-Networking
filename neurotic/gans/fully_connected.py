# python
from dataclasses import dataclass

# pypi
from torch import nn

@dataclass
class GeneratorDefault:
    """Default values for the generator"""
    input_size: int=10
    hidden_layer_size: int=128
    output_size: int=784
    block_count: int=4
    size_multiplier: int=2


class GeneratorFactory:
    """Builder of fully-connected generators

    Args:

     input_size: length for the input noise-vector
     hidden_layer_size: length of output for first layer
     output_size: the length of the output image vector
     block_count: how many linear-norm-relu blocks to give the generator
     size_multiplier: how much to multiply hidden layer by for each block
    """
    def __init__(self, input_size: int=GeneratorDefault.input_size,
                 hidden_layer_size: int=GeneratorDefault.hidden_layer_size,
                 output_size: int=GeneratorDefault.output_size,
                 block_count: int=GeneratorDefault.block_count,
                 size_multiplier: int=GeneratorDefault.size_multiplier):
        self.input_size = input_size
        self.hidden_layer_size = hidden_layer_size
        self.output_size = output_size
        self.block_count = block_count
        self.size_multiplier = size_multiplier
        self._blocks = None
        return

    def block(self, input_size: int, output_size: int) -> nn.Sequential:
        """Create a linear block for the generator
    
        Args:
         - `input_size`: vector size for the input to the linear layer
         - `output_size`: vector size for the output
    
        Returns:
         - Sequential generator block
        """
        return nn.Sequential(
            nn.Linear(input_size, output_size),
            nn.BatchNorm1d(output_size),
            nn.ReLU(inplace=True),
        )


    @property
    def blocks(self) -> nn.Sequential: 
       """Creates the network for the generator
    
    
        Returns:
         sequence of generator blocks with Linear and Sigmoid tail
        """
       if self._blocks is None:
          input_size, output_size = self.input_size, self.hidden_layer_size
          blocks = []
    
          for block in range(self.block_count):
             blocks.append(self.block(input_size, output_size))
             input_size, output_size = (output_size, output_size
                                        * self.size_multiplier)
    
    
          input_size = input_size if self.block_count else output_size
          blocks.append(nn.Linear(input_size,
                                  self.output_size))
          blocks.append(nn.Sigmoid())
          self._blocks = nn.Sequential(*blocks)
       return self._blocks
