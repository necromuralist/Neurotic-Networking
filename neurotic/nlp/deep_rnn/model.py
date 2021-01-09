# from pypi
from trax import layers

import attr




@attr.s(auto_attribs=True)
class GRUModel:
    """Builds the layers for the GRU model

    Args:
     shift_positions: amount of padding to add to the front of input
     vocabulary_size: the size of our learned vocabulary
     model_dimensions: the GRU and Embeddings dimensions
     gru_layers: how many GRU layers to create
     mode: train, eval, or predict
    """
    shift_positions: int=1
    vocabulary_size: int=256
    model_dimensions: int=512
    gru_layers: int=2
    mode: str="train"
    _model: layers.Serial=None

    @property
    def model(self) -> layers.Serial:
        """The GRU Model"""
        if self._model is None:
            self._model = layers.Serial(
                layers.ShiftRight(self.shift_positions, mode=self.mode),
                layers.Embedding(self.vocabulary_size, self.model_dimensions),
                *[layers.GRU(self.model_dimensions)
                  for gru_layer in range(self.gru_layers)],
                layers.Dense(self.vocabulary_size),
                layers.LogSoftmax()
            )
        return self._model
