# python
from argparse import Namespace
from collections import Counter
from typing import Iterable

# pypi
import attr
import numpy

# my stuff
from neurotic.nlp.twitter.counter import WordCounter

Sentiment = Namespace(
    negative = 0,
    positive = 1,
)

@attr.s(auto_attribs=True)
class NaiveBayes:
    """Naive Bayes Sentiment Classifier for Tweets

    Args:
     tweets: the training tweets
     labels: the sentiment labels for the training tweets
    """
    tweets: Iterable
    labels: Iterable
    _counter: WordCounter = None
    _vocabulary: set = None
    _logprior: float = None
    _loglikelihood: dict = None

    @property
    def counter(self) -> WordCounter:
        """The word processor/counter"""
        if self._counter is None:
            self._counter = WordCounter(self.tweets, self.labels)
        return self._counter

    @property
    def vocabulary(self) -> set:
        """The unique tokens in the tweets"""
        if self._vocabulary is None:
            self._vocabulary = {key[0] for key in self.counter.counts}
        return self._vocabulary

    @property
    def logprior(self) -> float:
        """the log-odds of the priors"""
        if self._logprior is None:
            positive_documents = numpy.sum(self.labels)
            negative_documents = len(self.labels) - positive_documents
            self._logprior = numpy.log(positive_documents) - numpy.log(negative_documents)
        return self._logprior

    @property
    def loglikelihood(self) -> dict:
        """The log-likelihoods for words"""
        if self._loglikelihood is None:
            self._loglikelihood = {}
            counts = self.counter.counts        
    
            all_positive_words = sum(
                (counts[(token, sentiment)] for token, sentiment in counts
                 if sentiment == Sentiment.positive))
            all_negative_words = sum(
                (counts[(token, sentiment)] for token, sentiment in counts
                 if sentiment == Sentiment.negative))
            vocabulary_size = len(self.vocabulary)
    
            for word in self.vocabulary:
                this_word_positive_count = counts[(word, Sentiment.positive)]
                this_word_negative_count = counts[(word, Sentiment.negative)]
    
                probability_word_is_positive = ((this_word_positive_count + 1)/
                                             (all_positive_words + vocabulary_size))
                probability_word_is_negative = ((this_word_negative_count + 1)/
                                             (all_negative_words + vocabulary_size))
    
                self._loglikelihood[word] = (numpy.log(probability_word_is_positive) -
                                             numpy.log(probability_word_is_negative))
        return self._loglikelihood

    def predict_ratio(self, tweet: str) -> float:
        """predict the odds-ratio positive/negative
    
        Args:
         tweet: the tweet to predict
    
        Returns:
         log-odds-ratio for tweet (positive/negative)
        """
        tokens = self.counter.process(tweet)
        return self.logprior + sum(self.loglikelihood.get(token, 0) for token in tokens)

    def predict_sentiment(self, tweet: str) -> int:
        """Predict whether the tweet's sentiment is positive or negative
    
        Args:
         tweet: the 'document' to analyze
    
        Returns:
         the sentiment (0=negative, 1=positive)
        """
        return self.predict_ratio(tweet) > 0

    def check_rep(self) -> None:
        """Does some basic checks of the input arguments"""
        assert len(self.tweets) == len(self.labels)
        return
