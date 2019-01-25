# from python
from pathlib import Path
from typing import Union
import os

# from pypi
from dotenv import load_dotenv

# this project
from neurotic.base.errors import ConfigurationError

OptionalName = Union[str, None]
OptionalInteger = Union[int, None]


class DataPathDefaults:
    """Some strings for the DataPath"""
    root_folder = "data/"
    depth_below_top_variable = "DEPTH_BELOW_TOP"
    environment_file = ".env"
    sub_folder_key = "SUB_FOLDER"
    top_depth = 0


class DataPath:
    """keeps the paths to the data folders

    Args:
     filename: name of a file in the data folder
     filename_key: key in the environment to grab the filename (if you don't pass in the filename)
     root_folder_name: top-level name of the folder (not sub-folders of data-folder)
     sub_folder_name: path to subfolder with file (but without the root)
     depth_below_top: number of folders below level above the root folder
     depth_key: environment key if we need to grab it
     environment_file: name of the dotenv file if we need it
     check_exists: whether to care if there is a file/folder by that name
    """
    def __init__(self, filename: OptionalName=None,
                 filename_key: OptionalName=None,
                 root_folder_name: str=DataPathDefaults.root_folder,
                 sub_folder_name: OptionalName=None,
                 sub_folder_key: OptionalName=DataPathDefaults.sub_folder_key,
                 depth_below_top: OptionalInteger=None,
                 depth_key: OptionalName=DataPathDefaults.depth_below_top_variable,
                 environment_file: OptionalName=DataPathDefaults.environment_file,
                 check_exists: bool=True,
    ):
        self._filename = filename
        self.filename_key = filename_key
        self.root_folder_name = root_folder_name
        self.sub_folder_name = sub_folder_name
        self.sub_folder_key = sub_folder_key
        self.depth_key = depth_key
        self.environment_file = environment_file
        self.check_exists = check_exists
        self._environment_path = None
        self._depth_below_top = depth_below_top
        self._root = None
        self._folder = None
        self._from_folder = None
        return

    @property
    def environment_path(self) -> Path:
        """The environment file as a =pathlib.Path="""
        if self._environment_path is None:
            self._environment_path = Path(self.environment_file)
        return self._environment_path

    @property
    def filename(self) -> Path:
        """The name of the data file

        Raises:
         ConfigurationError: neither filename nor filename_key were set
        """
        if self._filename is None:
            load_dotenv(dotenv_path=self.environment_path)
            if self.filename_key is None:
                raise ConfigurationError(
                    "Either set the ``filename`` or ``filename_key``")
            self._filename = os.environ.get(self.filename_key)
            if self._filename is None:
                raise ConfigurationError("You need to set up the {}"
                                         " file".format(self.environment_file))
        return self._filename

    @property
    def depth_below_top(self) -> int:
        """Uses .env environment variable to get depth

        Defaults to 0 if neither the environment nor the variable was set
        """
        if self._depth_below_top is None:
            load_dotenv(dotenv_path=self.environment_path)
            self._depth_below_top = int(os.getenv(
                self.depth_key, DataPathDefaults.top_depth))
        return self._depth_below_top            

    @property
    def root(self) -> Path:
        """sets the folder to a Path object
        """
        if self._root is None:
            self._root = Path(self.root_folder_name)
            if self.depth_below_top:
                here, up = Path("."), Path("..")
                for level in range(self.depth_below_top):
                    here = up.joinpath(here)
                self._root = here.joinpath(self._root)
        if self.check_exists:
            self.check_folder(self._root)
        return self._root

    @property
    def from_folder(self) -> Path:
        """the path to the filename in the folder

        Raises:
         ConfigurationError: file doesn't exist in the path
        """
        if self._from_folder is None:
            self._from_folder = self.folder.joinpath(self.filename)
            if self.check_exists:
                self.check_file(self._from_folder)
        return self._from_folder

    @property
    def folder(self) -> Path:
        """The Path to the sub-folder

        If neither the name or the key are set, this clones the root.

        Raises:
         ConfigurationError: environment key set but none found
        """
        if self._folder is None:
            load_dotenv(dotenv_path=self.environment_path)
            if self.sub_folder_key is None:
                self._sub_folder = self.root
            else:
                self._sub_folder = os.environ.get(self.sub_folder_key)
                if self._sub_folder is None:
                    raise ConfigurationError(
                        "You need to set up the {}"
                        " file".format(self.environment_file))
                self._sub_folder = self.root.joinpath(self._sub_folder)
                if self.check_exists:
                    self.check_folder(self._sub_folder)
        return self._sub_folder

    def check_file(self, path: Path) -> None:
        """checks if the path is a file

        Args:
         path: Path to file
        
        Raises:
         ConfigurationError: path doesn't point to a file
        """
        if not path.is_file():
            raise ConfigurationError(
                "'{}' is not a file relative to {}".format(path,
                                                           path.cwd()))
        return

    def check_folder(self, path: Path) -> None:
        """Checks if the path is a folder

        Args:
         path: Path to the folder

        Raises:
         ConfigurationError: path doesn't point to a folder
        """
        if not path.is_dir():
            raise ConfigurationError(
                "'{}' is not a directory relative to {}".format(path,
                                                                path.cwd()))
        return


class DataPathTwo:
    """A less stringent data-path

    This assumes less about the structure and always assumes there's a dotenv file

    Args:
     filename: the name of the file
     folder_key: the key in the .env that points to the folder path
     filename_key: key in the .env for the file if you don't pass it in
     make_folder: if True and folder doesn't exist, make it
     expand_user: expand the '~'
    """
    def __init__(self, filename: str=None,
                 folder_key: str="DATA_PATH",
                 filename_key: str=None,
                 make_folder: bool=True,
                 expand_user: bool=True) -> None:
        self._filename = filename
        self.folder_key = folder_key
        self.filename_key = filename_key
        self.expand_user = expand_user
        self.make_folder = make_folder
        self._folder = None
        self._from_folder = None
        return

    @property
    def filename(self) -> str:
        """The name of the file
        
        Raises:
         ConfigurationError: no name give, dotenv not set up
        """
        if self._filename is None:
            if self.filename_key is None:
                raise ConfigurationError("filename and filename_key not set")
            self.re_load()
            self._filename = os.environ.get(self.filename_key)
            if not self._filename:
                raise ConfigurationError(
                    "'{}' not set in the .env file".format(self.filename_key))
        return self._filename
            

    @property
    def folder(self) -> Path:
        """the path to the folder"""
        if self._folder is None:
            self.re_load()
            self._folder = os.environ.get(self.folder_key)
            if not self._folder:
                raise ConfigurationError(
                    "You need to set the {} in the .env, currently '{}'".format(
                        self.folder_key, self._folder)
                )
            self._folder = Path(self._folder)
            if self.expand_user:
                self._folder = self._folder.expanduser()
            if self.make_folder and not self._folder.is_dir():
                self._folder.mkdir(parents=True)
        return self._folder

    @property
    def from_folder(self) -> Path:
        """The path to the file in the folder"""
        if self._from_folder is None:
            self._from_folder = self.folder.joinpath(self.filename)
        return self._from_folder

    def check_folder(self) -> None:
        """Checks that the folder exists
        
        Raises:
         AssertionError: folder doesn't exist
        """
        assert self.folder.is_dir(), "Folder {} doesn't exist.".format(self.folder)
        return

    def re_load(self):
        """call load_dotenv

        For some reason load_dotenv doesn't always work the first time
        this just exposes it so you don't have to import it
        """
        load_dotenv()
        return


class TrainingTestingValidationPaths:
    """Holds the paths to the folders

    Args:
     train_key: key in the environemnt for the training folder
     test_key: key in the environment for the testing folder
     validation_key: key in the environment for the validation folder
    """
    def __init__(self, train_key="TRAIN", test_key="TEST",
                 validation_key="VALIDATE") -> None:
        load_dotenv()
        self.train_key = train_key
        self.test_key = test_key
        self.validation_key= validation_key
        self._training = None
        self._testing = None
        self._validation = None
        return

    @property
    def training(self) -> DataPathTwo:
        """The path to the training set"""
        if self._training is None:
            self._training = DataPathTwo(folder_key=self.train_key)
        return self._training

    @property
    def testing(self) -> DataPathTwo:
        """path to the testing set"""
        if self._testing is None:
            self._testing = DataPathTwo(folder_key=self.test_key)
        return self._training

    @property
    def validation(self) -> DataPathTwo:
        """path to the validation set"""
        if self._validation is None:
            self._validation = DataPathTwo(folder_key=self.validation_key)
        return self._validation

    def check(self) ->None:
        """Checks that the folders are valid

        Raises: 
         AssertionError: folder doesn't exist
        """
        self.main.check_folder()
        self.training.check_folder()
        self.validation.check_folder()
        self.testing.check_folder()
        return
