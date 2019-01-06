# python
from functools import partial

import argparse
import os

# pypi
from dotenv import load_dotenv
from PIL import Image, ImageFile
from torchvision import datasets
import numpy
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optimizer
import torchvision.transforms as transforms

# this project
from neurotic.tangles.data_paths import DataPathTwo
from neurotic.tangles.timer import Timer
from neurotic.constants.imagenet_map import imagenet

# the output won't show up if you don't flush it when redirecting it to a file
print = partial(print, flush=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

ImageFile.LOAD_TRUNCATED_IMAGES = True

load_dotenv()
dog_path = DataPathTwo(folder_key="DOG_PATH")
dog_training_path = DataPathTwo(folder_key="DOG_TRAIN")
dog_testing_path = DataPathTwo(folder_key="DOG_TEST")
dog_validation_path = DataPathTwo(folder_key="DOG_VALIDATE")

human_path = DataPathTwo(folder_key="HUMAN_PATH")

BREEDS = len(set(dog_training_path.folder.iterdir()))
print("Number of Dog Breeds: {}".format(BREEDS))

timer = Timer(beep=SPEAKABLE)

means = [0.485, 0.456, 0.406]
deviations = [0.229, 0.224, 0.225]
IMAGE_SIZE = 224
IMAGE_HALF_SIZE = IMAGE_SIZE//2

train_transform = transforms.Compose([
    transforms.RandomRotation(30),
    transforms.RandomResizedCrop(IMAGE_SIZE),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(means,
                         deviations)])

test_transform = transforms.Compose([transforms.Resize(255),
                                      transforms.CenterCrop(IMAGE_SIZE),
                                      transforms.ToTensor(),
                                      transforms.Normalize(means,
                                                           deviations)])

training = datasets.ImageFolder(root=str(dog_training_path.folder),
                                transform=train_transform)
validation = datasets.ImageFolder(root=str(dog_validation_path.folder),
                                  transform=test_transform)
testing = datasets.ImageFolder(root=str(dog_testing_path.folder),
                               transform=test_transform)

BATCH_SIZE = 10
WORKERS = 0

train_batches = torch.utils.data.DataLoader(training, batch_size=BATCH_SIZE,
                                            shuffle=True, num_workers=WORKERS)
validation_batches = torch.utils.data.DataLoader(
    validation, batch_size=BATCH_SIZE, shuffle=True, num_workers=WORKERS)
test_batches = torch.utils.data.DataLoader(
    testing, batch_size=BATCH_SIZE, shuffle=True, num_workers=WORKERS)

loaders_scratch = dict(train=train_batches,
                       validate=validation_batches,
                       test=test_batches)

LAYER_ONE_OUT = 16
LAYER_TWO_OUT = LAYER_ONE_OUT * 2
LAYER_THREE_OUT = LAYER_TWO_OUT * 2

KERNEL = 3
PADDING = 1
FULLY_CONNECTED_OUT = 500


class Net(nn.Module):
    """Naive Neural Network to classify dog breeds"""
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(3, LAYER_ONE_OUT,
                               KERNEL, padding=PADDING)
        self.conv2 = nn.Conv2d(LAYER_ONE_OUT, LAYER_TWO_OUT,
                               KERNEL, padding=PADDING)
        self.conv3 = nn.Conv2d(LAYER_TWO_OUT, LAYER_THREE_OUT,
                               KERNEL, padding=PADDING)
        # max pooling layer
        self.pool = nn.MaxPool2d(2, 2)
        # linear layer (64 * 4 * 4 -> 500)
        self.fc1 = nn.Linear((IMAGE_HALF_SIZE//4)**2 * LAYER_THREE_OUT, FULLY_CONNECTED_OUT)
        self.fc2 = nn.Linear(FULLY_CONNECTED_OUT, BREEDS)
        # dropout layer (p=0.25)
        self.dropout = nn.Dropout(0.25)
        return

    
    def forward(self, x):
        # add sequence of convolutional and max pooling layers
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))

        x = x.view(-1, (IMAGE_HALF_SIZE//4)**2 * LAYER_THREE_OUT)
        x = self.dropout(x)

        x = self.dropout(F.relu(self.fc1(x)))
        x = self.fc2(x)        
        return x

model_scratch = Net()
if torch.cuda.is_available():
    print("Using {} GPUs".format(torch.cuda.device_count()))
    model_scratch = nn.DataParallel(model_scratch)
model_scratch.to(device)

criterion_scratch = nn.CrossEntropyLoss()

optimizer_scratch = optimizer.SGD(model_scratch.parameters(),
                                  lr=0.001,
                                  momentum=0.9)


def train(epochs: int, train_batches: torch.utils.data.DataLoader,
          validation_batches: torch.utils.data.DataLoader,
          model: nn.Module,
          optimizer: optimizer.SGD,
          criterion: nn.CrossEntropyLoss,
          epoch_start: int=1,
          save_path: str="model_scratch.pt"):
    """Trains the Model

    Args:
     epochs: number of times to train on the data set
     train_batches: the batch-loaders for training
     validation_batches: batch-loaders for validation
     model: the network to train
     optimizer: the gradient descent object
     criterion: object to do backwards propagation
     epoch_start: number to start the epoch count with
     save_path: path to save the best network parameters
    """
    validation_loss_min = numpy.Inf
    end = epoch_start + epochs
    
    for epoch in range(epoch_start, end):
        timer.start()
        training_loss = 0.0
        validation_loss = 0.0
        
        model.train()
        for data, target in train_batches:
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            training_loss += loss.item() * data.size(0)

        model.eval()
        for data, target in validation_batches:
            data, target = data.to(device), target.cuda(device)
            output = model(data)
            loss = criterion(output, target)
            validation_loss += loss.item() * data.size(0)

        training_loss /= len(train_batches.dataset)
        validation_loss /= len(validation_batches.dataset)
            
        timer.end()
        print('Epoch: {} \tTraining Loss: {:.6f} \tValidation Loss: {:.6f}'.format(
            epoch, 
            training_loss,
            validation_loss
            ))
        
        if validation_loss < validation_loss_min:
            print('Validation loss decreased ({:.6f} --> {:.6f}). Saving model ...'.format(
                validation_loss_min,
                validation_loss))
            torch.save(model.state_dict(), save_path)
            validation_loss_min = validation_loss            
    return model


def test(test_batches: torch.utils.data.DataLoader,
         model: nn.Module,
         criterion: nn.CrossEntropyLoss) -> None:
    """Test the model
    
    Args:
     test_batches: batch loader of test images
     model: the network to test
     criterion: calculator for the loss
    """
    test_loss = 0.
    correct = 0.
    total = 0.

    model.eval()
    for data, target in test_batches:
        data, target = data.to(device), target.to(device)
        output = model(data)
        loss = criterion(output, target)
        test_loss += loss.item() * data.size(0)
        # convert output probabilities to predicted class
        predictions = output.data.max(1, keepdim=True)[1]
        # compare predictions to true label
        correct += numpy.sum(
            numpy.squeeze(
                predictions.eq(
                    target.data.view_as(predictions))).cpu().numpy())
        total += data.size(0)
    test_loss /= len(test_batches.dataset)
    print('Test Loss: {:.6f}\n'.format(test_loss))
    print('\nTest Accuracy: %2d%% (%2d/%2d)' % (
        100. * correct / total, correct, total))
    return


def train_and_test(train_batches: torch.utils.data.DataLoader,
                   validate_batches: torch.utils.data.DataLoader,
                   test_batches: torch.utils.data.DataLoader,
                   model: nn.Module,
                   model_path: Path,
                   optimizer: optimizer.SGD,
                   criterion: nn.CrossEntropyLoss,
                   epochs: int=10,
                   epoch_start: int=1,
                   load_model: bool=False) -> None:
    """Trains and Tests the Model

    Args:
     train_batches: batch-loaders for training
     validate_batches: batch-loaders for validation
     test_batches: batch-loaders for testing
     model: the network to train
     model_path: where to save the best model
     optimizer: the gradient descent object
     criterion: object to do backwards propagation
     epochs: number of times to train on the data set
     epoch_start: number to start the epoch count with
     load_model: whether to load the model from a file
    """
    if load_model and model_path.is_file():
        model.load_state_dict(torch.load(model_path))
    print("Starting Training")
    timer.start()
    model_scratch = train(epochs=epochs,
                          epoch_start=epoch_start,
                          train_batches=train_batches,
                          validation_batches=validate_batches,
                          model=model,
                          optimizer=optimizer, 
                          criterion=criterion,
                          save_path=model_path)
    timer.end()
    # load the best model
    model.load_state_dict(torch.load(model_path))
    print("Starting Testing")
    timer.start()
    test(test_batches, model, criterion)
    timer.end()
    return

model_path = DataPathTwo(
    folder_key="MODELS",
    filename="model_scratch.pt")
assert model_path.folder.is_dir()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test or Train the Naive Dog Classifier")
    parser.add_argument("--test", action="store_true",
                        help="Only run the test")
    parser.add_argument("--epochs", default=10, type=int,
                        help="Training epochs (default: %(default)s)")
    parser.add_argument(
        "--epoch-offset", default=0, type=int,
        help="Offset for the output of epochs (default: %(default)s)")
    parser.add_argument("--restart", action="store_true",
                        help="Wipe out old model.")

    arguments = parser.parse_args()
    if arguments.test:
        test(loaders_scratch["test"], model_scratch, criterion_scratch)
    else:
        train_and_test(epochs=arguments.epochs,
                       train_batches=loaders_scratch["train"],
                       validate_batches=loaders_scratch["validate"],
                       test_batches=loaders_scratch["test"],
                       model=model_scratch,
                       optimizer=optimizer_scratch, 
                       criterion=criterion_scratch,
                       epoch_start=arguments.epoch_offset,
                       model_path=model_path.from_folder,
                       load_model=not arguments.restart)
