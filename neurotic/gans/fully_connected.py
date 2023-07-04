# python
from dataclasses import dataclass


@dataclass
class GeneratorDefault:
    """Default values for the generator"""
    input_size: int=10
    hidden_layer_size: int=128


class GeneratorFactory:
    """Builder of fully-connected generators

    Args:

     input_size: length for the input noise-vector
     hidden_layer_size: length of output for first layer
    """
    def __init__(self, input_size=GeneratorDefault.input_size,
                 hidden_layer_size=GeneratorDefault.hidden_layer_size):
        self.input_size = input_size
        self.hidden_layer_size = hidden_layer_size
        return
