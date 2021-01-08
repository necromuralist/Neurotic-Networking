# python
import random

# pypi
import attr
import trax.fastmath.numpy as numpy

# this project
from neurotic.nlp.deep_rnn.data_loader import DataLoader

@attr.s(auto_attribs=True)
class DataGenerator:
    """Generates batches

    Args:
     data: lines of data
     data_loader: something with to-tensor method
     batch_size: size of the batches
     max_length: the maximum length for a line (longer lines will be ignored)
     shuffle: whether to shuffle the data
    """
    data: list
    data_loader: DataLoader
    batch_size: int
    max_length: int
    shuffle: bool=True
    _line_count: int= None
    _line_indices: list=None
    _generator: object=None

    @property
    def line_count(self) -> int:
        """Number of lines in the data"""
        if self._line_count is None:
            self._line_count = len(self.data)
        return self._line_count

    @property
    def line_indices(self) -> list:
        """Indices of the lines in the data"""
        if self._line_indices is None:
            self._line_indices = list(range(self.line_count))
        return self._line_indices

    def __iter__(self):
        """A pass-through for this method"""
        return self

    def data_generator(self):
        """Generator method that yields batches of data
    
        Yields:
         (batch, batch, mask)
        """
        index = 0
        current_batch = []
        if self.shuffle:
            random.shuffle(self.line_indices)
        
        while True:
            if index >= self.line_count:
                index = 0
                if self.shuffle:
                    random.shuffle(self._line_indices)
                
            line = self.data[self.line_indices[index]]
            if len(line) < self.max_length:
                current_batch.append(line)
            index += 1
    
            if len(current_batch) == self.batch_size:
                batch = []
                mask = []
                for line in current_batch:
                    tensor = self.data_loader.to_tensor(line)
                    tensor += [0] * (self.max_length - len(tensor))
                    batch.append(tensor)
                    mask.append([int(item != 0) for item in tensor])
                   
                batch = numpy.array(batch)
                yield batch, batch, numpy.array(mask)
                current_batch = []
        return

    @property
    def generator(self):
        """Infinite generator of batches"""
        if self._generator is None:
            self._generator = self.data_generator()
        return self._generator

    def __next__(self):
        """make this an iterator"""
        return next(self.generator)
