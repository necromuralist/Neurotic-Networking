# From python
from collections import Counter
from datetime import datetime
from typing import (
    List,
    Union,
    )
# from pypi
import numpy

SPLIT_ON_THIS = " "
Review = List[str]
Label = List[str]
Classification = Union[int, str]

class SentimentNetwork:
    """A network to predict if a review is positive or negative

    Args:
     hidden_nodes: Number of nodes to create in the hidden layer
     learning_rate: Learning rate to use while training        
     output_nodes: Number of output nodes (should always be 1)
     tokenizer: what to split on
     verbose: whether to output update information
    """
    def __init__(self,
                 hidden_nodes: int=10, 
                 learning_rate: float=0.1,
                 output_nodes: int=1,
                 tokenizer:str=" ",
                 verbose:bool=False) -> None:
        # Assign a seed to our random number generator to ensure we get
        # reproducable results during development 
        numpy.random.seed(1)
        self.hidden_nodes = hidden_nodes
        self.learning_rate = learning_rate
        self.output_nodes = output_nodes
        self.tokenizer = tokenizer
        self.verbose = verbose
        self._review_vocabulary = None
        self._label_vocabulary = None
        self._review_vocabulary_size = None
        self._label_vocabulary_size = None
        self._word_to_index = None
        self._label_to_index = None
        self._input_nodes = None
        self._weights_input_to_hidden = None
        self._weights_hidden_to_output = None
        self._input_layer = None
        return

    @property
    def review_vocabulary(self) -> List:
        """list of tokens in the reviews"""
        if self._review_vocabulary is None:
            vocabulary = set()
            for review in self.reviews:
                vocabulary.update(set(review.split(self.tokenizer)))
            self._review_vocabulary = list(vocabulary)
        return self._review_vocabulary
    
    @property
    def review_vocabulary_size(self) -> int:
        """The amount of tokens in our reviews"""
        if self._review_vocabulary_size is None:
            self._review_vocabulary_size = len(self.review_vocabulary)
        return self._review_vocabulary_size
    
    @property
    def label_vocabulary(self) -> List:
        """List of sentiment labels"""
        if self._label_vocabulary is None:
            self._label_vocabulary = list(set(self.labels))
        return self._label_vocabulary
    
    @property
    def label_vocabulary_size(self) -> int:
        """The amount of tokens in our labels"""
        if self._label_vocabulary_size is None:
            self._label_vocabulary_size = len(self.label_vocabulary)
        return self._label_vocabulary_size
    
    @property
    def word_to_index(self) -> dict:
        """maps a word to the index in our review vocabulary"""
        if self._word_to_index is None:
            self._word_to_index = {
                word: index
                for index, word in enumerate(self.review_vocabulary)}
        return self._word_to_index
    
    @property
    def label_to_index(self) -> dict:
        """maps a label to the index in our label vocabulary"""
        if self._label_to_index is None:
            self._label_to_index = {
                label: index
                for index, label in enumerate(self.label_vocabulary)}
        return self._label_to_index
    
    @property
    def input_nodes(self) -> int:
        """Number of input nodes"""
        if self._input_nodes is None:
            self._input_nodes = len(self.review_vocabulary)
        return self._input_nodes
    
    @property
    def weights_input_to_hidden(self) -> numpy.ndarray:
        """Weights for edges from input to hidden layer"""
        if self._weights_input_to_hidden is None:
            self._weights_input_to_hidden = numpy.zeros(
                (self.input_nodes, self.hidden_nodes))
        return self._weights_input_to_hidden
    
    @weights_input_to_hidden.setter
    def weights_input_to_hidden(self, weights: numpy.ndarray) -> None:
        """Set the weights"""
        self._weights_input_to_hidden = weights
        return
    
    @property
    def weights_hidden_to_output(self) -> numpy.ndarray:
        """Weights for edges from hidden to output layer"""
        if self._weights_hidden_to_output is None:
            self._weights_hidden_to_output = numpy.random.random(
                (self.hidden_nodes, self.output_nodes))
        return self._weights_hidden_to_output
    
    @weights_hidden_to_output.setter
    def weights_hidden_to_output(self, weights: numpy.ndarray) -> None:
        """updates the weights"""
        self._weights_hidden_to_output = weights
        return
    
    @property
    def input_layer(self) -> numpy.ndarray:
        """The Input Layer for the review tokens"""
        if self._input_layer is None:
            self._input_layer = numpy.zeros((1, self.input_nodes))
        return self._input_layer
    
    @input_layer.setter
    def input_layer(self, layer: numpy.ndarray) -> None:
        """Set the input layer"""
        self._input_layer = layer
        return

    def update_input_layer(self, review: str) -> None:
        """Update the counts in the input layer

        Args:
         review: A movie review
        """
        # reset any previous inputs
        self.input_layer *= 0
        tokens = review.split(self.tokenizer)
        counter = Counter()
        counter.update(tokens)
        for key, value in counter.items():
            if key in self.word_to_index:
                self.input_layer[:, self.word_to_index[key]] = value
        return

    def get_target_for_label(self, label: str) -> int:
        """Convert a label to `0` or `1`.
        Args:
         label(string) - Either "POSITIVE" or "NEGATIVE".
        Returns:
         `0` or `1`.
        """
        return 1 if label=="POSITIVE" else 0

    def sigmoid(self, x: numpy.ndarray) -> numpy.ndarray:
        """calculates the sigmoid for the input

        Args:
         x: vector to calculate the sigmoid

        Returns:
         sigmoid of x
        """
        return 1/(1 + numpy.exp(-x))

    def sigmoid_output_to_derivative(self, output: numpy.ndarray) -> numpy.ndarray:
        """Calculates the derivative if the sigmoid

        Args:
         output: the sigmoid output
        """
        return output * (1 - output)

    def train(self, training_reviews: Review, training_labels: Label) -> int:
        """Trains the model

        Args:
         training_reviews: list of reviews
         training_labels: listo of labels for the reviews

        Returns:
         count of correct
        """
        # there are side-effects that require self.reviews and self.labels
        self.reviews, self.labels = training_reviews, training_labels

        assert(len(training_reviews) == len(training_labels))
        correct_so_far = 0

        if self.verbose:        
            # Remember when we started for printing time statistics
            start = datetime.now()

        # loop through all the given reviews and run a forward and backward pass,
        # updating weights for every item
        reviews_labels = zip(training_reviews, training_labels)
        n_records = len(training_reviews)

        for index, (review, label) in enumerate(reviews_labels):
            # feed-forward
            self.update_input_layer(review)
            hidden_inputs = self.input_layer.dot(self.weights_input_to_hidden)
            hidden_outputs = hidden_inputs.dot(self.weights_hidden_to_output)
            output = self.sigmoid(hidden_outputs)

            # Backpropagation
            # we need to calculate the output_error separately
            # to update our correct count
            output_error = output - self.get_target_for_label(label)

            # we applied a sigmoid to the output
            # so we need to apply the derivative
            hidden_to_output_delta = (
                output_error
                * self.sigmoid_output_to_derivative(output))

            input_to_hidden_error = hidden_to_output_delta.dot(
                self.weights_hidden_to_output.T)
            # we didn't apply a function to the inputs to the hidden layer
            # so we don't need a derivative
            input_to_hidden_delta = input_to_hidden_error

            # our delta is based on the derivative which is heading
            # in the opposite direction of what we want so we need to negate it
            self.weights_hidden_to_output -= (
                self.learning_rate
                * hidden_inputs.T.dot(hidden_to_output_delta))
            self.weights_input_to_hidden -= (
                self.learning_rate
                * self.input_layer.T.dot(input_to_hidden_delta))

            if ((output < 0.5 and label=="NEGATIVE")
                or (output >= 0.5 and label=="POSITIVE")):
                correct_so_far += 1
            if self.verbose and not index % 1000:
                elapsed_time = datetime.now() - start
                reviews_per_second = (index/elapsed_time.seconds
                                      if elapsed_time.seconds > 0 else 0)
                print(
                    "Progress: {:.2f} %".format(100 * index/len(training_reviews))
                    + " Speed(reviews/sec): {:.2f}".format(reviews_per_second)
                    + " Error: {}".format(output_error[0])
                    + " #Correct: {}".format(correct_so_far)
                    + " #Trained: {}".format(index+1)
                    + " Training Accuracy: {:.2f} %".format(
                        correct_so_far * 100/float(index+1))
                    )
        if self.verbose:
            print("Training Time: {}".format(datetime.now() - start))
        return correct_so_far

    def test(self, testing_reviews: list, testing_labels:list) -> int:
        """
        Attempts to predict the labels for the given testing_reviews,
        and uses the test_labels to calculate the accuracy of those predictions.

        Returns:
         correct: number of correct predictions
        """
        
        # keep track of how many correct predictions we make
        correct = 0

        # we'll time how many predictions per second we make
        start = datetime.now()

        # Loop through each of the given reviews and call run to predict
        # its label.
        reviews_and_labels = zip(testing_reviews, testing_labels)
        for index, (review, label) in enumerate(reviews_and_labels):
            prediction = self.run(review)
            if prediction == label:
                correct += 1

            if not index % 100:
                elapsed_time = datetime.now() - start
                reviews_per_second = (index/elapsed_time.seconds
                                      if elapsed_time.seconds > 0 else 0)
                
                print(
                    "Progress: {:.2f}%".format(
                        100 * index/len(testing_reviews))
                    + " Speed(reviews/sec): {:.2f}".format(reviews_per_second)
                    + " #Correct: {}".format(correct)
                    + " #Tested: {}".format(index + 1)
                    + " Testing Accuracy: {:.2f} %".format(
                        correct * 100/(index+1))
                )
        return correct

    def run(self, review: str) -> str:
        """
        Returns a POSITIVE or NEGATIVE prediction for the given review.
        """
        review = review.lower()
        self.update_input_layer(review)
        hidden_inputs = self.input_layer.dot(self.weights_input_to_hidden)
        hidden_outputs = hidden_inputs.dot(self.weights_hidden_to_output)
        output = self.sigmoid(hidden_outputs)
        return "POSITIVE" if output[0] >= 0.5 else "NEGATIVE"
