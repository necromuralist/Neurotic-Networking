# python
from pathlib import Path

# from pypi
from trax.supervised import training

import attr
import trax
import trax.layers as trax_layers


@attr.s(auto_attribs=True)
class SentimentNetwork:
    """Builds and Trains the Sentiment Analysis Model

    Args:
     training_generator: generator of training batches
     validation_generator: generator of validation batches
     vocabulary_size: number of tokens in the training vocabulary
     training_loops: number of times to run the training loop
     output_path: path to where to store the model
     embedding_dimension: output dimension for the Embedding layer
     output_dimension: dimension for the Dense layer
    """
    vocabulary_size: int
    training_generator: object
    validation_generator: object
    training_loops: int
    output_path: Path
    embedding_dimension: int=256
    output_dimension: int=2
    _model: trax_layers.Serial=None
    _training_task: training.TrainTask=None
    _evaluation_task: training.EvalTask=None
    _training_loop: training.Loop=None

    @property
    def model(self) -> trax_layers.Serial:
        """The Embeddings model"""
        if self._model is None:
            self._model = trax_layers.Serial(
                trax_layers.Embedding(
                    vocab_size=self.vocabulary_size,
                    d_feature=self.embedding_dimension),
                trax_layers.Mean(axis=1),
                trax_layers.Dense(n_units=self.output_dimension),
                trax_layers.LogSoftmax(),
            )
        return self._model

    @property
    def training_task(self) -> training.TrainTask:
        """The training task for training the model"""
        if self._training_task is None:
            self._training_task = training.TrainTask(
                labeled_data=self.training_generator,
                loss_layer=trax_layers.CrossEntropyLoss(),
                optimizer=trax.optimizers.Adam(0.01),
                n_steps_per_checkpoint=10,
            )
        return self._training_task

    @property
    def evaluation_task(self) -> training.EvalTask:
        """The validation evaluation task"""
        if self._evaluation_task is None:
            self._evaluation_task = training.EvalTask(
                labeled_data=self.validation_generator,
                metrics=[trax_layers.CrossEntropyLoss(),
                         trax_layers.Accuracy()],
            )
        return self._evaluation_task

    @property
    def training_loop(self) -> training.Loop:
        """The thing to run the training"""
        if self._training_loop is None:
            self._training_loop = training.Loop(
                model=self.model,
                tasks=self.training_task,
                eval_tasks=self.evaluation_task,
                output_dir= self.output_path) 
        return self._training_loop

    def fit(self):
        """Runs the training loop"""
        self.training_loop.run(n_steps=self.training_loops)
        return
