# from python
from pathlib import Path

# from pypi
import numpy
import torch
import torch.nn as nn
import torch.optim as optimizer

# this project
from neurotic.tangles.logging import Tee
from neurotic.tangles.timer import Timer


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
     training_log: something to send the output to during training
     testing_log: something to send the output to during testing
     is_inception: expect two outputs in training
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
                 is_inception: bool=False,
                 load_model: bool=False,
                 beep: bool=False,
                 training_log: Tee=None,
                 testing_log: Tee=None,
    ) -> None:
        self.training_batches = training_batches
        self.validation_batches = validation_batches
        self.testing_batches = testing_batches
        self.model = model
        self.model_path = model_path
        self.optimizer = optimizer
        self.criterion = criterion
        self.epochs = epochs
        self.is_inception = is_inception
        self.beep = beep
        self.training_log = training_log if training_log else print
        self.testing_log = testing_log if testing_log else print
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
            if training and self.is_inception:
                # throw away the auxiliary output
                output, _ = self.model(data)
            else:
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
        with self.timer:
            self.model.load_state_dict(torch.load(self.model_path))
            loss, correct, total = self.forward(batches=self.testing_batches,
                                                training=False)
            self.testing_log("Test Loss: {:.3f}".format(loss))
            self.testing_log("Test Accuracy: {:.2f} ({}/{})".format(100 * correct/total,
                                                                    correct, total))
        return

    def train_and_validate(self):
        """Trains and Validates the model
        """
        validation_loss_min = numpy.Inf
        for epoch in range(self.epoch_start, self.epoch_end):
            with self.timer:
                training_loss, training_correct, training_count = self.train()
                (validation_loss, validation_correct,
                 validation_count) = self.validate()

            self.training_log(("Epoch: {}\t"
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
                self.training_log(
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
        self.training_log("Starting Training")
        with self.timer:
            self.train_and_validate()
        self.testing_log("\nStarting Testing")
        self.test()
        return
