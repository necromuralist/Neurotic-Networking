# python standard library
from typing import List
from collections import Counter

# from pypi
import numpy

# this project
from sentimental_network import SentiMental

class SentimentNoiseReduction(SentiMental):
    """reduces noise

    ... uml::
        
        SentimentNoiseReduction --|> SentiMental

    Args:
     lower_bound: threshold to add token to network
     polarity_cutoff: threshold for positive-negative ratio for words
    """
    def __init__(self, polarity_cutoff, lower_bound: int=50, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lower_bound = lower_bound
        self.polarity_cutoff = polarity_cutoff
        self._positive_counts = None
        self._negative_counts = None
        self._total_counts = None
        self._positive_negative_ratios = None
        return

    @property
    def review_vocabulary(self) -> List:
        """list of tokens in the reviews"""
        if self._review_vocabulary is None:
            # this needs to be called before total counts is used
            self.count_tokens()
            vocabulary = set()
            for review in self.reviews:
                tokens = set(review.split(self.tokenizer))
                tokens = (token for token in tokens
                          if self.total_counts[token] > self.lower_bound)
                tokens = (
                    token for token in tokens
                    if abs(self.positive_negative_ratios[token])
                           >= self.polarity_cutoff)
                vocabulary.update(tokens)
            self._review_vocabulary = list(vocabulary)
        return self._review_vocabulary

    @property
    def positive_counts(self) -> Counter:
        """Token counts for positive reviews"""
        if self._positive_counts is None:
            self._positive_counts = Counter()
        return self._positive_counts

    @property
    def negative_counts(self) -> Counter:
        """Token counts for negative reviews"""
        if self._negative_counts is None:
            self._negative_counts = Counter()
        return self._negative_counts

    @property
    def total_counts(self) -> Counter:
        """Token counts for total reviews"""
        if self._total_counts is None:
            self._total_counts = Counter()
        return self._total_counts

    @property
    def positive_negative_ratios(self) -> Counter:
        """log-ratio of positive to negative reviews"""
        if self._positive_negative_ratios is None:
            positive_negative_ratios = Counter()
            positive_negative_ratios.update(
                {token:
                 self.positive_counts[token]
                 /(self.negative_counts[token] + 1)
                 for token in self.total_counts})
            for token, ratio in positive_negative_ratios.items():
                if ratio > 1:
                    positive_negative_ratios[token] = numpy.log(ratio)
                else:
                    positive_negative_ratios[token] = -numpy.log(1/(ratio + 0.01))
            self._positive_negative_ratios = Counter()
            self._positive_negative_ratios.update(positive_negative_ratios)
        return self._positive_negative_ratios

    def count_tokens(self):
        """Populate the count-tokens"""
        self.reset_counters()
        for label, review in zip(self.labels, self.reviews):
            tokens = review.split(self.tokenizer)
            self.total_counts.update(tokens)
            if label == "POSITIVE":
                self.positive_counts.update(tokens)        
            else:
                self.negative_counts.update(tokens)
        return

    def reset_counters(self):
        """Set the counters back to none"""
        self._positive_counts = None
        self._negative_counts = None
        self._total_counts = None
        self._positive_negative_ratios = None
        return
