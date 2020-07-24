# pypi
import attr
import numpy

# this project
from .vectorizer import TweetVectorizer


@attr.s(auto_attribs=True)
class TweetSentiment:
    """Predicts the sentiment of a tweet

    Args:
     vectorizer: something to vectorize tweets
     theta: vector of weights for the logistic regression model
    """
    vectorizer: TweetVectorizer
    theta: numpy.ndarray

    def sigmoid(self, vectors: numpy.ndarray) -> float:
        """the logistic function

        Args:
         vectors: a matrix of bias, positive, negative counts

        Returns:
         array of probabilities that the tweets are positive
        """
        return 1/(1 + numpy.exp(-vectors))

    def probability_positive(self, tweet: str) -> float:
        """Calculates the probability of the tweet being positive

        Args:
         tweet: a tweet to classify

        Returns:
         the probability that the tweet is a positive one
        """
        x = self.vectorizer.extract_features(tweet, as_array=True)
        return numpy.squeeze(self.sigmoid(x.dot(self.theta)))

    def classify(self, tweet: str) -> int:
        """Decides if the tweet was positive or not

        Args:
         tweet: the tweet message to classify.
        """
        return int(numpy.round(self.probability_positive(tweet)))

    def __call__(self) -> numpy.ndarray:
        """Get the sentiments of the vectorized tweets
        
        Note:
         this assumes that the vectorizer passed in has the tweets

        Returns:
         array of predicted sentiments (1 for positive 0 for negative)
        """
        return numpy.round(self.sigmoid(self.vectorizer.vectors.dot(self.theta)))
