# from pypi
from trax.fastmath import numpy as fastmath_numpy
from trax import layers

import attr
import jax
import numpy
import trax


@attr.s
class TripletLoss:
    """Calculates the triplet loss frow two batches
    """
    margin: float = 0.25
    _layer: trax.layers.base.PureLayer=None

    @property
    def layer(self) -> trax.layers.base.PureLayer:
        """The Layer for the triplet loss"""
        if self._layer is None:
            self._layer = layers.Fn("TripletLoss", self.__call__)
        return self._layer

    def __call__(self, v1: numpy.ndarray,
                 v2: numpy.ndarray)-> jax.interpreters.xla.DeviceArray:
        """Calculates the triplet loss
    
        Args:
         v1: normalized batch for question 1
         v2: normalized batch for question 2
    
        Returns:
         triplet loss
        """
        scores = fastmath_numpy.dot(v1, v2.T)
        batch_size = len(scores)
        positive = fastmath_numpy.diagonal(scores)
        negative_without_positive = scores - (fastmath_numpy.eye(batch_size) * 2.0)
        closest_negative = fastmath_numpy.max(negative_without_positive, axis=1)
        negative_zero_on_duplicate = (1.0 - fastmath_numpy.eye(batch_size)) * scores
        mean_negative = fastmath_numpy.sum(negative_zero_on_duplicate, axis=1)/(batch_size - 1)
        triplet_loss1 = fastmath_numpy.maximum(0, self.margin - positive + closest_negative)
        triplet_loss2 = fastmath_numpy.maximum(0, (self.margin - positive) + mean_negative)
        return fastmath_numpy.mean(triplet_loss1 + triplet_loss2)
