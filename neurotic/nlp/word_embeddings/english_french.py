# pypi
from dotenv import load_dotenv


import attr
import numpy

# my stuff
from neurotic.nlp.word_embeddings.embeddings import EmbeddingsLoader

load_dotenv("posts/nlp/.env", override=True)

loader = EmbeddingsLoader()

def get_matrices(en_fr: dict, french_vecs: dict, english_vecs: dict):
    """
    Args:
        en_fr: English to French dictionary
        french_vecs: French words to their corresponding word embeddings.
        english_vecs: English words to their corresponding word embeddings.

    Return: 
        X: a matrix where the columns are the English embeddings.
        Y: a matrix where the columns correspond to the French embeddings.
    """

    ### START CODE HERE (REPLACE INSTANCES OF 'None' with your code) ###

    # X_l and Y_l are lists of the english and french word embeddings
    # X_l = list()
    # Y_l = list()

    # get the english words (the keys in the dictionary) and store in a set()
    english_set = set(english_vecs)

    # get the french words (keys in the dictionary) and store in a set()
    french_set = set(french_vecs)

    # store the french words that are part of the english-french dictionary (these are the values of the dictionary)
    # french_words = set(en_fr.values())
    filtered = {english_word: french_word
                for english_word, french_word in en_fr.items()
                if english_word in english_set and french_word in french_set}
    X = [english_vecs[english_word] for english_word in filtered]
    Y = [french_vecs[french_word] for french_word in filtered.values()]

    # loop through all english, french word pairs in the english french dictionary
    
    
    # for en_word, fr_word in en_fr.items():
    # 
    #     # check that the french word has an embedding and that the english word has an embedding
    #     if fr_word in french_set and en_word in english_set:
    # 
    #         # get the english embedding
    #         en_vec = english_vecs[en_word]
    # 
    #         # get the french embedding
    #         fr_vec = french_vecs[fr_word]
    # 
    #         # add the english embedding to the list
    #         X_l.append(en_vec)
    # 
    #         # add the french embedding to the list
    #         Y_l.append(fr_vec)
    # 
    # # stack the vectors of X_l into a matrix X
    # X = numpy.vstack(X_l)
    # 
    # # stack the vectors of Y_l into a matrix Y
    # Y = numpy.vstack(Y_l)
    ### END CODE HERE ###

    # return X, Y
    return numpy.vstack(X), numpy.vstack(Y)


@attr.s(auto_attribs=True)
class TrainingData:
    """Converts the embeddings into a test set

    Args:
     loader: EmbeddingsLoader instance
    """
    _loader: EmbeddingsLoader=None
    _english_vocabulary: set=None
    _french_vocabulary: set=None
    _filtered: dict=None
    _x_train: numpy.ndarray=None
    _y_train: numpy.ndarray=None

    @property
    def loader(self) -> EmbeddingsLoader:
        """A loader for the embeddings subsets"""
        if self._loader is None:
            self._loader = EmbeddingsLoader()
        return self._loader

    @loader.setter
    def loader(self, new_loader: EmbeddingsLoader) -> None:
        """Sets the embeddings loader"""
        self._loader = new_loader
        return

    @property
    def english_vocabulary(self) -> set:
        """The english embeddings subset words"""
        if self._english_vocabulary is None:
            self._english_vocabulary = set(self.loader.english_subset)
        return self._english_vocabulary

    @property
    def french_vocabulary(self) -> set:
        """The french embeddings subset words"""
        if self._french_vocabulary is None:
            self._french_vocabulary = set(self.loader.french_subset)
        return self._french_vocabulary

    @property
    def filtered(self) -> dict:
        """A {enlish:french} dict filtered down
        
        This is a dict made of the original english-french dictionary created
        by the embeddings loader but filtered down so that the key is in the
        ``english_vocabulary`` and the value is in the ``french_vocabulary``

        This is used to ensure that the training set is created it will only
        contain terms that have entries in both embeddings subsets
        """
        if self._filtered is None:
            self._filtered = {
                english_word: french_word
                for english_word, french_word in self.loader.training.items()
                if (english_word in self.english_vocabulary and
                    french_word in self.french_vocabulary)}
        return self._filtered

    @property
    def x_train(self) -> numpy.ndarray:
        """The english-language embeddings as row-vectors"""
        if self._x_train is None:
            self._x_train = numpy.vstack(
                [self.loader.english_subset[english_word]
                 for english_word in self.filtered]
                )
        return self._x_train

    @property
    def y_train(self) -> numpy.ndarray:
        """The french-language embeddings as row-vectors"""
        if self._y_train is None:
            self._y_train = numpy.vstack(
                [self.loader.french_subset[french_word]
                 for french_word in self.filtered.values()]
            )
        return self._y_train

    def check_rep(self) -> None:
        """Checks the shape of the training data


        Note:
         since this checks those attributes they will be built if they don't
         already exist

        Raises:
         AttributeError - there'se something unexpected about the shape of the data
        """
        rows, columns = self.x_train.shape
        assert rows == len(self.filtered)
        assert columns == len(next(iter(self.loader.english_subset.values())))
        
        rows, columns = self.y_train.shape
        assert rows == len(self.filtered)
        assert columns == len(next(iter(self.loader.french_subset.values())))            
        return
