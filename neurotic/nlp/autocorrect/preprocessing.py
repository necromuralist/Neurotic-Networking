# python
from collections import Counter
from pathlib import Path

import math
import os
import re

# pypi
import attr


@attr.s(auto_attribs=True)
class CorpusBuilder:
    """Builds the autocorrect corpus counts

    Args:
     path: Path to the corpus source file
    """
    path: Path
    _words: list=None
    _counts: Counter=None
    _probabilities: dict=None

    @property
    def words(self) -> list:
        """
        The processed words from the source file
    
        Returns: 
          words: list of all words in the corpus lower-cased
        """
        if self._words is None:
            with self.path.open() as lines:
                tokenized = (re.findall("\w+", line) for line in lines)
                self._words = [word.strip().lower() for sublist in tokenized for word in sublist]
        return self._words

    @property
    def counts(self) -> Counter:
        """The counter for the words in the corpus
    
        Returns:
         word: word-frequency counter
        """
        if self._counts is None:
            self._counts = Counter(self.words)
        return self._counts

    @property
    def probabilities(self) -> dict:
        """The probability for each word in the corpus
    
        Returns:
         word:probability dictionary
        """
        if self._probabilities is None:
            total = sum(self.counts.values())
            self._probabilities = {word: self.counts[word]/total
                                   for word in self.counts}
        return self._probabilities
