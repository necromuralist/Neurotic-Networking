# python
from collections import defaultdict, namedtuple
from pathlib import Path

import os

# pypi
from dotenv import load_dotenv
from pathlib import Path

import attr
import nltk
import pandas

nltk.download("punkt")

Tokens = namedtuple("Tokens", ["unknown", "padding", "padding_token"])
TOKENS = Tokens(unknown=0,
                padding=1,
                padding_token="<PAD>")

Question = namedtuple("Question", ["question_one", "question_two"])
Data = namedtuple("Data", ["train", "validate", "test", "y_test"])


@attr.s(auto_attribs=True)
class DataTokenizer:
    """Converts questions to tokens

    Args:
     data: the data-frame to tokenize
    """
    data: pandas.DataFrame
    _question_1: pandas.Series=None
    _question_2: pandas.Series=None

    @property
    def question_1(self) -> pandas.Series:
        """tokenized version of question 1"""
        if self._question_1 is None:
            self._question_1 = self.data.question1.apply(nltk.word_tokenize)
        return self._question_1

    @property
    def question_2(self) -> pandas.Series:
        """tokenized version of question 2"""
        if self._question_2 is None:
            self._question_2 = self.data.question2.apply(nltk.word_tokenize)
        return self._question_2


@attr.s(auto_attribs=True)
class DataTensorizer:
    """Convert tokenized words to numbers

    Args:
     vocabulary: word to integer mapping
     question_1: data to convert
     question_2: other data to convert
    """
    vocabulary: dict
    question_1: pandas.Series
    question_2: pandas.Series
    _tensorized_1: pandas.Series=None
    _tensorized_2: pandas.Series=None

    def to_index(self, words: list) -> list:
        """Convert list of words to list of integers"""
        return [self.vocabulary[word] for word in words]

    @property
    def tensorized_1(self) -> pandas.Series:
        """numeric version of question 1"""
        if self._tensorized_1 is None:
            self._tensorized_1 = self.question_1.apply(self.to_index)
        return self._tensorized_1

    @property
    def tensorized_2(self) -> pandas.Series:
        """Numeric version of question 2"""
        if self._tensorized_2 is None:
            self._tensorized_2 = self.question_2.apply(self.to_index)
        return self._tensorized_2


@attr.s(auto_attribs=True)
class DataLoader:
    """Loads and transforms the data

    Args:
     env: The path to the .env file with the raw-data path
     key: key in the environment with the path to the data
     train_validation_size: number of entries for the training/validation set
     training_fraction: what fraction of the training/valdiation set for training
    """
    env: str="posts/nlp/.env"
    key: str="QUORA_TRAIN"
    train_validation_size: int=300000
    training_fraction: float=0.8
    _data_path: Path=None
    _raw_data: pandas.DataFrame=None
    _training_data: pandas.DataFrame=None
    _testing_data: pandas.DataFrame=None
    _duplicates: pandas.DataFrame=None
    _tokenized_train: DataTokenizer=None
    _tokenized_test: DataTokenizer=None
    _vocabulary: dict=None
    _tensorized_train: DataTensorizer=None
    _tensorized_test: DataTensorizer=None
    _test_labels: pandas.Series=None    
    _data: namedtuple=None

    @property
    def data_path(self) -> Path:
        """Where to find the data file"""
        if self._data_path is None:
            load_dotenv(self.env)
            self._data_path = Path(os.environ[self.key]).expanduser()
        return self._data_path

    @property
    def raw_data(self) -> pandas.DataFrame:
        """The raw-data"""
        if self._raw_data is None:
            self._raw_data = pandas.read_csv(self.data_path)
            self._raw_data = self._raw_data[~self._raw_data.question1.isna()]
            self._raw_data = self._raw_data[~self._raw_data.question2.isna()]        
        return self._raw_data

    @property
    def training_data(self) -> pandas.DataFrame:
        """The training/validation part of the data"""
        if self._training_data is None:
            self._training_data = self.raw_data.iloc[:self.train_validation_size]
        return self._training_data

    @property
    def testing_data(self) -> pandas.DataFrame:
        """The testing portion of the raw data"""
        if self._testing_data is None:
            self._testing_data = self.raw_data.iloc[self.train_validation_size:]
        return self._testing_data

    @property
    def duplicates(self) -> pandas.DataFrame:
        """training-validation data that has duplicate questions"""
        if self._duplicates is None:
            self._duplicates = self.training_data[self.training_data.is_duplicate==1]
        return self._duplicates

    @property
    def tokenized_train(self) -> DataTokenizer:
        """training tokenized    
        """
        if self._tokenized_train is None:
            self._tokenized_train = DataTokenizer(self.duplicates)
        return self._tokenized_train

    @property
    def tokenized_test(self) -> DataTokenizer:
        """Test Tokenizer"""
        if self._tokenized_test is None:
            self._tokenized_test = DataTokenizer(
                self.testing_data)
        return self._tokenized_test

    @property
    def vocabulary(self) -> dict:
        """The token:index map"""
        if self._vocabulary is None:
            self._vocabulary = defaultdict(lambda: TOKENS.unknown)
            self._vocabulary[TOKENS.padding_token] = TOKENS.padding
            combined = (self.tokenized_train.question_1
                        + self.tokenized_train.question_2)
            for index, tokens in combined.iteritems():
                tokens = (token for token in set(tokens)
                          if token not in self._vocabulary)
                for token in tokens:
                    self._vocabulary[token] = len(self._vocabulary) + 1
        return self._vocabulary            

    @property
    def tensorized_train(self) -> DataTensorizer:
        """Tensorizer for the training data"""
        if self._tensorized_train is None:
            self._tensorized_train = DataTensorizer(
                vocabulary=self.vocabulary,
                question_1 = self.tokenized_train.question_1,
                question_2 = self.tokenized_train.question_2,
            )
        return self._tensorized_train

    @property
    def tensorized_test(self) -> DataTensorizer:
        """Tensorizer for the testing data"""
        if self._tensorized_test is None:
            self._tensorized_test = DataTensorizer(
                vocabulary = self.vocabulary,
                question_1 = self.tokenized_test.question_1,
                question_2 = self.tokenized_test.question_2,
            )
        return self._tensorized_test

    @property
    def test_labels(self) -> pandas.Series:
        """The labels for the test data
    
        0 : not duplicate questions
        1 : is duplicate
        """
        if self._test_labels is None:
            self._test_labels = self.testing_data.is_duplicate
        return self._test_labels

    @property
    def data(self) -> namedtuple:
        """The final tensorized data"""
        if self._data is None:
            cut_off = int(len(self.duplicates) * self.training_fraction)
            self._data = Data(
                train=Question(
                    question_one=self.tensorized_train.tensorized_1[:cut_off].to_numpy(),
                    question_two=self.tensorized_train.tensorized_2[:cut_off].to_numpy()),
                validate=Question(
                    question_one=self.tensorized_train.tensorized_1[cut_off:].to_numpy(),
                    question_two=self.tensorized_train.tensorized_2[cut_off:].to_numpy()),
                test=Question(
                    question_one=self.tensorized_test.tensorized_1.to_numpy(),
                    question_two=self.tensorized_test.tensorized_2.to_numpy()),
                y_test=self.test_labels.to_numpy(),
            )
        return self._data
