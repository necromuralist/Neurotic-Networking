# python
from collections import namedtuple
from pathlib import Path

import os

# pypi
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

import attr
import pandas

Read = namedtuple("Read", "dotenv key encoding".split())
READ = Read(dotenv="posts/nlp/.env", key="NER_DATASET",
            encoding="ISO-8859-1")

COLUMNS={"Sentence #":"sentence",
         "Word": "word",
         "Tag": "tag"}

Token = namedtuple("Token", "pad unknown".split())
TOKEN = Token(pad="<PAD>", unknown="UNK")

Splits = namedtuple("Split", "train validation test".split())
SPLIT = Splits(train=33570, validation=7194, test=7194)

DataSets = namedtuple("DataSets", [
    "x_train",
    "y_train",
    "x_validate",
    "y_validate",
    "x_test",
    "y_test"
])


@attr.s(auto_attribs=True)
class DataSplitter:
    """Splits up the training, testing, etc.

    Args:
     split: constants with the train, test counts
     sentences: input data to split
     labels: y-data to split
     random_state: seed for the splitting
    """
    split: namedtuple
    sentences: list
    labels: list    
    random_state: int=None
    _data_sets: namedtuple=None

    @property
    def data_sets(self) -> namedtuple:
        """The Split data sets"""
        if self._data_sets is None:
            x_train, x_leftovers, y_train, y_leftovers = train_test_split(
                self.sentences, self.labels,
                train_size=self.split.train,
                random_state=self.random_state)
            x_validate, x_test, y_validate, y_test = train_test_split(
                x_leftovers,
                y_leftovers,
                test_size=self.split.test,
                random_state=self.random_state)
            self._data_sets = DataSets(x_train=x_train,
                                       y_train=y_train,
                                       x_validate=x_validate,
                                       y_validate=y_validate,
                                       x_test=x_test,
                                       y_test=y_test,
                                       )
            assert len(x_train) + len(x_validate) + len(x_test) == len(self.sentences)
        return self._data_sets


@attr.s(auto_attribs=True)
class DataTransformer:
    """Converts a dataset to vectors

    Since this might process the validation and test sets
    pass in the vocabulary and tags explicitly

    Args:
     data: the data to convert
     vocabulary: map from word to index
     tags: map from tag to index
    """
    data: pandas.DataFrame
    vocabulary: dict
    tags: dict
    _sentences: list=None
    _labels: list=None
    _sentence_vectors: list=None
    _label_vectors: list=None

    @property
    def sentences(self) -> list:
        """List of sentences from the data"""
        if self._sentences is None:
            self.set_sentences_and_labels()
        return self._sentences

    @property
    def labels(self) -> list:
        """List of labels from the data"""
        if self._labels is None:
            self.set_sentences_and_labels()
        return self._labels

    @property
    def sentence_vectors(self) -> list:
        """Sentences converted to Integers"""
        if self._sentence_vectors is None:
            self._sentence_vectors = [
                [self.vocabulary.get(word, TOKEN.unknown)
                 for word in sentence]
                for sentence in self.sentences
            ]
            assert len(self._sentence_vectors) == len(self.sentences)
        return self._sentence_vectors

    @property
    def label_vectors(self) -> list:
        """Labels converted to integer-lists"""
        if self._label_vectors is None:
            self._label_vectors = [
                [self.tags.get(label, TOKEN.unknown)
                 for label in sentence_labels]
                for sentence_labels in self.labels
            ]
            assert len(self._label_vectors) == len(self.labels)
        return self._label_vectors

    def set_sentences_and_labels(self) -> None:
        """Converts the data to lists
        of sentence token lists and also sets the labels
        """
        self._sentences = []
        self._labels = []
        sentence = None
        for row in self.data.itertuples():
            if not pandas.isna(row.sentence):
                if sentence:
                    self._sentences.append(sentence)
                    self._labels.append(labels)
                sentence = [row.word]
                labels = [row.tag]
            else:
                sentence.append(row.word)
                labels.append(row.tag)
        return


@attr.s(auto_attribs=True)
class DataLoader:
    """Loads and converts the kaggle data

    Args:
      read: the stuff to download the data
    """
    read: namedtuple=READ    
    _data: pandas.DataFrame=None
    _vocabulary: dict=None
    _tags: dict=None

    @property
    def data(self) -> pandas.DataFrame:
        """The original kaggle dataset"""
        if self._data is None:
            load_dotenv(self.read.dotenv)
            path = Path(os.environ[self.read.key]).expanduser()
            self._data = pandas.read_csv(path, encoding=self.read.encoding)
            self._data = self._data.rename(columns=COLUMNS)
        return self._data

    @property
    def vocabulary(self) -> dict:
        """map of word to index
    
        Note:
          This is creating a transformation of the entire data-set
        so it comes before the train-test-split so it uses the whole
        dataset, not just training
        """
        if self._vocabulary is None:
            self._vocabulary = {
                word: index
                for index, word in enumerate(self.data.word.unique())}
            self._vocabulary[TOKEN.pad] = len(self._vocabulary)
            self._vocabulary[TOKEN.unknown] = len(self._vocabulary)
        return self._vocabulary

    @property
    def tags(self) -> dict:
        """map of tag to index"""
        if self._tags is None:
            self._tags = {tag: index for index, tag in enumerate(
                self.data.tag.unique())}
            self._tags[TOKEN.unknown] = len(self._tags)
        return self._tags


@attr.s(auto_attribs=True)
class TheData:
    """Data pre-processor
    
    Args:
     read_constants: stuff to help load the dataset
     split_constants: stuff to help split the dataset
     random_state: seed for the splitting
    """
    read_constants: namedtuple=READ
    split_constants: namedtuple=SPLIT
    random_state: int=33
    _data_sets: namedtuple=None
    _loader: DataLoader=None
    _transformer: DataTransformer=None
    _splitter: DataSplitter=None

    @property
    def data_sets(self) -> namedtuple:
        """The split up data sets"""
        if self._data_sets is None:
            self._data_sets = self.splitter.data_sets
        return self._data_sets

    @property
    def loader(self) -> DataLoader:
        """The loader of the data"""
        if self._loader is None:
            self._loader = DataLoader(
                read=self.read_constants,            
            )
        return self._loader

    @property
    def transformer(self) -> DataTransformer:
        """The sentence and label builder"""
        if self._transformer is None:
            self._transformer = DataTransformer(
                data=self.loader.data,
                vocabulary=self.loader.vocabulary,
                tags=self.loader.tags,
            )
        return self._transformer

    @property
    def splitter(self) -> DataSplitter:
        """The splitter upper for the data"""
        if self._splitter is None:
            self._splitter = DataSplitter(
                split=self.split_constants,
                sentences = self.transformer.sentence_vectors,
                labels = self.transformer.label_vectors,
                random_state=self.random_state
            )
        return self._splitter
