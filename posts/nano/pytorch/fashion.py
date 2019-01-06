# from pypi
from torch import nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
import pandas
import torch


descriptions = ("T-shirt/top",
                "Trouser",
                "Pullover",
                "Dress",
                "Coat",
                "Sandal",
                "Shirt",
                "Sneaker",
                "Bag",
                "Ankle boot",
                )

label_decoder = dict(zip(range(10), descriptions))


class HyperParameters:
    inputs = 28**2
    hidden_layer_1 = 256
    hidden_layer_2 = 128
    hidden_layer_3 = 64
    outputs = 10
    axis = 1
    learning_rate = 0.003
    epochs = 30
    dropout_probability = 0.2


class DropoutModel(nn.Module):
    """Model with dropout to prevent overfitting

    Args:
     hyperparameters: object with the hyper-parameter settings
    """
    def __init__(self, hyperparameters: object=HyperParameters) -> None:
        super().__init__()
        self.input_to_hidden = nn.Linear(hyperparameters.inputs,
                                         hyperparameters.hidden_layer_1)
        self.hidden_1_to_hidden_2 = nn.Linear(hyperparameters.hidden_layer_1,
                                              hyperparameters.hidden_layer_2)
        self.hidden_2_to_hidden_3 = nn.Linear(hyperparameters.hidden_layer_2,
                                              hyperparameters.hidden_layer_3)
        self.hidden_3_to_output = nn.Linear(hyperparameters.hidden_layer_3,
                                            hyperparameters.outputs)

        # Dropout module with 0.2 drop probability
        self.dropout = nn.Dropout(p=hyperparameters.dropout_probability)
        return
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """One Forward pass through the network"""
        # make sure input tensor is flattened
        x = x.view(x.shape[0], -1)
        
        # Now with dropout
        x = self.dropout(F.relu(self.input_to_hidden(x)))
        x = self.dropout(F.relu(self.hidden_1_to_hidden_2(x)))
        x = self.dropout(F.relu(self.hidden_2_to_hidden_3(x)))
        
        # output so no dropout here
        return F.log_softmax(self.hidden_3_to_output(x),
                             dim=HyperParameters.axis)


def train(model:nn.Module, optimizer: object, criterion: object,
          train_batches: DataLoader , test_batches: DataLoader,
          epochs:int=30, emit: bool=True, device: object=None) -> pandas.DataFrame:
    """Trains the model and tests it

    Args:
     model: the torch model to train
     optimizer: something to take the forward step
     criterion: callable to calculate the loss (error)
     train_batches: the batch-iterator of training data
     test_batches: the batch-iterator of testing data
     epochs: number of times to re-run the training
     emit: if True, print loss as you go
     device: a cpu or cuda device

    Returns:
     train_loss, test_loss, accuracies: data-frame of metrics from training and testing
    """
    train_losses, test_losses, accuracies = [], [], []
    for epoch in range(epochs):
        total_loss = 0
        for inputs, labels in train_batches:
            if device:
                inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            # images = images.view(images.shape[0], -1)
            outputs = model.forward(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()        
        else:
            test_loss = 0
            accuracy = 0
            with torch.no_grad():
                for inputs, labels in test_batches:
                    if devices:
                        inputs, labels = inputs.to(device), labels.to(device)
                    output = model(inputs)
                    test_loss += criterion(outputs, labels).item()
                    probabilities = torch.exp(outputs)
                    top_p, top_class = probabilities.topk(1, dim=1)
                    equals = top_class == labels.view(*top_class.shape)
                    accuracy += torch.mean(equals.type(torch.FloatTensor)).item()
            mean_accuracy = accuracy/len(test_batches)
            train_losses.append(total_loss/len(train_batches))
            test_losses.append(test_loss/len(test_batches))
            accuracies.append(mean_accuracy)
            print("Epoch: {}/{}".format(epoch + 1, HyperParameters.epochs),
                  "Training loss: {:.2f}".format(train_losses[-1]),
                  "Test Loss: {:.2f}".format(test_losses[-1]),
                  "Test Accuracy: {:.2f}".format(mean_accuracy)),
    return pandas.DataFrame.from_dict({"Training Loss":train_losses,
                                       "Test Loss": test_losses,
                                       "Test Accuracy": accuracies})
