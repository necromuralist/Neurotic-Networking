# python
from argparse import Namespace
from itertools import cycle

import random

# pypi
from nltk.corpus import twitter_samples

import attr
import numpy

# this project
from .processor import TwitterProcessor

Defaults = Namespace(
    split = 4000,
)

NLTK = Namespace(
    corpus="twitter_samples",
    negative = "negative_tweets.json",
    positive="positive_tweets.json",
)

SpecialTokens = Namespace(padding="__PAD__",
                          ending="__</e>__",
                          unknown="__UNK__")

SpecialIDs = Namespace(
    padding=0,
    ending=1,
    unknown=2,
)

@attr.s(auto_attribs=True)
class TensorBuilder:
    """converts tweets to tensors

    Args: 
     - split: where to split the training and validation data
    """
    split = Defaults.split
    _positive: list=None
    _negative: list=None
    _positive_training: list=None
    _negative_training: list=None
    _positive_validation: list=None
    _negative_validation: list=None
    _process: TwitterProcessor=None
    _vocabulary: dict=None
    _x_train: list=None

    @property
    def positive(self) -> list:
        """The raw positive NLTK tweets"""
        if self._positive is None:
            self._positive = twitter_samples.strings(NLTK.positive)
        return self._positive

    @property
    def negative(self) -> list:
        """The raw negative NLTK tweets"""
        if self._negative is None:
            self._negative = twitter_samples.strings(NLTK.negative)
        return self._negative

    @property
    def positive_training(self) -> list:
        """The positive training data"""
        if self._positive_training is None:
            self._positive_training = self.positive[:self.split]
        return self._positive_training

    @property
    def negative_training(self) -> list:
        """The negative training data"""
        if self._negative_training is None:
            self._negative_training = self.negative[:self.split]
        return self._negative_training

    @property
    def positive_validation(self) -> list:
        """The positive validation data"""
        if self._positive_validation is None:
            self._positive_validation = self.positive[self.split:]
        return self._positive_validation

    @property
    def negative_validation(self) -> list:
        """The negative validation data"""
        if self._negative_validation is None:
            self._negative_validation = self.negative[self.split:]
        return self._negative_validation

    @property
    def process(self) -> TwitterProcessor:
        """processor for tweets"""
        if self._process is None:
            self._process = TwitterProcessor()
        return self._process

    @property
    def vocabulary(self) -> dict:
        """A map of token to numeric id"""
        if self._vocabulary is None:
            self._vocabulary = {SpecialTokens.padding: SpecialIDs.padding,
                                SpecialTokens.ending: SpecialIDs.ending,
                                SpecialTokens.unknown: SpecialIDs.unknown}
            for tweet in self.x_train:
                for token in self.process(tweet):
                    if token not in self._vocabulary:
                        self._vocabulary[token] = len(self._vocabulary)
        return self._vocabulary

    @property
    def x_train(self) -> list:
        """The unprocessed training data"""
        if self._x_train is None:
            self._x_train = self.positive_training + self.negative_training
        return self._x_train

    def to_tensor(self, tweet: str) -> list:
        """Converts tweet to list of numeric identifiers
    
        Args:
         tweet: the string to convert
    
        Returns:
         list of IDs for the tweet
        """
        tensor = [self.vocabulary.get(token, SpecialIDs.unknown)
                  for token in self.process(tweet)]
        return tensor


@attr.s(auto_attribs=True)
class TensorGenerator:
    """Generates batches of vectorized-tweets

    Args:
     converter: TensorBuilder object
     positive_data: list of positive data
     negative_data: list of negative data
     batch_size: the size for each generated batch     
     shuffle: whether to shuffle the generated data
     infinite: whether to generate data forever
    """
    converter: TensorBuilder
    positive_data: list
    negative_data: list
    batch_size: int
    shuffle: bool=True
    infinite: bool = True
    _positive_indices: list=None
    _negative_indices: list=None
    _positives: iter=None
    _negatives: iter=None

    @property
    def positive_indices(self) -> list:
        """The indices to use to grab the positive tweets"""
        if self._positive_indices is None:
            k = len(self.positive_data)
            if self.shuffle:
                self._positive_indices = random.sample(range(k), k=k)
            else:
                self._positive_indices = list(range(k))
        return self._positive_indices

    @property
    def negative_indices(self) -> list:
        """Indices for the negative tweets"""
        if self._negative_indices is None:
            k = len(self.negative_data)
            if self.shuffle:
                self._negative_indices = random.sample(range(k), k=k)
            else:
                self._negative_indices = list(range(k))
        return self._negative_indices

    @property
    def positives(self):
        """The positive index generator"""
        if self._positives is None:
            self._positives = self.positive_generator()
        return self._positives

    @property
    def negatives(self):
        """The negative index generator"""
        if self._negatives is None:
            self._negatives = self.negative_generator()
        return self._negatives

    def positive_generator(self):
        """Generator of indices for positive tweets"""
        stop = len(self.positive_indices)
        index = 0
        while True:
            yield self.positive_indices[index]
            index += 1
            if index == stop:
                if not self.infinite:
                    break
                if self.shuffle:
                    self._positive_indices = None
                index = 0
        return

    def negative_generator(self):
        """generator of indices for negative tweets"""
        stop = len(self.negative_indices)
        index = 0
        while True:
            yield self.negative_indices[index]
            index += 1
            if index == stop:
                if not self.infinite:
                    break
                if self.shuffle:
                    self._negative_indices = None
                index = 0
        return

    def __iter__(self):
        return self

    def __next__(self):
        assert self.batch_size % 2 == 0
        half_batch = self.batch_size // 2
    
        # get the indices
        positives = (next(self.positives) for index in range(half_batch))
        negatives = (next(self.negatives) for index in range(half_batch))
        
        # get the tweets
        positives = (self.positive_data[index] for index in positives)
        negatives = (self.negative_data[index] for index in negatives)
    
        # get the token ids
        try:    
            positives = [self.converter.to_tensor(tweet) for tweet in positives]
            negatives = [self.converter.to_tensor(tweet) for tweet in negatives]
        except RuntimeError:
            # python changed the behavior to not stop a generator on StopIteration
            # the next(self.positives) will raise a RuntimeError if
            # we're not running this infinitely
            raise StopIteration
    
        batch = positives + negatives
    
        longest = max((len(tweet) for tweet in batch))
    
        paddings = (longest - len(tensor) for tensor in batch)
        paddings = ([0] * padding for padding in paddings)
    
        padded = [tensor + padding for tensor, padding in zip(batch, paddings)]
        inputs = numpy.array(padded)
    
        # the labels for the inputs
        targets = numpy.array([1] * half_batch + [0] * half_batch)
    
        assert len(targets) == len(batch)
    
        # default the weights to ones
        weights = numpy.ones_like(targets)    
        return inputs, targets, weights
