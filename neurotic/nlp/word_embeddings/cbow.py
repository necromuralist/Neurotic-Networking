# python
from collections import Counter, namedtuple
from enum import Enum, unique

# pypi
import attr
import numpy




@unique
class Axis(Enum):
    ROWS = 0
    COLUMNS = 1

Gradients = namedtuple("Gradients", ["input_weights", "hidden_weights", "input_bias", "hidden_bias"])

Weights = namedtuple("Weights", ["input_weights", "hidden_weights", "input_bias", "hidden_bias"])


@attr.s(auto_attribs=True)
class CBOW:
    """A continuous bag of words model builder

    Args:
     hidden: number of rows in the hidden layer
     vocabulary_size: number of tokens in the vocabulary
     learning_rate: learning rate for back-propagation updates
     random_seed: int
    """
    hidden: int
    vocabulary_size: int
    learning_rate: float=0.03
    random_seed: int=1    
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
    def input_weights(self) -> numpy.ndarray:
        """Weights for the first layer"""
        if self._input_weights is None:
            self._input_weights = self.random_generator.random(
                (self.hidden, self.vocabulary_size))
        return self._input_weights

    @property
    def hidden_weights(self) -> numpy.ndarray:
        """The weights for the hidden layer"""
        if self._hidden_weights is None:
            self._hidden_weights = self.random_generator.random(
                (self.vocabulary_size, self.hidden)
            )
        return self._hidden_weights

    @property
    def input_bias(self) -> numpy.ndarray:
        """Bias for the input layer"""
        if self._input_bias is None:
            self._input_bias = self.random_generator.random(
                (self.hidden, 1)
            )
        return self._input_bias

    @property
    def hidden_bias(self) -> numpy.ndarray:
        """Bias for the hidden layer"""
        if self._hidden_bias is None:
            self._hidden_bias = self.random_generator.random(
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
        second_layer_output = (numpy.dot(self.hidden_weights, first_layer_output)
                       + self.hidden_bias)
        return second_layer_output, first_layer_output

    def gradients(self, data: numpy.ndarray,
                  predicted: numpy.ndarray,
                  actual: numpy.ndarray,
                  hidden_input: numpy.ndarray) -> Gradients:
        """does the gradient calculation for back-propagation
    
        This is broken out to be able to troubleshoot/compare it
    
       Args:
         data: the input x value
         predicted: what our model predicted the labels for the data should be
         actual: what the actual labels should have been
         hidden_input: the input to the hidden layer
        Returns:
         Gradients for input_weight, hidden_weight, input_bias, hidden_bias
        """
        difference = predicted - actual
        batch_size = difference.shape[1]
        l1 = numpy.maximum(numpy.dot(self.hidden_weights.T, difference), 0)
    
        input_weights_gradient = numpy.dot(l1, data.T)/batch_size
        hidden_weights_gradient = numpy.dot(difference, hidden_input.T)/batch_size
        input_bias_gradient = numpy.sum(l1,
                                        axis=Axis.COLUMNS.value,
                                        keepdims=True)/batch_size
        hidden_bias_gradient = numpy.sum(difference,
                                         axis=Axis.COLUMNS.value,
                                         keepdims=True)/batch_size
        return Gradients(input_weights=input_weights_gradient,
                         hidden_weights=hidden_weights_gradient,
                         input_bias=input_bias_gradient,
                         hidden_bias=hidden_bias_gradient)

    def backward(self, data: numpy.ndarray,
                 predicted: numpy.ndarray,
                 actual: numpy.ndarray,
                 hidden_input: numpy.ndarray) -> None:
        """Does back-propagation to update the weights
    
       Arg:s
         data: the input x value
         predicted: what our model predicted the labels for the data should be
         actual: what the actual labels should have been
         hidden_input: the input to the hidden layer
        """
        gradients = self.gradients(data=data,
                                   predicted=predicted,
                                   actual=actual,
                                   hidden_input=hidden_input)
        # I don't have setters for the properties so use the private variables
        self._input_weights -= self.learning_rate * gradients.input_weights
        self._hidden_weights -= self.learning_rate * gradients.hidden_weights
        self._input_bias -= self.learning_rate * gradients.input_bias
        self._hidden_bias -= self.learning_rate * gradients.hidden_bias
        return

    def __call__(self, data: numpy.ndarray) -> numpy.ndarray:
        """makes a prediction on the data
    
        Args:
         data: input data for the prediction
        
        Returns:
         softmax of model output
        """
        output, _ = self.forward(data)
        return self.softmax(output)


@attr.s(auto_attribs=True)
class Batches:
    """Generates batches of data

    Args:
     data: the source of the data to generate (training data)
     word_to_index: dict mapping the word to the vocabulary index
     half_window: number of tokens on either side of word to grab
     batch_size: the number of entries per batch
     batches: number of batches to generate before quitting
     verbose: whether to emit messages
    """
    data: numpy.ndarray
    word_to_index: dict
    half_window: int
    batch_size: int
    batches: int
    repetitions: int=0
    verbose: bool=False    
    _vocabulary_size: int=None
    _vectors: object=None

    @property
    def vocabulary_size(self) -> int:
        """Number of tokens in the vocabulary"""
        if self._vocabulary_size is None:
            self._vocabulary_size = len(self.word_to_index)
        return self._vocabulary_size

    def indices_and_frequencies(self, context_words: list) -> list:
        """combines word-indexes and frequency counts-dict
    
        Args:
         context_words: words to get the indices for
    
        Returns:
         list of (word-index, word-count) tuples built from context_words
        """
        frequencies = Counter(context_words)
        indices = [self.word_to_index[word] for word in context_words]
        return [(indices[index], frequencies[context_words[index]])
                for index in range(len(indices))]

    @property
    def vectors(self):
        """our vector-generator started up"""
        if self._vectors is None:
            self._vectors = self.vector_generator()
        return self._vectors

    def vector_generator(self):
        """Generates vectors infinitely
        
        x: fraction of context words represented by word
        y: array with 1 where center word is in the vocabulary and 0 elsewhere
    
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

    def __next__(self) -> tuple:
        """Creates the batches and returns them
    
        Returns:
         x, y batches
        """
        batch_x = []
        batch_y = []
    
        if self.repetitions == self.batches:
            raise StopIteration()
        self.repetitions += 1    
        for x, y in self.vectors:
            if len(batch_x) < self.batch_size:
                batch_x.append(x)
                batch_y.append(y)
            else:
                return numpy.array(batch_x).T, numpy.array(batch_y).T
        return


@attr.s(auto_attribs=True)
class TheTrainer:
    """Something to train the model

    Args:
     model: thing to train
     batches: batch generator
     learning_impairment: rate to slow the model's learning
     impairment_point: how frequently to impair the learner
     emit_point: how frequently to emit messages
     verbose: whether to emit messages
    """
    model: CBOW
    batches: Batches
    learning_impairment: float=0.66
    impairment_point: int=100
    emit_point: int=10
    verbose: bool=False
    _losses: list=None

    @property
    def losses(self) -> list:
        """Holder for the training losses"""
        if self._losses is None:
            self._losses = []
        return self._losses

    def __call__(self):    
        """Trains the model using gradient descent
        """
        self.best_loss = float("inf")
        for repetitions, x_y in enumerate(self.batches):
            x, y = x_y
            output, hidden_input = self.model.forward(x)
            predictions = self.model.softmax(output)
    
            loss = self.cross_entropy_loss(predicted=predictions, actual=y)
            if loss < self.best_loss:
                self.best_loss = loss
                self.best_weights = Weights(
                    self.model.input_weights.copy(),
                    self.model.hidden_weights.copy(),
                    self.model.input_bias.copy(),
                    self.model.hidden_bias.copy(),
                )
            self.losses.append(loss)
            self.model.backward(data=x, predicted=predictions, actual=y,
                                hidden_input=hidden_input)
            if ((repetitions + 1) % self.impairment_point) == 0:
                self.model.learning_rate *= self.learning_impairment
                if self.verbose:
                    print(f"new learning rate: {self.model.learning_rate}")
            if self.verbose and ((repetitions + 1) % self.emit_point == 0):
                print(f"{repetitions + 1}: loss={self.losses[repetitions]}")
        return 

    def cross_entropy_loss(self, predicted: numpy.ndarray,
                           actual: numpy.ndarray) -> numpy.ndarray:
        """Calculates the cross-entropy loss
    
        Args:
         predicted: array with the model's guesses
         actual: array with the actual labels
    
        Returns:
         the cross-entropy loss
        """
        log_probabilities = (numpy.multiply(numpy.log(predicted), actual)
                             + numpy.multiply(numpy.log(1 - predicted), 1 - actual))
        cost = -numpy.sum(log_probabilities)/self.batches.batch_size
        return numpy.squeeze(cost)
