# python
from argparse import Namespace
from collections import Counter
from typing import List, Union

# pypi
import numpy
import attr


# this package
from neurotic.nlp.twitter.processor import TwitterProcessor
from neurotic.nlp.twitter.counter import WordCounter

Columns = Namespace(
    bias=0,
    positive=1,
    negative=2
)

TweetClass = Namespace(
    positive=1,
    negative=0
)

# some types
Tweets = List[List[str]]
Vector = Union[numpy.ndarray, list]


@attr.s(auto_attribs=True)
class TweetVectorizer:
    """A tweet vectorizer

    Args:
     tweets: the pre-processed/tokenized tweets to vectorize
     counts: the counter with the tweet token counts
     processed: to not process the bulk tweets
     bias: constant to use for the bias
    """
    tweets: Tweets
    counts: Counter
    processed: bool=True
    bias: float=1
    _process: TwitterProcessor=None
    _vectors: numpy.ndarray=None

    @property
    def process(self) -> TwitterProcessor:
        """Processes tweet strings to tokens"""
        if self._process is None:
            self._process = TwitterProcessor()
        return self._process

    @property
    def vectors(self) -> numpy.ndarray:
        """The vectorized tweet counts"""
        if self._vectors is None:
            rows = [self.extract_features(tweet) for tweet in self.tweets]
            self._vectors = numpy.array(rows)
        return self._vectors

    def extract_features(self, tweet: str, as_array: bool=False) -> Vector:
        """converts a single tweet to an array of counts

        Args:
         tweet: a string tweet to count up
         as_array: whether to return an array instead of a list

        Returns:
         either a list of floats or a 1 x 3 array
        """
        # this is a hack to make this work both in bulk and one tweet at a time
        tokens = tweet if self.processed else self.process(tweet)
        vector = [
            self.bias,
            sum((self.counts[(token, TweetClass.positive)]
                 for token in tokens)),
            sum((self.counts[(token, TweetClass.negative)]
                                for token in tokens))
        ]
        vector = numpy.array([vector]) if as_array else vector
        return vector

    def reset(self) -> None:
        """Removes the vectors"""
        self._vectors = None
        return

    def check_rep(self) -> None:
        """Checks that the tweets and word-counter are set

        Raises:
         AssertionError if one of them isn't right
        """
        for tweet in self.tweets:
            assert type(tweet) is str
        assert type(self.counter) is Counter
        return
