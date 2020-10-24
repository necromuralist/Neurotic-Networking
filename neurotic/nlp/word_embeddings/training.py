# pypi
import attr
import numpy

# my stuff
from graeae import Timer


@attr.s(auto_attribs=True)
class TheTrainer:
    """Trains the word-embeddings data

    Args:
     x_train: the training input
     y_train: the training labels
     training_steps: number of times to run the training loop
     learning_rate: multiplier for the gradient (alpha)
     seed: random-seed for numpy
     loss_every: if verbose, how often to show loss during fitting
     verbose: whether to emit messages
    """
    x_train: numpy.ndarray
    y_train: numpy.ndarray
    _timer: Timer=None
    training_steps: int=400
    learning_rate: float=0.8
    seed: int=129
    loss_every: int=25
    verbose: bool=True

    @property
    def timer(self) -> Timer:
        """A timer"""
        if self._timer is None:
            self._timer = Timer(emit=self.verbose)
        return self._timer

    def loss(self, transformation: numpy.ndarray) -> numpy.float:
        """
        Calculates the loss between XR and Y as the average sum of difference squared
    
        Args: 
            transformation: a matrix of dimension (n,n) - transformation matrix.
    
        Returns:
            loss: value of loss function for X, Y and R
        """
        rows, columns = self.x_train.shape
        
        difference = numpy.dot(self.x_train, transformation) - self.y_train
        difference_squared = difference**2
        sum_of_difference_squared = difference_squared.sum()
        return sum_of_difference_squared/rows

    def gradient(self, transformation: numpy.ndarray) -> numpy.ndarray:
        """computes the gradient (slope) of the loss
        
        Args: 
            transformation: transformation matrix of dimension (n,n)
    
        Returns:
            gradient: a matrix of dimension (n,n)
        """
        rows, columns = self.x_train.shape
    
        gradient = (
            numpy.dot(self.x_train.T,
                      numpy.dot(self.x_train, transformation) - self.y_train) * 2
        )/rows
        assert gradient.shape == (columns, columns)
        return gradient

    def fit(self) -> numpy.ndarray:
        """Fits the transformation matrix to the data
    
        Side Effect:
         sets self.transformation  and self.losses
    
        Returns:
         the projection matrix that minimizes the F norm ||X R -Y||^2
        """
        numpy.random.seed(self.seed)
        assert self.x_train.shape == self.y_train.shape
        rows, columns = self.x_train.shape
        self.transformation = numpy.random.rand(columns, columns)
        self.losses = []
        if self.verbose:
            print("Step\tLoss")
        with self.timer:
            for step in range(self.training_steps):
                loss = self.loss(self.transformation)
                if self.verbose and step % 25 == 0:
                    print(f"{step}\t{loss:0.4f}")
                self.transformation -= self.learning_rate * self.gradient(
                    self.transformation)
                self.losses.append(loss)
        assert self.transformation.shape == (columns, columns)
        return self.transformation
