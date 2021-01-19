# from python
from typing import List, Tuple
import random

# from pypi
import attr
import numpy

Vectors = List[List[int]]
Batch = Tuple[numpy.ndarray]


@attr.s(auto_attribs=True)
class DataGenerator:
    """A generator of data to train the NER Model

    Args:
     batch_size: how many lines to generate at once
     x: the encoded sentences
     y: the encoded labels 
     padding: encoding to use for padding lines
     shuffle: whether to shuffle the data
     verbose: whether to print messages to stdout
    """
    batch_size: int
    x: Vectors
    y: Vectors
    padding: int
    shuffle: bool=False
    verbose: bool=False
    _batch: iter=None

    def batch_generator(self):
        """Generates batches"""
        line_count = len(self.x)
        line_indices = list(range(line_count))
    
        if self.shuffle:
            random.shuffle(line_indices)
        index = 0
        
        while True:
            x_batch = [0] * self.batch_size
            y_batch = [0] * self.batch_size
            longest = 0
            for batch_index in range(self.batch_size):
                if index >= line_count:
                    index = 0
                    if self.shuffle:
                        random.shuffle(line_indices)
                
                x_batch[batch_index] = self.x[line_indices[index]]
                y_batch[batch_index] = self.y[line_indices[index]]
                
                longest = max(longest, len(x_batch[batch_index]))
                index += 1
                
            X = numpy.full((self.batch_size, longest), self.padding)
            Y = numpy.full((self.batch_size, longest), self.padding)
    
            for batch_index in range(self.batch_size): 
                line = x_batch[batch_index]
                label = y_batch[batch_index]
    
                for word in range(len(line)):
                    X[batch_index, word] = line[word]
                    Y[batch_index, word] = label[word]
    
            if self.verbose:
                print("index=", index)
            yield (X,Y)
        return    

    @property
    def batch(self):
        """The instance of the generator"""
        if self._batch is None:
            self._batch = self.batch_generator()
        return self._batch

    def __iter__(self):
        return self

    def __next__(self) -> Batch:
        return next(self.batch)
