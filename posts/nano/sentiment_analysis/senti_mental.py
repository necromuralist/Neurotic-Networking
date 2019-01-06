from sentiment_network import SentimentNetwork
class SentiMental(SentimentNetwork):
    """Implements a slightly optimized version"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hidden_layer = None
        self._target_for_label = None
        return

    @property
    def hidden_layer(self) -> numpy.ndarray:
        """The hidden layer nodes"""
        if self._hidden_layer is None:
            self._hidden_layer = numpy.zeros((1, self.hidden_nodes))
        return self._hidden_layer

    @hidden_layer.setter
    def hidden_layer(self, nodes: numpy.ndarray) -> None:
        """Set the hidden nodes"""
        self._hidden_layer = nodes
        return

    @property
    def target_for_label(self):
        """target to label map"""
        if self._target_for_label is None:
            self._target_for_label = dict(POSITIVE=1, NEGATIVE=0)
        return self._target_for_label

    def train(self, reviews:list, labels:list) -> None:
        """Trains the model

        Args:
         reviews: list of reviews
         labels: list of labels for each review
        """
        # make sure out we have a matching number of reviews and labels
        assert(len(reviews) == len(labels))
        if self.verbose:
            start = datetime.now()
            correct_so_far = 0
        
        # loop through all the given reviews and run a forward and backward pass,
        # updating weights for every item
        reviews_labels = zip(reviews, labels)
        n_records = len(reviews)

        for index, (review, label) in enumerate(reviews_labels):
            # feed-forward
            # Note: I keep thining I can just call run, but our error correction needs
            # the input layer so we have to do all the calculations
            # input layer is a list of indices for unique words in the review
            # that are in our vocabulary

            input_layer = [self.word_to_index[token]
                           for token in set(review.split(self.tokenizer))
                           if token in self.word_to_index]
            self.hidden_layer *= 0

            # here there's no multiplcation, just an implicit multiplication of 1
            for node in input_layer:
                self.hidden_layer += self.weights_input_to_hidden[node]

            hidden_outputs = self.hidden_layer.dot(self.weights_hidden_to_output)
            output = self.sigmoid(hidden_outputs)

            # Backpropagation
            # we need to calculate the output_error separately to update our correct count
            output_error = output - self.target_for_label[label]

            # we applied a sigmoid to the output so we need to apply the derivative
            hidden_to_output_delta = output_error * self.sigmoid_output_to_derivative(output)

            input_to_hidden_error = hidden_to_output_delta.dot(self.weights_hidden_to_output.T)
            # we didn't apply a function to the inputs to the hidden layer
            # so we don't need a derivative
            input_to_hidden_delta = input_to_hidden_error

            self.weights_hidden_to_output -= self.learning_rate * self.hidden_layer.T.dot(
                hidden_to_output_delta)
            for node in input_layer:
                self.weights_input_to_hidden[node] -= (
                    self.learning_rate
                    * input_to_hidden_delta[0])
            if self.verbose:
                if (output < 0.5 and label=="NEGATIVE") or (output >= 0.5 and label=="POSITIVE"):
                    correct_so_far += 1
                if not index % 1000:
                    elapsed_time = datetime.now() - start
                    reviews_per_second = (index/elapsed_time.seconds
                                          if elapsed_time.seconds > 0 else 0)
                    print(
                        "Progress: {:.2f} %".format(100 * index/len(reviews))
                        + " Speed(reviews/sec): {:.2f}".format(reviews_per_second)
                        + " Error: {}".format(output_error[0])
                        + " #Correct: {}".format(correct_so_far)
                        + " #Trained: {}".format(index+1)
                        + " Training Accuracy: {:.2f} %".format(
                            correct_so_far * 100/float(index+1))
                        )
        if self.verbose:
            print("Training Time: {}".format(datetime.now() - start))
        return

    def run(self, review: str, translate: bool=True) -> Classification:
        """
        Returns a POSITIVE or NEGATIVE prediction for the given review.

        Args:
         review: the review to classify
         translate: convert output to a string

        Returns:
         classification for the review
        """
        nodes = [self.word_to_index[token]
                 for token in set(review.split(self.tokenizer))
                 if token in self.word_to_index]
        self.hidden_layer *= 0
        for node in nodes:
            self.hidden_layer += self.weights_input_to_hidden[node]

        hidden_outputs = self.hidden_layer.dot(self.weights_hidden_to_output)
        output = self.sigmoid(hidden_outputs)
        if translate:
            output = "POSITIVE" if output[0] >= 0.5 else "NEGATIVE"
        return output
