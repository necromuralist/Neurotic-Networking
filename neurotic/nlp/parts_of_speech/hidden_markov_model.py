# python
from collections import Counter

import math

# pypi
import attr
import numpy

# this project
from .preprocessing import DataLoader, Empty
from .training import TheTrainer
from .matrices import Matrices


class AlgorithmError(Exception):
    """Called when the methods are called out of order"""


@attr.s(auto_attribs=True)
class HiddenMarkov:
    """A Hidden Markov Model Class

    Args:
     loader: a DataLoader
     trainer: A TheTrainer object
     matrices: A Matrices object
    """
    loader: DataLoader
    trainer: TheTrainer
    matrices: Matrices
    best_probabilities: numpy.ndarray=None
    best_paths: numpy.ndarray=None
    _states: list=None
    _tag_counts: Counter=None
    _tag_count: int=None
    _transition_matrix: numpy.ndarray=None
    _emission_matrix: numpy.ndarray=None
    _test_words: list=None
    _test_word_count: int=None
    _vocabulary: dict=None
    _start_token_index: int=None
    _negative_infinity: float = None

    @property
    def states(self) -> list:
        """POS Tags representing nodes in the HMM graph
    
        Returns:
         list of POS tags found in the training set
        """
        if self._states is None:
            self._states = self.matrices.tags
        return self._states

    @property
    def tag_counts(self) -> Counter:
        """The number of times a POS tag was in the training set
    
        Returns:
         dict-like of POS: Count
        """
        if self._tag_counts is None:
            self._tag_counts = self.trainer.tag_counts
        return self._tag_counts

    @property
    def tag_count(self) -> int:
        """The Number of tags in the corpus"""
        if self._tag_count is None:
            self._tag_count = len(self.tag_counts)
        return self._tag_count

    @property
    def transition_matrix(self) -> numpy.ndarray:
        """The 'A' Matrix with the transitions"""
        if self._transition_matrix is None:
            self._transition_matrix = self.matrices.transition
        return self._transition_matrix

    @property
    def emission_matrix(self) -> numpy.ndarray:
        """The Emission matrix (B)"""
        if self._emission_matrix is None:
            self._emission_matrix = self.matrices.emission
        return self._emission_matrix

    @property
    def test_words(self) -> list:
        """The preprocessed test-words"""
        if self._test_words is None:
            self._test_words = self.loader.test_words
        return self._test_words

    @property
    def test_word_count(self) -> int:
        """Number of words in the test set"""
        if self._test_word_count is None:
            self._test_word_count = len(self.test_words)
        return self._test_word_count

    @property
    def vocabulary(self) -> dict:
        """Training tokens mapped to index in the training corpus"""
        if self._vocabulary is None:
            self._vocabulary = self.loader.vocabulary
        return self._vocabulary

    @property
    def start_token_index(self) -> int:
        """The index of the start token in the graph states"""
        if self._start_token_index is None:
            self._start_token_index = self.states.index(Empty.tag)
        return self._start_token_index

    @property
    def negative_infinity(self) -> float:
        """a value for no probability"""
        if self._negative_infinity is None:
            self._negative_infinity = float("-inf")
        return self._negative_infinity

    def initialize_matrices(self):
        """Initializes the ``best_probs`` and ``best_paths`` matrices
    
        """
        self.best_probabilities = numpy.zeros((self.tag_count, self.test_word_count))
        self.best_paths = numpy.zeros((self.tag_count, self.test_word_count), dtype=int)
        
        for pos_tag in range(len(self.states)):
            if self.transition_matrix[self.start_token_index, pos_tag] == 0:
                self.best_probabilities[pos_tag, 0] = self.negative_infinity
            else:
                self.best_probabilities[pos_tag, 0] = (
                    math.log(self.transition_matrix[self.start_token_index, pos_tag])
                    + math.log(self.emission_matrix[
                        pos_tag, self.vocabulary[self.test_words[0]]]))
        return

    def viterbi_forward(self):
        """The forward training pass
    
        Raises:
          AlgorithmError: initalize_matrices wasn't run before this method
        """
        if self.best_probabilities is None:
            raise AlgorithmError("initialize_matrices must be called before viterbi_forward")
        for word in range(1, self.test_word_count): 
            for pos_tag in range(self.tag_count):
                best_probability_for_this_tag = self.negative_infinity
                best_path_for_this_tag = None
                for previous_possible_tag in range(self.tag_count):
    
                    probability = (
                        self.best_probabilities[previous_possible_tag, word-1]
                        + math.log(self.transition_matrix[previous_possible_tag, pos_tag])
                        + math.log(self.emission_matrix[
                            pos_tag,
                            self.vocabulary[self.test_words[word]]]))
    
                    if probability > best_probability_for_this_tag:
                        best_probability_for_this_tag = probability
                        best_path_for_this_tag = previous_possible_tag
                self.best_probabilities[pos_tag, word] = best_probability_for_this_tag
                self.best_paths[pos_tag, word] = best_path_for_this_tag
        return

    def viterbi_backward(self):
        """
        This function creates the best path.
    
        Raises:
         AlgorithmError: initialize or forward-pass not done
        """
        if self.best_probabilities is None:
            raise AlgorithmError("initialize and forward-pass not run")
        elif self.best_probabilities[:, 1:].sum() == 0:
            raise AlgorithmError("forward-pass not run")
    
        z = [None] * self.test_word_count
        
        best_probability_for_last_word = self.negative_infinity
        prediction = [None] * self.test_word_count
        last_column = self.test_word_count - 1
        for pos_tag in range(self.tag_count):
            if self.best_probabilities[pos_tag, last_column] > best_probability_for_last_word:
                best_probability_for_last_word = self.best_probabilities[pos_tag, last_column]
                z[last_column] = pos_tag
        prediction[last_column] = self.states[z[last_column]]
    
        for word in range(last_column, 0, -1):
            previous_word = word - 1
            pos_tag_for_word = z[word]
            z[previous_word] = self.best_paths[pos_tag_for_word, word]
            prediction[previous_word] = self.states[z[previous_word]]
        self.predictions = prediction    
        return

    def __call__(self):
        """Calls the methods in order"""
        self.initialize_matrices()
        self.viterbi_forward()
        self.viterbi_backward()
        return
