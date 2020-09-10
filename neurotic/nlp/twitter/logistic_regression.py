# from pypi
import attr
import numpy

# this project
from .counter import WordCounter
from .sentiment import TweetSentiment
from .vectorizer import TweetVectorizer

@attr.s(auto_attribs=True)
class LogisticRegression:
    """train and predict tweet sentiment

    Args:
     iterations: number of times to run gradient descent
     learning_rate: how fast to change the weights during training
    """
    iterations: int
    learning_rate: float
    _weights: numpy.array = None
    final_loss: float=None

    @property
    def weights(self) -> numpy.array:
        """The weights for the regression
    
        Initially this will be an array of zeros.
        """
        if self._weights is None:
            self._weights = numpy.zeros((3, 1))
        return self._weights

    @weights.setter
    def weights(self, new_weights: numpy.array) -> None:
        """Set the weights to a new value"""
        self._weights = new_weights
        return

    def sigmoid(self, vectors: numpy.ndarray) -> float:
        """Calculates the logistic function value
    
        Args:
         vectors: a matrix of bias, positive, negative counts
    
        Returns:
         array of probabilities that the tweets are positive
        """
        return 1/(1 + numpy.exp(-vectors))

    def gradient_descent(self, x: numpy.ndarray, y: numpy.ndarray):
        """Finds the weights for the model
    
        Args:
         x: the tweet vectors
         y: the positive/negative labels
        """
        assert len(x) == len(y)
        rows = len(x)
        self.learning_rate /= rows
        for iteration in range(self.iterations):
            y_hat = self.sigmoid(x.dot(self.weights))
            # average loss
            loss = numpy.squeeze(-((y.T.dot(numpy.log(y_hat))) +
                                   (1 - y.T).dot(numpy.log(1 - y_hat))))/rows
            gradient = ((y_hat - y).T.dot(x)).sum(axis=0, keepdims=True)
            self.weights -= self.learning_rate * gradient.T
        return loss

    def fit(self, x_train: numpy.ndarray, y_train:numpy.ndarray):
        """fits the weights for the logistic regression
    
        Note:
         as a side effect this also sets counter, loss, and sentimenter attributes
    
        Args:
         x_train: the training tweets
         y_train: the training labels
        """
        self.counter = WordCounter(x_train, y_train)
        vectorizer = TweetVectorizer(x_train, self.counter.counts, processed=False)
        y = y_train.values.reshape((-1, 1))
        self.loss = self.gradient_descent(vectorizer.vectors, y)
        return self.loss

    def predict(self, x: numpy.ndarray) -> numpy.ndarray:
        """Predict the labels for the inputs
    
        Args:
         x: a list or array of tweets
    
        Returns:
         array of predicted labels for the tweets
        """
        vectorizer = TweetVectorizer(x, self.counter.counts, processed=False)
        sentimenter = TweetSentiment(vectorizer, self.weights)
        return sentimenter()

    def score(self, x: numpy.ndarray, y: numpy.ndarray) -> float:
        """Get the mean accuracy
        
        Args:
         x: arrray of tweets
         y: labels for the tweets
    
        Returns:
         mean accuracy
        """
        predictions = self.predict(x)
        correct = sum(predictions.T[0] == y)
        return correct/len(x)
