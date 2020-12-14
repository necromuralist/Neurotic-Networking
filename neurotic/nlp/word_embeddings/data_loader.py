# python
from pathlib import Path

import os
import re

# pypi
from dotenv import load_dotenv

import attr
import nltk

@attr.s(auto_attribs=True)
class DataCleaner:
    """A cleaner for the word-embeddings data

    Args:
     key: environment key with path to the data file
     env_path: path to the .env file
    """
    key: str="SHAKESPEARE"
    env_path: str="posts/nlp/.env"
    stop: str="."
    _data_path: str=None
    _data: str=None
    _unpunctuated: str=None
    _punctuation: re.Pattern=None
    _tokens: list=None
    _processed: list=None

    @property
    def data_path(self) -> Path:
        """The path to the data file"""
        if self._data_path is None:
            load_dotenv(self.env_path)
            self._data_path = Path(os.environ[self.key]).expanduser()
        return self._data_path

    @property
    def data(self) -> str:
        """The data-file read in as a string"""
        if self._data is None:
            with self.data_path.open() as reader:
                self._data = reader.read()
        return self._data

    @property
    def punctuation(self) -> re.Pattern:
        """The regular expression to find punctuation"""
        if self._punctuation is None:
            self._punctuation = re.compile("[,!?;-]")
        return self._punctuation

    @property
    def unpunctuated(self) -> str:
        """The data with punctuation replaced by stop"""
        if self._unpunctuated is None:
            self._unpunctuated = self.punctuation.sub(self.stop, self.data)
        return self._unpunctuated

    @property
    def tokens(self) -> list:
        """The tokenized data"""
        if self._tokens is None:
            self._tokens = nltk.word_tokenize(self.unpunctuated)
        return self._tokens

    @property
    def processed(self) -> list:
        """The final processed tokens"""
        if self._processed is None:
            self._processed = [token.lower() for token in self.tokens
                               if token.isalpha() or token==self.stop]
        return self._processed

@attr.s(auto_attribs=True)
class MetaData:
    """Compile some basic data about the data

    Args:
     data: the cleaned and tokenized data
    """
    data: list
    _distribution: nltk.probability.FreqDist=None
    _vocabulary: tuple=None
    _word_to_index: dict=None

    @property
    def distribution(self) -> nltk.probability.FreqDist:
        """The Token Frequency Distribution"""
        if self._distribution is None:
            self._distribution = nltk.FreqDist(self.data)
        return self._distribution

    @property
    def vocabulary(self) -> tuple:
        """The sorted unique tokens in the data"""
        if self._vocabulary is None:
            self._vocabulary = tuple(sorted(set(self.data)))
        return self._vocabulary

    @property
    def word_to_index(self) -> dict:
        """Maps words to their index in the vocabulary"""
        if self._word_to_index is None:
            self._word_to_index = {word: index
                                   for index, word in enumerate(self.vocabulary)}
        return self._word_to_index
