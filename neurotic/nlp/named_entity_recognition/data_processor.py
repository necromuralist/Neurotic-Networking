# python
from collections import namedtuple
from functools import partial
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

TheData = namedtuple("TheData", [
    "vocabulary",
    "tags",
    "data_sets",
    "raw_data_sets",
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
class DataFlattener:
    """Converts the kaggle data to sentences and labels

    Args:
     data: the data to convert
    """
    data: pandas.DataFrame
    _sentences: list=None
    _labels: list=None

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
class DataVectorizer:
    """Converts the data-set strings to vectors

    Args:
     data_sets: the split up data sets
     vocabulary: map from token to index
     tags: map from tag to index
    """
    data_sets: namedtuple
    vocabulary: dict
    tags: dict
    _vectorized_datasets: namedtuple=None

    @property
    def vectorized_datasets(self) -> namedtuple:
        """the original data sets converted to indices"""
        if self._vectorized_datasets is None:
            sentence_vectors = partial(self.to_vectors,
                                       to_index=self.vocabulary)
            label_vectors = partial(self.to_vectors,
                                    to_index=self.tags)
            self._vectorized_datasets = DataSets(
                x_train = sentence_vectors(self.data_sets.x_train),
                y_train = label_vectors(self.data_sets.y_train),
                x_validate = sentence_vectors(self.data_sets.x_validate),
                y_validate = label_vectors(self.data_sets.y_validate),
                x_test = sentence_vectors(self.data_sets.x_test),
                y_test = label_vectors(self.data_sets.y_test),
            )
        return self._vectorized_datasets

    def to_vectors(self, source: list, to_index: dict) -> list:
        """Sentences converted to Integers
        
        Args:
         source: iterator of tokenized strings to convert
         to_index: map to convert the tokens to indices
    
        Returns:
         tokens in source converted to indices
        """
        vectors = [
                [to_index.get(token, TOKEN.unknown)
                 for token in line]
                for line in source
            ]
        assert len(vectors) == len(source)
        return vectors


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
class NERData:
    """Master NER Data preparer
    
    Args:
     read_constants: stuff to help load the dataset
     split_constants: stuff to help split the dataset
     random_state: seed for the splitting
    """
    read_constants: namedtuple=READ
    split_constants: namedtuple=SPLIT
    random_state: int=33
    _data: namedtuple=None
    _loader: DataLoader=None
    _flattener: DataFlattener=None
    _splitter: DataSplitter=None
    _vectorizer = DataVectorizer=None

    @property
    def data(self) -> namedtuple:
        """The split up data sets"""
        if self._data is None:
            self._data = TheData(
                vocabulary=self.loader.vocabulary,
                tags=self.loader.tags,
                raw_data_sets=self.splitter.data_sets,
                data_sets=self.vectorizer.vectorized_datasets,
            )
        return self._data

    @property
    def loader(self) -> DataLoader:
        """The loader of the data"""
        if self._loader is None:
            self._loader = DataLoader(
                read=self.read_constants,            
            )
        return self._loader

    @property
    def flattener(self) -> DataFlattener:
        """The sentence and label builder"""
        if self._flattener is None:
            self._flattener = DataFlattener(
                data=self.loader.data,
            )
        return self._flattener

    @property
    def splitter(self) -> DataSplitter:
        """The splitter upper for the data"""
        if self._splitter is None:
            self._splitter = DataSplitter(
                split=self.split_constants,
                sentences = self.flattener.sentences,
                labels = self.flattener.labels,
                random_state=self.random_state
            )
        return self._splitter

    @property
    def vectorizer(self) -> DataVectorizer:
        """Vectorizes the raw-data sets"""
        if self._vectorizer is None:
            self._vectorizer = DataVectorizer(
                data_sets=self.splitter.data_sets,
                tags=self.loader.tags,
                vocabulary=self.loader.vocabulary
            )
        return self._vectorizer
