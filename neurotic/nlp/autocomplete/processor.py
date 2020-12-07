# python
from collections import Counter
from itertools import chain
# from pypi
import attr

@attr.s(auto_attribs=True)
class CountProcessor:
    """Processes the data to have unknowns

    Args:
     training: the tokenized training data (list of lists)
     testing: the tokenized testing data
     count_threshold: minimum number of times token needs to appear
     unknown_token: string to use for words below threshold
    """
    training: list
    testing: list
    count_threshold: int=2
    unknown_token: str="<unk>"
    _counts: dict=None
    _vocabulary: set=None
    _train_unknown: list=None
    _test_unknown: list=None

    @property
    def counts(self) -> Counter:
        """Count of each word in the training data"""
        if self._counts is None:
            self._counts = Counter(chain.from_iterable(self.training))
        return self._counts

    @property
    def vocabulary(self) -> set:
        """The tokens in training that appear at least ``count_threshold`` times"""
        if self._vocabulary is None:
            self._vocabulary = set((token for token, count in self.counts.items()
                                if count >= self.count_threshold))
        return self._vocabulary

    @property
    def train_unknown(self) -> list:
        """Training data with words below threshold replaced"""
        if self._train_unknown is None:
            self._train_unknown = self.parts_unknown(self.training)
        return self._train_unknown

    @property
    def test_unknown(self) -> list:
        """Testing data with words below threshold replaced"""
        if self._test_unknown is None:
            self._test_unknown = self.parts_unknown(self.testing)
        return self._test_unknown

    def parts_unknown(self, source: list) -> list:
        """Replaces tokens in source that aren't in vocabulary
    
        Args:
         source: nested list of lists with tokens to check
        
        Returns: source with unknown words replaced by unknown_token
        """
        return [
                [token if token in self.vocabulary else self.unknown_token
                 for token in tokens]
            for tokens in source
        ]
