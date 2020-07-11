# A Word Counter

# from python
from collections import Counter
import typing

# from pypi
import attr

# this project
from .processor import TwitterProcessor

@attr.s(auto_attribs=True)
class WordCounter:
    """A word-sentiment counter

    Args:
     tweets: list of unprocessed tweets
     labels: list of 1's (positive) and 0's that identifies sentiment for each tweet
    """
    tweets: typing.List[str]
    labels: typing.List[int]
    _process: TwitterProcessor = None
    _counts: Counter = None

    @property
    def process(self) -> TwitterProcessor:
        """A callable to process tweets to lists of words"""
        if self._process is None:
            self._process = TwitterProcessor()
        return self._process

    @property
    def counts(self) -> Counter:
        """Processes the tweets and labels

        Returns:
         counts of word-sentiment pairs
        """
        if self._counts is None:
            assert len(self.tweets) == len(self.labels), \
                f"Tweets: {len(self.tweets)}, Labels: {len(self.labels)}"
            self._counts = Counter()
            for tweet, label in zip(self.tweets, self.labels):
                for word in self.process(tweet):
                    self._counts[(word, label)] += 1
        return self._counts
