# python
from string import ascii_lowercase
# from pypi
import attr


@attr.s(auto_attribs=True)
class TheEditor:
    """Does various edits to words

    Args:
     word: string to edit
    """
    word: str
    _splits: list=None
    _deleted: list=None
    _switched: list=None
    _replaced: list=None
    _inserted: list=None

    @property
    def splits(self) -> list:
        """Tuples of splits for word"""
        if self._splits is None:
            self._splits = [(self.word[:index], self.word[index:])
                            for index in range(len(self.word) + 1)]
        return self._splits

    @property
    def deleted(self) -> list:
        """Deletes one letter at a time from the word
    
        Returns:
         list of all possible strings created by deleting one letter
        """
        if self._deleted is None:
            self._deleted = [left + right[1:]
                             for left, right in self.splits if right]
        return self._deleted

    @property
    def switched(self) -> list:
        """switches one letter pair at a time
    
        Returns:
         all possible strings with one adjacent charater switched
        """
        if self._switched is None:
            self._switched = [left[:-1] + right[0] + left[-1] + right[1:]
                              for left, right in self.splits
                              if left and right]
        return self._switched

    @property
    def replaced(self) -> list:
        """Replace each letter with every other letter of the alphabet
    
        Returns:
         replacements in alphabetical order (doesn't include original word)
        """
        if self._replaced is None:
            self._replaced = set([left + letter + right[1:]
                                  for left, right in self.splits if right
                                  for letter in ascii_lowercase])
            self._replaced.discard(self.word)
            self._replaced = sorted(list(self._replaced))
        return self._replaced

    @property
    def inserted(self) -> list:
        """Adds letters before and after each letter
    
        Returns:
          all possible strings with one new letter inserted at every offset
        """
        if self._inserted is None:
            self._inserted = [left + letter + right
                              for left, right in self.splits
                              for letter in ascii_lowercase]
        return self._inserted
