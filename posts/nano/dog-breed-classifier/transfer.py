# python
from pathlib import Path
from functools import partial

import argparse

# pypi
from dotenv import load_dotenv
from PIL import ImageFile
from torchvision import datasets
import numpy
import torch
import torch.nn as nn
import torch.optim as optimizer
import torchvision.models as models
import torchvision.transforms as transforms

# this project
from neurotic.tangles.data_paths import DataPathTwo
from neurotic.tangles.timer import Timer

# the output won't show up if you don't flush it when redirecting it to a file
print = partial(print, flush=True)

ImageFile.LOAD_TRUNCATED_IMAGES = True

load_dotenv()
dog_path = DataPathTwo(folder_key="DOG_PATH")
dog_training_path = DataPathTwo(folder_key="DOG_TRAIN")
dog_testing_path = DataPathTwo(folder_key="DOG_TEST")
dog_validation_path = DataPathTwo(folder_key="DOG_VALIDATE")

human_path = DataPathTwo(folder_key="HUMAN_PATH")

BREEDS = len(set(dog_training_path.folder.iterdir()))
print("Number of Dog Breeds: {}".format(BREEDS))


class Trainer:
    """Trains, validates, and tests the model

    Args:
     training_batches: batch-loaders for training
     validation_batches: batch-loaders for validation
     testing_batches: batch-loaders for testing
     model: the network to train
     model_path: where to save the best model
     optimizer: the gradient descent object
     criterion: object to do backwards propagation
     device: where to put the data (cuda or cpu)
     epochs: number of times to train on the data set
     epoch_start: number to start the epoch count with
     load_model: whether to load the model from a file
     beep: whether timer should emit sounds
    """
    def __init__(self,
                 training_batches: torch.utils.data.DataLoader,
                 validation_batches: torch.utils.data.DataLoader,
                 testing_batches: torch.utils.data.DataLoader,
                 model: nn.Module,
                 model_path: Path,
                 optimizer: optimizer.SGD,
                 criterion: nn.CrossEntropyLoss,
                 device: torch.device=None,
                 epochs: int=10,
                 epoch_start: int=1,
                 load_model: bool=False,
                 beep: bool=False) -> None:
        self.training_batches = training_batches
        self.validation_batches = validation_batches
        self.testing_batches = testing_batches
        self.model = model
        self.model_path = model_path
        self.optimizer = optimizer
        self.criterion = criterion
        self.epochs = epochs
        self.beep = beep
        self._epoch_start = None
        self.epoch_start = epoch_start
        self.load_model = load_model
        self._timer = None
        self._epoch_end = None
        self._device = device
        return

    @property
    def epoch_start(self) -> int:
        """The number to start the epoch count"""
        return self._epoch_start

    @epoch_start.setter
    def epoch_start(self, new_start: int) -> None:
        """Sets the epoch start, removes the epoch end"""
        self._epoch_start = new_start
        self._epoch_end = None
        return

    @property
    def device(self) -> torch.device:
        """The device to put the data on"""
        if self._device is None:
            self._device = torch.device("cuda" if torch.cuda.is_available()
                                        else "cpu")
        return self._device

    @property
    def epoch_end(self) -> int:
        """the end of the epochs (not inclusive)"""
        if self._epoch_end is None:
            self._epoch_end = self.epoch_start + self.epochs
        return self._epoch_end

    @property
    def timer(self) -> Timer:
        """something to emit times"""
        if self._timer is None:
            self._timer = Timer(beep=self.beep)
        return self._timer

    def forward(self, batches: torch.utils.data.DataLoader,
                training: bool) -> tuple:
        """runs the forward pass

        Args:
         batches: data-loader
         training: if true, runs the training, otherwise validates
        Returns:
         tuple: loss, correct, total
        """
        forward_loss = 0
        correct = 0

        if training:
            self.model.train()
        else:
            self.model.eval()
        for data, target in batches:
            data, target = data.to(self.device), target.to(self.device)
            if training:
                self.optimizer.zero_grad()
            output = self.model(data)
            loss = self.criterion(output, target)
            if training:
                loss.backward()
                self.optimizer.step()
            forward_loss += loss.item() * data.size(0)

            predictions = output.data.max(1, keepdim=True)[1]
            correct += numpy.sum(
                numpy.squeeze(
                    predictions.eq(
                        target.data.view_as(predictions))).cpu().numpy())
        forward_loss /= len(batches.dataset)
        return forward_loss, correct, len(batches.dataset)

    def train(self) -> tuple:
        """Runs the training

        Returns:
         training loss, correct, count
        """
        return self.forward(batches=self.training_batches, training=True)

    def validate(self) -> tuple:
        """Runs the validation

        Returns:
         validation loss, correct, count
        """
        return self.forward(batches=self.validation_batches, training=False)

    def test(self) -> None:
        """Runs the testing

        """
        self.timer.start()
        self.model.load_state_dict(torch.load(self.model_path))
        loss, correct, total = self.forward(batches=self.testing_batches,
                                            training=False)
        print("Test Loss: {:.3f}".format(loss))
        print("Test Accuracy: {:.2f} ({}/{})".format(100 * correct/total,
                                                     correct, total))
        self.timer.end()
        return

    def train_and_validate(self):
        """Trains and Validates the model
        """
        validation_loss_min = numpy.Inf
        for epoch in range(self.epoch_start, self.epoch_end):
            self.timer.start()
            training_loss, training_correct, training_count = self.train()
            (validation_loss, validation_correct,
             validation_count) = self.validate()
            self.timer.end()
            print(("Epoch: {}\t"
                   "Training - Loss: {:.2f}\t"
                   "Accuracy: {:.2f}\t"
                   "Validation - Loss: {:.2f}\t"
                   "Accuracy: {:.2f}").format(
                       epoch,
                       training_loss,
                       training_correct/training_count,
                       validation_loss,
                       validation_correct/validation_count,
                ))

            if validation_loss < validation_loss_min:
                print(
                    ("Validation loss decreased ({:.6f} --> {:.6f}). "
                     "Saving model ...").format(
                         validation_loss_min,
                         validation_loss))
                torch.save(self.model.state_dict(), self.model_path)
                validation_loss_min = validation_loss
        return

    def __call__(self) -> None:
        """Trains, Validates, and Tests the model"""
        if self.load_model and self.model_path.is_file():
            self.model.load_state_dict(torch.load(self.model_path))
        print("Starting Training")
        self.timer.start()
        self.train_and_validate()
        self.timer.end()
        print("\nStarting Testing")
        self.test()
        return


class Transformer:
    """builds the data-sets

    Args:
     means: list of means for each channel
     deviations: list of standard deviations for each channel
     image_size: size to crop the image to
    """
    def __init__(self,
                 means: list=[0.485, 0.456, 0.406],
                 deviations: list=[0.229, 0.224, 0.225],
                 image_size: int=299) -> None:
        self.means = means
        self.deviations = deviations
        self.image_size = image_size
        self._training = None
        self._testing = None
        return

    @property
    def training(self) -> transforms.Compose:
        """The image transformers for the training"""
        if self._training is None:
            self._training = transforms.Compose([
                transforms.RandomRotation(30),
                transforms.RandomResizedCrop(self.image_size),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize(self.means,
                                     self.deviations)])
        return self._training

    @property
    def testing(self) -> transforms.Compose:
        """Image transforms for the testing"""
        if self._testing is None:
            self._testing = transforms.Compose(
                [transforms.Resize(350),
                 transforms.CenterCrop(self.image_size),
                 transforms.ToTensor(),
                 transforms.Normalize(self.means,
                                      self.deviations)])
        return self._testing


class DataSets:
    """Builds the data-sets

    Args:
     training_path: path to the training set
     validation_path: path to the validation set
     testing_path: path to the test-set
     transformer: object with the image transforms
    """
    def __init__(self, training_path: str, validation_path: str,
                 testing_path: str, transformer: Transformer=None) -> None:
        self.training_path = training_path
        self.validation_path = validation_path
        self.testing_path = testing_path
        self._transformer = transformer
        self._training = None
        self._validation = None
        self._testing = None
        return

    @property
    def transformer(self) -> Transformer:
        """Object with the image transforms"""
        if self._transformer is None:
            self._transformer = Transformer()
        return self._transformer

    @property
    def training(self) -> datasets.ImageFolder:
        """The training data set"""
        if self._training is None:
            self._training = datasets.ImageFolder(
                root=str(self.training_path),
                transform=self.transformer.training)
        return self._training

    @property
    def validation(self) -> datasets.ImageFolder:
        """The validation dataset"""
        if self._validation is None:
            self._validation = datasets.ImageFolder(
                root=str(self.validation_path),
                transform=self.transformer.testing)
        return self._validation

    @property
    def testing(self) -> datasets.ImageFolder:
        """The test set"""
        if self._testing is None:
            self._testing = datasets.ImageFolder(
                root=str(self.testing_path),
                transform=self.transformer.testing)
        return self._testing


class Batches:
    """The data batch loaders

    Args:
     datasets: a data-set builder
     batch_size: the size of each batch loaded
     workers: the number of processes to use
    """
    def __init__(self, datasets: DataSets,
                 batch_size: int=20,
                 workers: int=0) -> None:
        self.datasets = datasets
        self.batch_size = batch_size
        self.workers = workers
        self._training = None
        self._validation = None
        self._testing = None
        return

    @property
    def training(self) -> torch.utils.data.DataLoader:
        """The training batches"""
        if self._training is None:
            self._training = torch.utils.data.DataLoader(
                self.datasets.training,
                batch_size=self.batch_size,
                shuffle=True, num_workers=self.workers)
        return self._training

    @property
    def validation(self) -> torch.utils.data.DataLoader:
        """The validation batches"""
        if self._validation is None:
            self._validation = torch.utils.data.DataLoader(
                self.datasets.validation,
                batch_size=self.batch_size,
                shuffle=True, num_workers=self.workers)
        return self._validation

    @property
    def testing(self) -> torch.utils.data.DataLoader:
        """The testing batches"""
        if self._testing is None:
            self._testing = torch.utils.data.DataLoader(
                self.datasets.testing,
                batch_size=self.batch_size,
                shuffle=True, num_workers=self.workers)
        return self._testing


class Inception:
    """Sets up the model, criterion, and optimizer for the transfer learning

    Args:
     classes: number of outputs for the final layer
     learning_rate: learning rate for the optimizer
     momentum: momentum for the optimizer
    """
    def __init__(self, classes: int=BREEDS,
                 learning_rate: float=0.001, momentum: float=0.9) -> None:
        self.classes = classes
        self.learning_rate = learning_rate
        self.momentum = momentum
        self._device = None
        self._model = None
        self._classifier_inputs = None
        self._criterion = None
        self._optimizer = None
        return

    @property
    def device(self) -> torch.device:
        """Processor to use (cpu or cuda)"""
        if self._device is None:
            self._device = torch.device(
                "cuda" if torch.cuda.is_available() else "cpu")
        return self._device

    @property
    def model(self) -> models.inception_v3:
        """The inception model"""
        if self._model is None:
            self._model = models.inception_v3(pretrained=True)
            self._model.aux_logits = False
            for parameter in self._model.parameters():
                parameter.requires_grad = False
            classifier_inputs = self._model.fc.in_features
            self._model.fc = nn.Linear(in_features=classifier_inputs,
                                       out_features=self.classes,
                                       bias=True)
            self._model.to(self.device)
        return self._model

    @property
    def criterion(self) -> nn.CrossEntropyLoss:
        """The loss callable"""
        if self._criterion is None:
            self._criterion = nn.CrossEntropyLoss()
        return self._criterion

    @property
    def optimizer(self) -> optimizer.SGD:
        """The Gradient Descent object"""
        if self._optimizer is None:
            self._optimizer = optimizer.SGD(
                self.model.parameters(),
                lr=self.learning_rate,
                momentum=self.momentum)
        return self._optimizer


transfer_path = DataPathTwo(
    folder_key="MODELS",
    filename="model_transfer.pt")
assert transfer_path.folder.is_dir()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test or Train the Inception V3 Dog Classifier")
    parser.add_argument("--test-only", action="store_true",
                        help="Only run the test")
    parser.add_argument("--epochs", default=10, type=int,
                        help="Training epochs (default: %(default)s)")
    parser.add_argument(
        "--epoch-offset", default=1, type=int,
        help="Offset for the output of epochs (default: %(default)s)")
    parser.add_argument("--restart", action="store_true",
                        help="Wipe out old model.")

    arguments = parser.parse_args()

    data_sets = DataSets(training_path=dog_training_path.folder,
                         validation_path=dog_validation_path.folder,
                         testing_path=dog_testing_path.folder)
    batches = Batches(datasets=data_sets)
    inception = Inception()
    trainer = Trainer(epochs=arguments.epochs,
                      training_batches=batches.training,
                      validation_batches=batches.validation,
                      testing_batches=batches.testing,
                      model=inception.model,
                      device=inception.device,
                      optimizer=inception.optimizer,
                      criterion=inception.criterion,
                      model_path=transfer_path.from_folder,
                      load_model=True,
                      beep=False)
    if arguments.test_only:
        trainer.test()
    else:
        trainer()
