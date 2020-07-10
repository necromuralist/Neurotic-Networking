# python
import re
import string

# pypi
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer

import attr
import nltk

class WheatBran:
    """This is a holder for the regular expressions"""
    START_OF_LINE = r"^"
    OPTIONAL = "{}?"
    ANYTHING = "."
    ZERO_OR_MORE = "{}*"
    ONE_OR_MORE = "{}+"
    ONE_OF_THESE = "[{}]"

    SPACE = r"\s"
    SPACES = ONE_OR_MORE.format(SPACE)
    PART_OF_A_WORD = r"\w"
    EVERYTHING_OR_NOTHING = ZERO_OR_MORE.format(ANYTHING)

    ERASE = ""
    FORWARD_SLASHES = r"\/\/"
    NEWLINES = ONE_OF_THESE.format(r"\r\n")
    # a dollar is a special regular expression character meaning end of line
    # so escape it
    DOLLAR_SIGN = r"\$"

    # to remove
    STOCK_SYMBOL = DOLLAR_SIGN + ZERO_OR_MORE.format(PART_OF_A_WORD)
    RE_TWEET = START_OF_LINE + "RT" + SPACES
    HYPERLINKS = ("http" + OPTIONAL.format("s") + ":" + FORWARD_SLASHES
                  + EVERYTHING_OR_NOTHING + ZERO_OR_MORE.format(NEWLINES))
    HASH = "#"

    remove = [STOCK_SYMBOL, RE_TWEET, HYPERLINKS, HASH]


@attr.s
class TwitterProcessor:
    """processor for tweets"""
    _tokenizer = attr.ib(default=None)
    _stopwords = attr.ib(default=None)
    _stemmer = attr.ib(default=None)

    def clean(self, tweet: str) -> str:
        """Removes sub-strings from the tweet
    
        Args:
         tweet: string tweet
    
        Returns:
         tweet with certain sub-strings removed
        """
        for expression in WheatBran.remove:
            tweet = re.sub(expression, WheatBran.ERASE, tweet)
        return tweet

    @property
    def tokenizer(self) -> TweetTokenizer:
        """The NLTK Tweet Tokenizer
    
        It will:
         - tokenize a string
         - remove twitter handles
         - remove repeated characters after the first three
        """
        if self._tokenizer is None:
            self._tokenizer = TweetTokenizer(preserve_case=False,
                                             strip_handles=True,
                                             reduce_len=True)
        return self._tokenizer

    def remove_useless_tokens(self, tokens: list) -> list:
        """Remove stopwords and punctuation
    
        Args:
         tokens: list of strings
    
        Returns:
         tokens with unuseful tokens removed
        """    
        return [word for word in tokens if (word not in self.stopwords and
                                            word not in string.punctuation)]

    @property
    def stopwords(self) -> list:
        """NLTK English stopwords
        
        Warning:
         if the stopwords haven't been downloaded this also tries too download them
        """
        if self._stopwords is None:
            nltk.download('stopwords')
            self._stopwords =  stopwords.words("english")
        return self._stopwords

    @property
    def stemmer(self) -> PorterStemmer:
        """Porter Stemmer for the tokens"""
        if self._stemmer is None:
            self._stemmer = PorterStemmer()
        return self._stemmer

    def stem(self, tokens: list) -> list:
        return [self.stemmer.stem(word) for word in tokens]

    def __call__(self, tweet: str) -> list:
        """does all the processing in one step
    
        Args:
         tweet: string to process
        """
        cleaned = self.clean(tweet)    
        cleaned = self.tokenizer.tokenize(cleaned)
        cleaned = self.stem(cleaned)
        cleaned = self.remove_useless_tokens(cleaned)
        return cleaned
