# python
from functools import partial

# from pypi
from trax.fastmath import numpy as fastmath_numpy
from trax import layers

import attr
import jax
import numpy
import trax


def triplet_loss(v1: numpy.ndarray,
             v2: numpy.ndarray, margin: float=0.25)-> jax.interpreters.xla.DeviceArray:
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
    triplet_loss1 = fastmath_numpy.maximum(0, margin - positive + closest_negative)
    triplet_loss2 = fastmath_numpy.maximum(0, (margin - positive) + mean_negative)
    return fastmath_numpy.mean(triplet_loss1 + triplet_loss2)

def triplet_loss_layer(margin: float=0.25) -> layers.Fn:
    """Converts the triplet_loss function to a trax layer"""
    with_margin = partial(triplet_loss, margin=margin)
    return layers.Fn("TripletLoss", with_margin)
