# pypi
from tabulate import tabulate

import attr
import numpy
import pandas

@attr.s(auto_attribs=True)
class MinimumEdits:
    """Calculates the minimum edit distance between two strings

    Uses the Levenshtein distance

    Args:
     source: the starting string
     target: what to transform the source to
     insertion_cost: how much inserting a character costs
     deletion_cost: how much deleting a character costs
     replacement_cost: how much swapping out a character costs
     table_format: tabluate table format for printing table
    """
    source: str
    target: str
    insertion_cost: int=1
    deletion_cost: int=1
    replacement_cost: int=2
    table_format: str="orgtbl"
    _rows: int=None
    _columns: int=None
    _distance_table: numpy.ndarray=None
    _distance_frame: pandas.DataFrame=None
    _minimum_distance: int=None
    _backtrace: list=None

    @property
    def rows(self) -> int:
        """Rows in the table"""
        if self._rows is None:
            self._rows = len(self.source)
        return self._rows

    @property
    def columns(self) -> int:
        """Number of columns for the table"""
        if self._columns is None:
            self._columns = len(self.target)
        return self._columns

    @property
    def distance_table(self) -> numpy.ndarray:
        """Table of edit distances"""
        if self._distance_table is None:
            self._distance_table = numpy.zeros((self.rows + 1, self.columns + 1),
                                               dtype=int)
            # initialize the first row
            for row in range(1, self.rows + 1):
                self._distance_table[row, 0] = (self._distance_table[row - 1, 0]
                                                + self.deletion_cost)
            # initialize the first column
            for column in range(1, self.columns + 1):
                self._distance_table[0, column] = (self._distance_table[0, column-1]
                                                   + self.insertion_cost)
            
            for row in range(1, self.rows + 1):
                one_row_back = row - 1
                for column in range(1, self.columns + 1):
                    one_column_back = column - 1
                    replacement_cost = (
                        0 if self.source[one_row_back] == self.target[one_column_back]
                        else self.replacement_cost)
                    self._distance_table[row, column] = min(
                        (self._distance_table[one_row_back, column]
                         + self.deletion_cost),
                         (self._distance_table[row, one_column_back]
                          + self.insertion_cost),
                        (self._distance_table[one_row_back, one_column_back]
                         + replacement_cost))
        return self._distance_table

    @property
    def distance_frame(self) -> pandas.DataFrame:
        """pandas dataframe of the distance table"""
        if self._distance_frame is None:
            self._distance_frame = pandas.DataFrame(
                self.distance_table,
                index= list("#" + self.source),
                columns = list("#" + self.target),
            )
        return self._distance_frame

    @property
    def minimum_distance(self) -> int:
        """The minimum edit distance from source to target"""
        if self._minimum_distance is None:
            self._minimum_distance = self.distance_table[
                self.rows, self.columns]
        return self._minimum_distance

    def __str__(self) -> str:
        """tabluate version of distance frame
    
        Returns:
         table formatted string of distance table
        """
        return tabulate(self.distance_frame, headers="keys", tablefmt=self.table_format)
