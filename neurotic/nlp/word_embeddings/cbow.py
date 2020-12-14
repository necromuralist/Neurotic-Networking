# python
from enum import Enum, unique

# pypi
import attr
import numpy

# this project
from .data_loader import MetaData



@unique
class Axis(Enum):
    ROWS = 0
    COLUMNS = 1


@attr.s(auto_attribs=True)
class CBOW:
    """A continuous bag of words model builder

    Args:
     hidden: number of rows in the hidden layer
     meta: MetaData
     random_seed: int
    """
    hidden: int
    meta: MetaData
    random_seed: int=1
    _vocabulary_size: int=None
    _random_generator: numpy.random.PCG64=None
    
    # layer one
    _input_weights: numpy.ndarray=None
    _input_bias: numpy.ndarray=None

    # hidden layer
    _hidden_weights: numpy.ndarray=None
    _hidden_bias: numpy.ndarray=None

    @property
    def random_generator(self) -> numpy.random.PCG64:
        """The random number generator"""
        if self._random_generator is None:
            self._random_generator = numpy.random.default_rng(self.random_seed)
        return self._random_generator

    @property
    def vocabulary_size(self) -> int:
        """Number of tokens in the vocabulary"""
        if self._vocabulary_size is None:
            self._vocabulary_size = len(self.meta.vocabulary)
        return self._vocabulary_size

    @property
    def input_weights(self) -> numpy.ndarray:
        """Weights for the first layer"""
        if self._input_weights is None:
            self._input_weights = self.random_generator.standard_normal(
                (self.hidden, self.vocabulary_size))
        return self._input_weights

    @property
    def hidden_weights(self) -> numpy.ndarray:
        """The weights for the hidden layer"""
        if self._hidden_weights is None:
            self._hidden_weights = self.random_generator.standard_normal(
                (self.vocabulary_size, self.hidden))
        return self._hidden_weights

    @property
    def input_bias(self) -> numpy.ndarray:
        """Bias for the input layer"""
        if self._input_bias is None:
            self._input_bias = self.random_generator.standard_normal(
                (self.hidden, 1)
            )
        return self._input_bias

    @property
    def hidden_bias(self) -> numpy.ndarray:
        """Bias for the hidden layer"""
        if self._hidden_bias is None:
            self._hidden_bias = self.random_generator.standard_normal(
                (self.vocabulary_size, 1)
            )
        return self._hidden_bias

    def softmax(self, scores: numpy.ndarray) -> numpy.ndarray:
        """Calculate the softmax
    
        Args: 
            scores: output scores from the hidden layer
        Returns: 
            yhat: prediction (estimate of y)"""
        return numpy.exp(scores)/numpy.sum(numpy.exp(scores), axis=Axis.ROWS.value)

    def forward(self, data: numpy.ndarray) -> tuple:
        """makes a model prediction
    
        Args:
         data: x-values to train on
    
        Returns:
         output, first-layer output
        """
        first_layer_output = numpy.maximum(numpy.dot(self.input_weights, data)
                                      + self.input_bias, 0)
        predictions = (numpy.dot(self.hidden_weights, first_layer_output)
                       + self.hidden_bias)
        return predictions, first_layer_output


@attr.s(auto_attribs=True)
class Batches:
    """Generates batches of data

    Args:
     data: the source of the data to generate (training data)
     word_to_index: dict mapping the word to the vocabulary index
     half_window: number of tokens on either side of word to grab
     batch_size: the number of entries per batch
     verbose: whether to emit messages
    """
    data: numpy.ndarray
    word_to_index: dict
    half_window: int
    batch_size: int
    verbose: bool=False    
    _vocabulary_size: int=None    

    @property
    def vocabulary_size(self) -> int:
        """Number of tokens in the vocabulary"""
        if self._vocabulary_size is None:
            self._vocabulary_size = len(self.word_to_index)
        return self._vocabulary_size

    def indices_and_frequencies(self, context_words: list) -> list:
        """combines indexes and frequency counts-dict
    
        Args:
         context_words: words to get the indices for
    
        Returns:
         list of (word-index, word-count) tuples built from context_words
        """
        frequencies = Counter(context_words)
        indices = [self.word_to_index[word] for word in context_words]
        return [(indices[index], frequencies[context_words[index]])
                for index in range(len(indices))]

    def vectors(self):
        """Generates vectors infinitely
    
        Yields:
         tuple of x, y 
        """
        location = self.half_window
        while True:
            y = numpy.zeros(self.vocabulary_size)
            x = numpy.zeros(self.vocabulary_size)
            center_word = self.data[location]
            y[self.word_to_index[center_word]] = 1
            context_words = (
                self.data[(location - self.half_window): location]
                + self.data[(location + 1) : (location + self.half_window + 1)])
    
            for word_index, frequency in self.indices_and_frequencies(context_words):
                x[word_index] = frequency/len(context_words)
            yield x, y
            location += 1
            if location >= len(self.data):
                if self.verbose:
                    print("location in data is being set to 0")
                location = 0
        return

    def __iter__(self):
        """makes this into an iterator"""
        return self

    def __next__(self):
        batch_x = []
        batch_y = []
        for x, y in self.vectors():
            while len(batch_x) < batch_size:
                batch_x.append(x)
                batch_y.append(y)
            else:
                yield numpy.array(batch_x).T, numpy.array(batch_y).T
                batch = []    
        return
