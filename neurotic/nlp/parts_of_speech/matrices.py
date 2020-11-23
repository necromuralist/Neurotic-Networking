# pypi
import attr
import numpy

@attr.s(auto_attribs=True)
class Matrices:
    """The matrices for the hidden markov model

    Args:
     ``transition_counts``: dictionary of counts of adjacent POS tags
     ``emission_counts``: dictionary of (word, POS) counts
     ``tag_counts``: dictionary of POS tag-counts
     ``words``: list of words in the vocabulary
     ``alpha``: The smoothing value
    """
    transition_counts: dict
    emission_counts: dict
    tag_counts: dict
    words: list=attr.ib(converter=sorted)
    alpha: float=0.001
    _tags: list=None
    _tag_count: int=None
    _word_count: int=None
    _transition: numpy.ndarray=None
    _emission: numpy.ndarray=None

    @property
    def tags(self) -> list:
        """Sorted list of the POS tags"""
        if self._tags is None:
            self._tags = sorted(self.tag_counts)
        return self._tags

    @property
    def tag_count(self) -> int:
        """Number of tags"""
        if self._tag_count is None:
            self._tag_count = len(self.tags)
        return self._tag_count

    @property
    def word_count(self) -> int:
        """Number of words in the vocabulary"""
        if self._word_count is None:
            self._word_count = len(self.words)
        return self._word_count

    @property
    def transition(self) -> numpy.ndarray:
        """The Transition Matrix"""
        if self._transition is None:
            self._transition = numpy.zeros((self.tag_count, self.tag_count))
            for row in range(self.tag_count):
                for column in range(self.tag_count):
                    key = (self.tags[row], self.tags[column])
                    count = self.transition_counts[key] if key in self.transition_counts else 0
                    previous_tag_count = self.tag_counts[self.tags[row]]
                    self._transition[row, column] = (
                        (count + self.alpha)
                        /(previous_tag_count + self.alpha * self.tag_count))
        return self._transition

    @property
    def emission(self) -> numpy.ndarray:
        """The Emission Matrix"""
        if self._emission is None:
            self._emission = numpy.zeros((self.tag_count, self.word_count))
            for row in range(self.tag_count):
                for column in range(self.word_count):
                    key = (self.tags[row], self.words[column])
                    emission_count = self.emission_counts[key] if key in self.emission_counts else 0
                    tag_count = self.tag_counts[self.tags[row]]
                    self._emission[row, column] = (
                        (emission_count + self.alpha)
                        /(tag_count + self.alpha * self.word_count)                
                    )
        return self._emission
