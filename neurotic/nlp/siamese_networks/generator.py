# python
from collections import namedtuple

import random

# pypi
import attr
import numpy

# this project
from neurotic.nlp.siamese_networks import DataLoader, TOKENS


@attr.s(auto_attribs=True)
class DataGenerator:
    """Batch Generator for Quora question dataset

    Args:
     question_one: tensorized question 1
     question_two: tensorized question 2
     batch_size: size of generated batches
     padding: token to use to pad the lists
     shuffle: whether to shuffle the questions around
    """
    question_one: numpy.ndarray
    question_two: numpy.ndarray
    batch_size: int
    padding: int=TOKENS.padding
    shuffle: bool=True
    _batch: iter=None

    

    def data_generator(self):
        """Generator function that yields batches of data
    
        Yields:
            tuple: (batch_question_1, batch_question_2)
        """
        unpadded_1 = []
        unpadded_2 = []
        index = 0
        number_of_questions = len(self.question_one)
        question_indexes = list(range(number_of_questions))
        
        if self.shuffle:
            random.shuffle(question_indexes)
    
        while True:
            if index >= number_of_questions:
                index = 0
                if self.shuffle:
                    random.shuffle(question_indexes)
            
            unpadded_1.append(self.question_one[question_indexes[index]])
            unpadded_2.append(self.question_two[question_indexes[index]])
    
            index += 1
            
            if len(unpadded_1) == self.batch_size:
                max_len = max(max(len(question) for question in unpadded_1),
                              max(len(question) for question in unpadded_2))
                max_len = 2**int(numpy.ceil(numpy.log2(max_len)))
                padded_1 = []
                padded_2 = []
                for question_1, question_2 in zip(unpadded_1, unpadded_2):
                    padded_1.append(question_1 + ((max_len - len(question_1)) * [self.padding]))
                    padded_2.append(question_2 +  ((max_len - len(question_2)) * [self.padding]))
                yield numpy.array(padded_1), numpy.array(padded_2)
                unpadded_1, unpadded_2 = [], []
        return

    @property
    def batch(self):
        """The generator instance"""
        if self._batch is None:
            self._batch = self.data_generator()
        return self._batch

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.batch)
