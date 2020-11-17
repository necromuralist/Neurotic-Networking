# python
from collections import defaultdict, Counter
# pypi
import attr


@attr.s(auto_attribs=True)
class TheTrainer:
    """Trains the POS model

    Args:
     corpus: iterable of word, tag tuples
    """
    corpus: list
    _transition_counts: dict=None
    _emission_counts: dict=None
    _tag_counts: dict=None

    @property
    def transition_counts(self) -> dict:
        """maps previous, next tags to counts"""
        if self._transition_counts is None:
            self._transition_counts = defaultdict(int)
            previous_tag = "--s--"
            for word, tag in self.corpus:
                self._transition_counts[(previous_tag, tag)] += 1
                previous_tag = tag
        return self._transition_counts

    @property
    def emission_counts(self) -> dict:
        """Maps tag, word pairs to counts"""
        if self._emission_counts is None:
            self._emission_counts = Counter(
                ((tag, word) for word, tag in self.corpus)
            )
        return self._emission_counts

    @property
    def tag_counts(self) -> dict:
        """Count of tags"""
        if self._tag_counts is None:
            self._tag_counts = Counter((tag for word, tag in self.corpus))
        return self._tag_counts
