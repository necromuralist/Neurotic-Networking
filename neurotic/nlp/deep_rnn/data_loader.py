# python
from pathlib import Path

import os

# pypi
from dotenv import load_dotenv

import attr

@attr.s(auto_attribs=True)
class DataLoader:
    """Load the data and convert it to 'tensors'

    Args:
     env_path: the path to the env file (as a string)
     env_key: the environmental variable with the path to the data
     validation_size: number for the validation set
     end_of_sentence: integer to use to indicate the end of a sentence
    """
    env_path: str="posts/nlp/.env"
    env_key: str="SHAKESPEARE"
    validation_size: int=1000
    end_of_sentence: int=1
    _data_path: Path=None
    _lines: list=None
    _training: list=None
    _validation: list=None

    @property
    def data_path(self) -> Path:
        """Loads the dotenv and converts the path
    
        Raises:
         assertion error if path doesn't exist
        """
        if self._data_path is None:
            load_dotenv(self.env_path, override=True)
            self._data_path = Path(os.environ[self.env_key]).expanduser()
            assert self.data_path.is_dir()
        return self._data_path

    @property
    def lines(self) -> list:
        """The lines of text-data"""
        if self._lines is None:
            self._lines = []
            for filename in self.data_path.glob("*.txt"):
                with filename.open() as play:
                    cleaned = (line.strip() for line in play)
                    self._lines += [line.lower() for line in cleaned if line]
        return self._lines

    @property
    def training(self) -> list:
        """Subset of the lines for training"""
        if self._training is None:
            self._training = self.lines[:-self.validation_size]
        return self._training

    @property
    def validation(self) -> list:
        """The validation subset of the lines"""
        if self._validation is None:
            self._validation = self.lines[-self.validation_size:]
        return self._validation

    def to_tensor(self, line: str) -> list:
        """Converts the line to the unicode value
    
        Args:
         line: the text to convert
        Returns:
         line converted to unicode integer encodings
        """
        return [ord(character) for character in line] + [self.end_of_sentence]
