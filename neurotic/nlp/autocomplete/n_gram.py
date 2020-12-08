# python
from collections import Counter
from itertools import chain

# pypi
import attr

@attr.s(auto_attribs=True)
class NGrams:
    """The N-Gram Language Model

    Args:
     data: the training data
     n: the size of the n-grams
     start_token: string to represent the start of a sentence
     end_token: string to represent the end of a sentence
    """
    data: list
    n: int
    start_token: str="<s>"
    end_token: str="<e>"
    _start_tokens: list=None
    _end_tokens: list=None
    _sentences: list=None
    _n_grams: list=None
    _counts: dict=None

    @property
    def start_tokens(self) -> list:
        """List of 'n' start tokens"""
        if self._start_tokens is None:
            self._start_tokens = [self.start_token] * self.n
        return self._start_tokens

    @property
    def end_tokens(self) -> list:
        """List of 1 end-tokens"""
        if self._end_tokens is None:
            self._end_tokens = [self.end_token]
        return self._end_tokens

    @property
    def sentences(self) -> list:
        """The data augmented with tags and converted to tuples"""
        if self._sentences is None:
            self._sentences = [tuple(self.start_tokens + sentence + self.end_tokens)
                               for sentence in self.data]
        return self._sentences

    @property
    def n_grams(self) -> list:
        """The n-grams from the data
    
        Warning:
         this flattens the n-grams so there isn't any sentence structure
        """
        if self._n_grams is None:
            self._n_grams = chain.from_iterable([
                [sentence[cut: cut + self.n] for cut in range(0, len(sentence) - (self.n - 1))]
                for sentence in self.sentences
            ])
        return self._n_grams

    @property
    def counts(self) -> Counter:
        """A count of all n-grams in the data
    
        Returns:
            A dictionary that maps a tuple of n-words to its frequency
        """
        if self._counts is None:        
            self._counts = Counter(self.n_grams)
        return self._counts


@attr.s(auto_attribs=True)
class NGramProbability:
    """Probability model for n-grams

    Args:
     data: the source for the n-grams
     n: the size of the n-grams
     k: smoothing factor
     augment_vocabulary: hack because the two probability functions use different vocabularies
    """
    data: list
    n: int
    k: float=1.0
    augment_vocabulary: bool=True
    _n_grams: NGrams=None
    _n_plus_one: NGrams=None
    _vocabulary: set=None
    _vocabulary_size: int=None
    _probabilities: dict=None

    @property
    def n_grams(self) -> NGrams:
        if self._n_grams is None:
            self._n_grams = NGrams(data=self.data, n=self.n)
        return self._n_grams

    @property
    def n_plus_one(self) -> NGrams:
        """N+1 Grams"""
        if self._n_plus_one is None:
            self._n_plus_one = NGrams(data=self.data, n=self.n + 1)
        return self._n_plus_one

    @property
    def vocabulary(self) -> set:
        """Unique words in the dictionary"""
        if self._vocabulary is None:
            data = list(chain.from_iterable(self.data)).copy()
            if self.augment_vocabulary:
                data += ["<e>", "<unk>"]
            self._vocabulary = set(data)
        return self._vocabulary

    @property
    def vocabulary_size(self) -> int:
        """Number of unique tokens in the data"""
        if self._vocabulary_size is None:
            self._vocabulary_size = len(self.vocabulary)
        return self._vocabulary_size

    def probability(self, word: str, previous_n_gram: tuple) -> float:
        """Calculates the probability of the word given the previous n-gram"""
        # just in case it's a list
        previous_n_gram = tuple(previous_n_gram)
        previous_n_gram_count = self.n_grams.counts.get(previous_n_gram, 0)
        denominator = previous_n_gram_count + self.k * self.vocabulary_size
        
        n_plus1_gram = previous_n_gram + (word,)
        n_plus1_gram_count = self.n_plus_one.counts.get(n_plus1_gram, 0)
        numerator = n_plus1_gram_count + self.k
        return numerator/denominator

    def probabilities(self, previous_n_gram: tuple) -> dict:
        """Finds the probability of each word in the vocabulary
    
        Args:
         previous_n_gram: the preceding tuple to calculate probabilities
    
        Returns:
         word:<probability word follows previous n-gram> for the vocabulary
        """
        previous_n_gram = tuple(previous_n_gram)
        return {word: self.probability(word=word, previous_n_gram=previous_n_gram)
                for word in self.vocabulary}
