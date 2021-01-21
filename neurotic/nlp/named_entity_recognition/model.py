# python
from collections import namedtuple

# pypi
from trax import layers

import attr

Settings = namedtuple("Settings", ["embeddings_size"])
SETTINGS = Settings(50)


@attr.s(auto_attribs=True)
class NER:
    """The named entity recognition model

    Args:
     vocabulary_size: number of tokens in the vocabulary
     tag_count: number of tags
     embeddings_size: the number of features in the embeddings layer
    """
    vocabulary_size: int
    tag_count: int
    embeddings_size: int=SETTINGS.embeddings_size
    _model: layers.Serial=None

    @property
    def model(self) -> layers.Serial:
        """The NER model instance"""
        if self._model is None:
            self._model = layers.Serial(
                layers.Embedding(self.vocabulary_size,
                                 d_feature=self.embeddings_size),
                layers.LSTM(self.embeddings_size),
                layers.Dense(n_units=self.tag_count),
                layers.LogSoftmax()
          )
        return self._model
