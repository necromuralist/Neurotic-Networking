from abc import (
    ABC,
    abstractproperty,
)

class DataPathDefaults:
    """Holds some constant default values"""
    root_name = "data/"
    levels_below_root = 0

class DataPathBase(ABC):
    """An abstract class for data-path-builders

    Args:
     file_name: the name of the data-file to load
     root_name: name of the top-level data folder
     levels_below_root: the number of levels below the root
    """
    def __init__(
            self,
            file_name: str,
            root_name: str=DataPathDefaults.root_name,
            levels_below_root: int=DataPathDefaults.levels_below_root) -> None:
        return
