import numpy

def sigmoid(x):
    """
    Compute the sigmoid of x

    Args:
     x: A scalar or numpy array of any size

    Returns:
     array: sigmoid(x)
    """
    return 1/(1 + numpy.exp(-x))
