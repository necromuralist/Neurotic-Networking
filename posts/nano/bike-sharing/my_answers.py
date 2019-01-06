import numpy

class NeuralNetwork(object):
    """Implementation of a neural network with one hidden layer

    Args:
     input_nodes: number of input nodes
     hidden_nodes: number of hidden nodes
     output_nodes: number of output_nodes
     learning_rate: rate at which to update the weights
    """
    def __init__(self, input_nodes: int, hidden_nodes: int, output_nodes:int,
                 learning_rate: float) -> None:
        # Set number of nodes in input, hidden and output layers.
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        self.learning_rate = learning_rate

        # Initialize weights
        self._weights_input_to_hidden = None
        self._weights_hidden_to_output = None
        return

    @property
    def weights_input_to_hidden(self) -> numpy.ndarray:
        """Array of weights from input layer to the hidden layer"""
        if self._weights_input_to_hidden is None:
            self._weights_input_to_hidden = numpy.random.normal(
                0.0, self.input_nodes**-0.5, 
                (self.input_nodes, self.hidden_nodes))
        return self._weights_input_to_hidden

    @weights_input_to_hidden.setter
    def weights_input_to_hidden(self, weights: numpy.ndarray) -> None:
        """Sets the weights"""
        self._weights_input_to_hidden = weights
        return

    @property
    def weights_hidden_to_output(self):
        """Array of weights for edges from hidden layer to output"""
        if self._weights_hidden_to_output is None:
            self._weights_hidden_to_output = numpy.random.normal(
                0.0,
                self.hidden_nodes**-0.5,
                (self.hidden_nodes, self.output_nodes))
        return self._weights_hidden_to_output

    @weights_hidden_to_output.setter
    def weights_hidden_to_output(self, weights: numpy.ndarray) -> None:
        """sets the weights for edges from hidden layer to output"""
        self._weights_hidden_to_output = weights
        return

    def activation_function(self, value):
        """A pass-through to the sigmoid"""
        return self.sigmoid(value)

    def sigmoid(self, value):
        """Calculates the sigmoid of the value"""
        return 1/(1 + numpy.exp(-value))

    def train(self, features, targets):
        ''' Train the network on batch of features and targets. 
        
            Arguments
            ---------
            
            features: 2D array, each row is one data record, each column is a feature
            targets: 1D array of target values
        
        '''
        n_records = features.shape[0]
        delta_weights_i_h = numpy.zeros(self.weights_input_to_hidden.shape)
        delta_weights_h_o = numpy.zeros(self.weights_hidden_to_output.shape)
        for X, y in zip(features, targets):            
            final_outputs, hidden_outputs = self.forward_pass_train(X)
            # Implement the backpropagation function below
            delta_weights_i_h, delta_weights_h_o = self.backpropagation(
                final_outputs, hidden_outputs, X, y, 
                delta_weights_i_h, delta_weights_h_o)
        self.update_weights(delta_weights_i_h, delta_weights_h_o, n_records)

    def forward_pass_train(self, X):
        ''' Implement forward pass here 
         
            Arguments
            ---------
            X: features batch

        '''
        hidden_inputs = numpy.matmul(X, self.weights_input_to_hidden)
        hidden_outputs = self.activation_function(hidden_inputs)

        final_inputs = numpy.matmul(hidden_outputs, self.weights_hidden_to_output)
        final_outputs = final_inputs
        return final_outputs, hidden_outputs

    def backpropagation(self, final_outputs, hidden_outputs, X, y, delta_weights_i_h, delta_weights_h_o):
        ''' Implement backpropagation
         
            Arguments
            ---------
            final_outputs: output from forward pass
            y: target (i.e. label) batch
            delta_weights_i_h: change in weights from input to hidden layers
            delta_weights_h_o: change in weights from hidden to output layers

        '''
        error = final_outputs - y
        
        hidden_error = numpy.matmul(self.weights_hidden_to_output, error)

        output_error_term = error
        
        hidden_error_term = hidden_error * hidden_outputs * (1 - hidden_outputs)
        
        delta_weights_i_h += -hidden_error_term * X[:, None]

        delta_weights_h_o += -output_error_term * hidden_outputs[:,None]
        return delta_weights_i_h, delta_weights_h_o

    def update_weights(self, delta_weights_i_h, delta_weights_h_o, n_records):
        ''' Update weights on gradient descent step
         
            Arguments
            ---------
            delta_weights_i_h: change in weights from input to hidden layers
            delta_weights_h_o: change in weights from hidden to output layers
            n_records: number of records

        '''
        self.weights_hidden_to_output += self.learning_rate * (delta_weights_h_o/n_records)
        self.weights_input_to_hidden += self.learning_rate * (delta_weights_i_h/n_records)
        return

    def run(self, features):
        ''' Run a forward pass through the network with input features 
        
            Arguments
            ---------
            features: 1D array of feature values
        '''
        
        hidden_inputs = numpy.matmul(features, self.weights_input_to_hidden)
        hidden_outputs = self.activation_function(hidden_inputs) 
       
        final_inputs = numpy.matmul(hidden_outputs, self.weights_hidden_to_output)
        final_outputs = final_inputs        
        return final_outputs

iterations = 7500
learning_rate = 0.4
hidden_nodes = 28
output_nodes = 1
