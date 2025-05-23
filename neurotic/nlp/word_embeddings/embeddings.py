"""This is a module for word embeddings loaders.
"""

# python
from argparse import Namespace
from pathlib import Path

import os
import pickle

# from pypi
from gensim.models.keyedvectors import BaseKeyedVectors, KeyedVectors

import attr
import pandas


@attr.s(auto_attribs=True)
class Embeddings:
    """Embeddings Loader"""
    path: str
    binary: bool
    _embeddings: BaseKeyedVectors=None

    @property
    def embeddings(self) -> BaseKeyedVectors:
        """The loaded embeddings"""
        if self._embeddings is None:
            self._embeddings = KeyedVectors.load_word2vec_format(self.path,
                                                                 binary=self.binary)
        return self._embeddings


@attr.s(auto_attribs=True)
class SubsetBuilder:
    """Create subset of embeddings that matches sets
    
    Args:
     embeddings_1: word embeddings
     embeddings_2: word embeddings
     subset_dict: dict whose keys and values to pull out of the embeddings
     output_1: path to save the first subset to
     output_2: path to save the second subset to
    """
    embeddings_1: KeyedVectors
    embeddings_2: KeyedVectors
    subset_dict: dict
    output_1: Path
    output_2: Path
    
    _vocabulary_1: set=None
    _vocabulary_2: set=None
    _subset_1: dict=None
    _subset_2: dict=None

    @property
    def subset_1(self) -> dict:
        """Subset of embeddings 1"""
        if self._subset_1 is None and self.output_1.is_file():        
            with self.output_1.open("rb") as reader:
                self._subset_1 = pickle.load(reader)
        return self._subset_1

    @property
    def subset_2(self) -> dict:
        """subset of embeddings 2"""
        if self._subset_2 is None and self.output_2.is_file():
            with self.output_2.open("rb") as reader:
                self._subset_2 = pickle.load(reader)
        return self._subset_2

    def pickle_it(self):
        """Save the subsets"""
        if self.subset_1 is not None:
            with self.output_1.open("wb") as writer:
                pickle.dump(self.subset_1, writer)
        if self.subset_2 is not None:
            with self.output_2.open("wb") as writer:
                pickle.dump(self.subset_2, writer)
        return

    def  __call__(self, pickle_it: bool=True) -> None:
        """Builds or loads the subsets and saves them as pickles
    
        Args:
         pickle_it: whether to save the subsets
        """
        if self.subset_1 is None or self.subset_2 is None:
            self.clean()
            self._subset_1, self._subset_2 = {}, {}
            for key, value in self.subset_dict.items():
                if key in self.embeddings_1 and value in self.embeddings_2:
                    self._subset_1[key] = self.embeddings_1[key]
                    self._subset_2[value] = self.embeddings_2[value]
            if pickle_it:
                self.pickle_it()
        return

    def clean(self) -> None:
        """Remove any pickled subsets
    
        Also removes any subset dictionaries
        """
        for path in (self.output_1, self.output_2):
            if path.is_file():
                path.unlink()
        self._subset_1 = self._subset_2 = None
        return


@attr.s(auto_attribs=True)
class DictLoader:
    """Loader for the english and french dictionaries

    This is specifically for the training and testing files
     - CSV-ish (separated by spaces instead of commas)
     - No header: column 1 = English, column 2 = English

    Args:
     path: path to the file
     columns: list of strings
     delimiter: separator for the columns in the source file
    """
    path: str
    columns: list=["English", "French"]
    delimiter: str=" "
    
    _dataframe: pandas.DataFrame=None
    _dictionary: dict=None

    @property
    def dataframe(self) -> pandas.DataFrame:
        """Loads the space-separated file as a dataframe"""
        if self._dataframe is None:
            self._dataframe = pandas.read_csv(self.path,
                                              names=self.columns,
                                              delimiter=self.delimiter)
        return self._dataframe

    @property
    def dictionary(self) -> dict:
        """english to french dictionary"""
        if self._dictionary is None:
            self._dictionary = dict(zip(self.dataframe[self.columns[0]],
                                        self.dataframe[self.columns[1]]))
        return self._dictionary


EmbeddingsKeys = Namespace(
    english_subset="ENGLISH_EMBEDDINGS_SUBSET",
    french_subset="FRENCH_EMBEDDINGS_SUBSET",
    training="ENGLISH_FRENCH_TRAINING",
    testing="ENGLISH_FRENCH_TESTING",
)

SourceKeys = Namespace(
    english="GOOGLE_EMBEDDINGS",
    french="FRENCH_EMBEDDINGS",
    training="ENGLISH_FRENCH_TRAINING",
    testing="ENGLISH_FRENCH_TESTING",
    )


TargetKeys = Namespace(
    english="ENGLISH_EMBEDDINGS_SUBSET",
    french="FRENCH_EMBEDDINGS_SUBSET",
    )


Keys = Namespace(
    source=SourceKeys,
    target=TargetKeys,
    )


@attr.s(auto_attribs=True)
class SourcePaths:
    """Paths to the source files

    These are files provided from other sources
    """
    keys: Namespace=Keys
    _english: Path=None
    _french: Path=None
    _training: Path=None
    _testing: Path=None

    @property
    def english(self) -> Path:
        """Path to the english word-embeddings"""
        if self._english is None:
            self._english = Path(os.environ[self.keys.source.english])
        return self._english

    @property
    def french(self) -> Path:
        """Path to the french word-embeddings"""
        if self._french is None:
            self._french = Path(os.environ[self.keys.source.french])
        return self._french

    @property
    def training(self) -> Path:
        """Path to the training dictionary"""
        if self._training is None:
            self._training = Path(os.environ[self.keys.source.training])
        return self._training

    @property
    def testing(self) -> Path:
        """Path to the testing dictionary"""
        if self._testing is None:
            self._testing = Path(os.environ[self.keys.source.testing])
        return self._testing


@attr.s(auto_attribs=True)
class TargetPaths:
    """Paths to save derived files"""
    keys: Namespace=Keys
    _english: Path=None
    _french: Path=None

    @property
    def english(self) -> Path:
        """Path to derived subset of english embeddings"""
        if self._english is None:
            self._english = Path(os.environ[self.keys.target.english])
        return self._english

    @property
    def french(self) -> Path:
        """Path to derived subset of french embeddings"""
        if self._french is None:
            self._french = Path(os.environ[self.keys.target.french])
        return self._french


@attr.s(auto_attribs=True)
class Paths:
    """Class to build and hold the source and target file paths"""
    _target: Path=None
    _source: Path=None

    @property
    def target(self) -> TargetPaths:
        """Holds object with paths to created embeddings subsets"""
        if self._target is None:
            self._target = TargetPaths()
        return self._target

    @property
    def source(self) -> SourcePaths:
        """Holds objetw with paths to original source files"""
        if self._source is None:
            self._source = SourcePaths()
        return self._source


@attr.s(auto_attribs=True)
class LoadAndBuild:
    """Loads embeddings and dictionaries and builds subsets"""
    _paths: Paths=None
    _english_embeddings: BaseKeyedVectors=None
    _french_embeddings: BaseKeyedVectors=None
    _training: dict=None
    _testing: dict=None
    _merged_dicts: dict=None
    _subset_builder: SubsetBuilder=None

    @property
    def paths(self) -> Paths:
        """Object with paths to files"""
        if self._paths is None:
            self._paths = Paths()
        return self._paths

    @property
    def english_embeddings(self) -> BaseKeyedVectors:
        """Word embeddings for English"""
        if self._english_embeddings is None:
            self._english_embeddings = Embeddings(self.paths.source.english,
                                                  binary=True).embeddings
        return self._english_embeddings

    @property
    def french_embeddings(self) -> BaseKeyedVectors:
        """Word embeddings for French"""
        if self._french_embeddings is None:
            self._french_embeddings = Embeddings(self.paths.source.french,
                                                 binary=False).embeddings
        return self._french_embeddings

    @property
    def training(self) -> dict:
        """training dictionary"""
        if self._training is None:
            self._training = DictLoader(self.paths.source.training).dictionary
        return self._training

    @property
    def testing(self) -> dict:
        """Testing dictionary"""
        if self._testing is None:
            self._testing = DictLoader(self.paths.source.testing).dictionary
        return self._testing

    @property
    def merged_dicts(self) -> dict:
        """Testing and training merged"""
        if self._merged_dicts is None:
            self._merged_dicts = self.training.copy()
            self._merged_dicts.update(self.testing)
            assert len(self._merged_dicts) == (len(self.training) + len(self.testing))
        return self._merged_dicts

    @property
    def subset_builder(self) -> SubsetBuilder:
        """Builder of the subset dictionaries"""
        if self._subset_builder is None:
            self._subset_builder = SubsetBuilder(
                self.english_embeddings,
                self.french_embeddings,
                self.merged_dicts,
                self.paths.target.english,
                self.paths.target.french)
        return self._subset_builder

    def __call__(self) -> None:
        """Calls the subset builder"""
        self.subset_builder()
        return


@attr.s(auto_attribs=True)
class EmbeddingsLoader:
    """Loads the embeddings and dictionaries

    Warning:
     this assumes that you've loaded the proper environment variables to
    find the files - it doesn't call ``load_dotenv``

    """
    _loader_builder: LoadAndBuild=None
    _english_subset: dict=None
    _french_subset: dict=None
    _training: dict=None
    _testing: dict=None

    @property
    def loader_builder(self) -> LoadAndBuild:
        """Object to load sources and build subsets"""
        if self._loader_builder is None:
            self._loader_builder = LoadAndBuild()
        return self._loader_builder

    @property
    def english_subset(self) -> dict:
        """The english embeddings subset
    
        This is a subset of the Google News embeddings that matches the keys in 
        the english to french dictionaries
        """
        if self._english_subset is None:
            if not self.loader_builder.paths.target.english.is_file():
                self.loader_builder()
                self._english_subset = self.loader_builder.subset_builder.subset_1
            else:
                with self.loader_builder.paths.target.english.open("rb") as reader:
                    self._english_subset = pickle.load(reader)
        return self._english_subset

    @property
    def french_subset(self) -> dict:
        """Subset of the MUSE French embeddings"""
        if self._french_subset is None:
            if self.loader_builder.paths.target.french.is_file():
                with self.loader_builder.paths.target.french.open("rb") as reader:
                    self._french_subset = pickle.load(reader)
            else:
                self.loader_builder()
                self._french_subset = self.loader_builder.subset_builder.subset_2
        return self._french_subset

    @property
    def training(self) -> dict:
        """The english to french dictionary training set"""
        if self._training is None:
            self._training = DictLoader(self.loader_builder.paths.source.training).dictionary
        return self._training

    @property
    def testing(self) -> dict:
        """testing english to french dictionary"""
        if self._testing is None:
            self._testing = DictLoader(self.loader_builder.paths.source.testing).dictionary
        return self._testing
