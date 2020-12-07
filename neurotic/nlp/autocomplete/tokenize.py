# python
import random

# pypi
import attr
import nltk


@attr.s(auto_attribs=True)
class Tokenizer:
    """Tokenizes string sentences

    Args:
     source: string data to tokenize
     end_of_sentence: what to split sentences on

    """
    source: str
    end_of_sentence: str="\n"
    _sentences: list=None
    _tokenized: list=None
    _training_data: list=None

    @property
    def sentences(self) -> list:
        """The data split into sentences"""
        if self._sentences is None:
            self._sentences = self.source.split(self.end_of_sentence)
            self._sentences = (sentence.strip() for sentence in self._sentences)
            self._sentences = [sentence for sentence in self._sentences if sentence]
        return self._sentences

    @property
    def tokenized(self) -> list:
        """List of tokenized sentence"""
        if self._tokenized is None:
            self._tokenized = [nltk.word_tokenize(sentence.lower())
                               for sentence in self.sentences]
        return self._tokenized


@attr.s(auto_attribs=True)
class TrainTestSplit:
    """splits up the training and testing sets

    Args:
     data: list of data to split
     training_fraction: how much to put in the training set
     seed: something to seed the random call
    """
    data: list
    training_fraction: float=0.8
    seed: int=87
    _shuffled: list=None
    _training: list=None
    _testing: list=None
    _split: int=None

    @property
    def shuffled(self) -> list:
        """The data shuffled"""
        if self._shuffled is None:
            random.seed(self.seed)
            self._shuffled = random.sample(self.data, k=len(self.data))
        return self._shuffled

    @property
    def training(self) -> list:
        """The Training Portion of the Set"""
        if self._training is None:
            self._training = self.shuffled[0:self.split]
        return self._training

    @property
    def testing(self) -> list:
        """The testing data"""
        if self._testing is None:
            self._testing = self.shuffled[self.split:]
        return self._testing

    @property
    def split(self) -> int:
        """The slice value for training and testing"""
        if self._split is None:
            self._split = int(len(self.data) * self.training_fraction)
        return self._split
