# python
from collections import namedtuple
from pathlib import Path

# pypi
import attr
import numpy
import trax

DataDefaults = namedtuple("DataDefaults",
                          ["path",
                           "dataset",
                           "keys",
                           "evaluation_size",
                           "end_of_sentence",
                           "vocabulary_file",
                           "vocabulary_path",
                           "length_keys",
                           "boundaries",
                           "batch_sizes",
                           "padding_token"])

DEFAULTS = DataDefaults(
    path=Path("~/data/tensorflow/translation/").expanduser(),
    dataset="opus/medical",
    keys=("en", "de"),
    evaluation_size=0.01,
    end_of_sentence=1,
    vocabulary_file="ende_32k.subword",
    vocabulary_path="gs://trax-ml/vocabs/",
    length_keys=[0, 1],
    boundaries=[2**power_of_two for power_of_two in range(3, 10)],
    batch_sizes=[2**power_of_two for power_of_two in range(8, 0, -1)],
    padding_token=0,
)

MaxLength = namedtuple("MaxLength", "train evaluate".split())
MAX_LENGTH = MaxLength(train=256, evaluate=512)
END_OF_SENTENCE = 1

def tokenize(input_str: str,
             vocab_file: str=None, vocab_dir: str=None,
             end_of_sentence: int=DEFAULTS.end_of_sentence) -> numpy.ndarray:
    """Encodes a string to an array of integers

    Args:
        input_str: human-readable string to encode
        vocab_file: filename of the vocabulary text file
        vocab_dir: path to the vocabulary file
        end_of_sentence: token for the end of sentence
    Returns:
        tokenized version of the input string
    """
    # The trax.data.tokenize method takes streams and returns streams,
    # we get around it by making a 1-element stream with `iter`.
    inputs =  next(trax.data.tokenize(iter([input_str]),
                                      vocab_file=vocab_file,
                                      vocab_dir=vocab_dir))
    
    # Mark the end of the sentence with EOS
    inputs = list(inputs) + [end_of_sentence]
    
    # Adding the batch dimension to the front of the shape
    batch_inputs = numpy.reshape(numpy.array(inputs), [1, -1])
    return batch_inputs

def detokenize(integers: numpy.ndarray,
               vocab_file: str=None,
               vocab_dir: str=None,
               end_of_sentence: int=DEFAULTS.end_of_sentence) -> str:
    """Decodes an array of integers to a human readable string

    Args:
        integers: array of integers to decode
        vocab_file: filename of the vocabulary text file
        vocab_dir: path to the vocabulary file
        end_of_sentence: token to mark the end of a sentence
    Returns:
        str: the decoded sentence.
    """
    # Remove the dimensions of size 1
    integers = list(numpy.squeeze(integers))
    
    # Remove the EOS to decode only the original tokens
    if end_of_sentence in integers:
        integers = integers[:integers.index(end_of_sentence)] 
    
    return trax.data.detokenize(integers, vocab_file=vocab_file, vocab_dir=vocab_dir)

@attr.s(auto_attribs=True)
class DataGenerator:
    """Generates the streams of data

    Args:
     training: whether this generates training data or not
     path: path to the data set
     data_set: name of the data set (from tensorflow datasets)
     keys: the names of the data
     max_length: longest allowed set of tokens
     evaluation_fraction: how much of the data is saved for evaluation
     length_keys: keys (indexes) to use when setting length
     boundaries: upper limits for batch sizes
     batch_sizes: batch_size for each boundary
     padding_token: which token is used for padding
     vocabulary_file: name of the sub-words vocabulary file
     vocabulary_path: where to find the vocabulary file
     end_of_sentence: token to indicate the end of a sentence
    """
    training: bool=True
    path: Path=DEFAULTS.path
    data_set: str=DEFAULTS.dataset
    keys: tuple=DEFAULTS.keys
    max_length: int=MAX_LENGTH.train
    length_keys: list=DEFAULTS.length_keys
    boundaries: list=DEFAULTS.boundaries
    batch_sizes: list=DEFAULTS.batch_sizes
    evaluation_fraction: float=DEFAULTS.evaluation_size
    vocabulary_file: str=DEFAULTS.vocabulary_file
    vocabulary_path: str=DEFAULTS.vocabulary_path
    padding_token: int=DEFAULTS.padding_token
    end_of_sentence: int=DEFAULTS.end_of_sentence
    _generator_function: type=None
    _batch_generator: type=None

    def end_of_sentence_generator(self, original):
        """Generator that adds end of sentence tokens
    
        Args:
         original: generator to add the end of sentence tokens to
    
        Yields:
         next tuple of arrays with EOS token added
        """
        for inputs, targets in original:
            inputs = list(inputs) + [self.end_of_sentence]
            targets = list(targets) + [self.end_of_sentence]
            yield numpy.array(inputs), numpy.array(targets)
        return 

    @property
    def generator_function(self):
        """Function to create the data generator"""
        if self._generator_function is None:
            self._generator_function = trax.data.TFDS(self.data_set,
                                                      data_dir=self.path,
                                                      keys=self.keys,
                                                      eval_holdout_size=self.evaluation_fraction,
                                                      train=self.training)
        return self._generator_function

    @property
    def batch_generator(self):
        """batch data generator"""
        if self._batch_generator is None:
            generator = self.generator_function()
            generator = trax.data.Tokenize(
                vocab_file=self.vocabulary_file,
                vocab_dir=self.vocabulary_path)(generator)
            generator = self.end_of_sentence_generator(generator)
            generator = trax.data.FilterByLength(
                max_length=self.max_length,
                length_keys=self.length_keys)(generator)
            generator = trax.data.BucketByLength(
                self.boundaries, self.batch_sizes,
                length_keys=self.length_keys
            )(generator)
            self._batch_generator = trax.data.AddLossWeights(
                id_to_mask=self.padding_token)(generator)
        return self._batch_generator
