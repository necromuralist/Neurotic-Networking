from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optimizer
import torchvision.models as models


class Inception:
    """Sets up the model, criterion, and optimizer for the transfer learning
    
    Args:
     classes: number of outputs for the final layer
     device: processor to use
     model_path: path to a saved model
     learning_rate: learning rate for the optimizer
     momentum: momentum for the optimizer
    """
    def __init__(self, classes: int,
                 device: torch.device=None,
                 model_path: str=None,
                 learning_rate: float=0.001, momentum: float=0.9) -> None:
        self.classes = classes
        self.model_path = model_path
        self.learning_rate = learning_rate
        self.momentum = momentum
        self._device = device
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
            for parameter in self._model.parameters():
                parameter.requires_grad = False
            classifier_inputs = self._model.fc.in_features
            self._model.fc = nn.Linear(in_features=classifier_inputs,
                                       out_features=self.classes,
                                       bias=True)
            self._model.to(self.device)
            if self.model_path:
                self._model.load_state_dict(torch.load(self.model_path))
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
            self._optimizer = optimizer.Adam(
                self.model.parameters(),
                lr=self.learning_rate)
        return self._optimizer

    def load_model(self, model_path: Path) -> None:
        """Load a saved model

        Args:
         path: path to the parameters file
        """
        self.model.load_state_dict(torch.load(model_path))
        return
