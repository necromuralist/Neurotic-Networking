# pypi
import attr

# this repository
from neurotic.nlp.autocorrect.edits import TheEditor


@attr.s(auto_attribs=True)
class WordSuggestor:
    """Suggests Words for Autocorrection

    Args:
     corpus: a Corpus Builder object
     suggestions: number of suggestions to return for each word
     want_switches: also do the =switch= edit
    """
    corpus: object
    suggestions: int=2
    want_switches: bool=True

    def one_letter_edits(self, word: str) -> set:
        """Get all possible words one edit away from the original
    
        Args:
          word: word for which we will generate all possible words one edit away.
    
        Returns:
          set of words with one possible edit.
        """    
        editor = TheEditor(word)
        edits = editor.replaced + editor.inserted + editor.deleted
        if self.want_switches:
            edits += editor.switched
        return set(edits)

    def two_letter_edits(self, word: str) -> set:
        """Make two-letter edits
    
        Args:
          word: the input string/word 
    
        Returns:
          set of strings with all possible two-letter edits
        """
        ones = self.one_letter_edits(word)
        return set.union(*(self.one_letter_edits(one) for one in ones))

    def __call__(self, word: str) -> list:
        """Finds the closest words to the word
    
        If the word is in our corpus then it just returns the word
    
        Args:
         word: potential word to correct
    
        Returns:
         list of (word, probability) tuples
        """
        if word in self.corpus.vocabulary:
            best = [(word, self.corpus.probabilities[word])]
        else:
            suggestions = self.corpus.vocabulary.intersection(self.one_letter_edits(word))
            if not suggestions:
                suggestions = self.corpus.vocabulary.intersection(self.two_letter_edits(word))
            if suggestions:
                probabilities = list(reversed(sorted(
                    [(self.corpus.probabilities.get(suggestion, 0), suggestion)
                     for suggestion in suggestions])))
                best = [(word, probability)
                        for (probability, word) in probabilities[
                                :self.suggestions]]
            else:
                best = [(word, 0)]
        return best
