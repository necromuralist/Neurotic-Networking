# pypi
from dotenv import load_dotenv

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

X_train, Y_train = get_matrices(
    loader.training, loader.french_subset, loader.english_subset)
