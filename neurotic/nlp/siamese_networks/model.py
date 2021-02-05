# python
from collections import namedtuple

# pypi
from trax import layers
from trax.fastmath import numpy as fastmath_numpy

import attr
import numpy
import trax

Axis = namedtuple("Axis", ["columns", "last"])
Constants = namedtuple("Constants", ["model_depth", "axis"])

AXIS = Axis(1, -1)

CONSTANTS = Constants(128, AXIS)


@attr.s(auto_attribs=True)
class SiameseModel:
    """The Siamese network model

    Args:
     vocabulary_size: number of tokens in the vocabulary
     model_depth: depth of our embedding layer
     mode: train|eval|predict
    """
    vocabulary_size: int
    model_depth: int=CONSTANTS.model_depth
    mode: str="train"
    _processor: trax.layers.combinators.Serial=None
    _model: trax.layers.combinators.Parallel=None

    def normalize(self, x: numpy.ndarray) -> numpy.ndarray:
        """Normalizes the vectors to have L2 norm 1
    
        Args:
         x: the array of vectors to normalize
    
        Returns:
         normalized version of x
        """
        return x/fastmath_numpy.sqrt(fastmath_numpy.sum(x**2,
                                                        axis=CONSTANTS.axis.last,
                                                        keepdims=True))

    @property
    def processor(self) -> trax.layers.Serial:
        """The Question Processor"""
        if self._processor is None:
            self._processor = layers.Serial(
                layers.Embedding(self.vocabulary_size, self.model_depth),
                layers.LSTM(self.model_depth),
                layers.Mean(axis=CONSTANTS.axis.columns),
                layers.Fn("Normalize", self.normalize) 
            ) 
        return self._processor

    @property
    def model(self) -> trax.layers.Parallel:
        """The Siamese Model"""
        if self._model is None:
            self._model = layers.Parallel(self.processor, self.processor)
        return self._model
