# from python
from argparse import Namespace

import os
import re
import string

# pypi
import attr

Environment = Namespace(
    training_corpus="WALL_STREET_JOURNAL_POS",
    vocabulary="WALL_STREET_JOURNAL_VOCABULARY",
    test_corpus= "WALL_STREET_JOURNAL_TEST_POS",
    test_words="WALL_STREET_JOURNAL_TEST_WORDS",
)

Suffixes = Namespace(
    noun = ["action", "age", "ance", "cy", "dom", "ee", "ence", "er", "hood",
            "ion", "ism", "ist", "ity", "ling", "ment", "ness", "or", "ry",
            "scape", "ship", "ty"],
    verb = ["ate", "ify", "ise", "ize"],
    adjective = ["able", "ese", "ful", "i", "ian", "ible", "ic", "ish", "ive",
                 "less", "ly", "ous"],
    adverb = ["ward", "wards", "wise"]
)

UNKNOWN = "--unknown-{}--"
Label = Namespace(
    digit=UNKNOWN.format("digit"),
    punctuation=UNKNOWN.format("punctuation"),
    uppercase=UNKNOWN.format("uppercase"),
    noun=UNKNOWN.format("noun"),    
    verb=UNKNOWN.format("verb"),
    adjective=UNKNOWN.format("adjective"),
    adverb=UNKNOWN.format("adverb"),
    unknown="--unknown--"
)

Unknown = Namespace(
    punctuation = set(string.punctuation),
    suffix = Suffixes,
    label=Label,
    has_digit=re.compile(r"\d"),
    has_uppercase=re.compile("[A-Z]")
)


@attr.s(auto_attribs=True)
class DataPreprocessor:
    """A pre-processor for the data

    Args:
     vocabulary: holder of our known words
     empty_token: what to use if a line is an empty string
    """
    vocabulary: dict
    empty_token: str="--n--"

    def handle_empty(self, words: list):
        """replace empty strings withh empty_token
    
        Args:
         words: list to process
         empty_token: what to replace empty strings with
    
        Yields:
         processed words
        """
        for word in words:
            if not word.strip():
                yield self.empty_token
            else:
                yield word
        return

    def label_unknowns(self, words: list) -> str:
        """
        Assign tokens to unknown words
    
        Args:
         word: word not in our vocabulary
         vocabulary: something to check if it is a known word
    
        Yields:
         word or label for the word if unknown
        """
        for word in words:
            if word in self.vocabulary:
                yield word
                
            elif Unknown.has_digit.search(word):
                yield Unknown.label.digit
        
            elif not Unknown.punctuation.isdisjoint(set(word)):
                yield Unknown.label.punctuation
        
            elif Unknown.has_uppercase.search(word):
                yield Unknown.label.uppercase
        
            elif any(word.endswith(suffix) for suffix in Unknown.suffix.noun):
                yield Unknown.label.noun
        
            elif any(word.endswith(suffix) for suffix in Unknown.suffix.verb):
                yield Unknown.label.verb
        
            elif any(word.endswith(suffix) for suffix in Unknown.suffix.adjective):
                yield Unknown.label.adjective
        
            elif any(word.endswith(suffix) for suffix in Unknown.suffix.adverb):
                yield Unknown.label.adverb
            else:
                yield Unknown.label.unknown
        return

    def __call__(self, words: list) -> list:
        """preprocesses the words
    
        Args:
         words: list of words to process
        
        Returns:
         preprocessed version of words
        """
        processed = (word.strip() for word in words)
        processed = self.handle_empty(processed)
        processed = [word for word in self.label_unknowns(processed)]
        return processed


@attr.s(auto_attribs=True)
class DataLoader:
    """Loads the traning and test data

    Args:
     environment: namespace with keys for the environment to load paths
    """
    environment: Namespace
    _preprocess: DataPreprocessor=None
    _vocabulary_words: list=None
    _vocabulary: dict=None
    _training_corpus: list=None
    _test_corpus: list=None
    _test_words: list=None

    @property
    def preprocess(self) -> DataPreprocessor:
        """The Preprocessor for the data"""
        if self._preprocess is None:
            self._preprocess = DataPreprocessor(self.vocabulary)
        return self._preprocess

    @property
    def vocabulary_words(self) -> list:
        """The list of vocabulary words for tranining"""
        if self._vocabulary_words is None:
            self._vocabulary_words = sorted(
                self.load(os.environ[self.environment.vocabulary]))
        return self._vocabulary_words

    @property
    def training_corpus(self) -> list:
        """The corpus  for tranining"""
        if self._training_corpus is None:
            self._training_corpus = self.load(os.environ[self.environment.training_corpus])
        return self._training_corpus

    @property
    def vocabulary(self) -> dict:
        """Converts the vocabulary list of words to a dict
    
        Returns:
         word to index of word in vocabulary words
        """
        if self._vocabulary is None:
            self._vocabulary = {
                word: index
                for index, word in enumerate(self.vocabulary_words)}
        return self._vocabulary

    @property
    def test_corpus(self) -> list:
        """The corpus  for tranining"""
        if self._test_corpus is None:
            self._test_corpus = self.load(os.environ[self.environment.test_corpus])
        return self._test_corpus

    @property
    def test_words(self) -> list:
        """The pre-processed test words"""
        if self._test_words is None:
            self._test_words = self.load(os.environ[self.environment.test_words])
            self._test_words = self.preprocess(self._test_words)
        return self._test_words

    def load(self, path: str) -> list:
        """Loads the strings from the file
    
        Args:
         path: path to the text file
    
        Returns:
         list of lines from the file
        """
        with open(path) as reader:
            lines = reader.read().split("\n")
        return lines
