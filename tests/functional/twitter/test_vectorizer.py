# from python
from collections import Counter

import random

# from pypi
from expects import (
    be,
    be_true,
    contain_exactly,
    expect,
    raise_error,
)
from pytest_bdd import (
    given,
    scenarios,
    when,
    then
)

import numpy

# this testing
from fixtures import katamari

# software under test
from neurotic.nlp.twitter.vectorizer import Columns, TweetVectorizer
from neurotic.nlp.twitter.counter import WordCounter

and_also = then
scenarios("../../features/twitter/tweet_vectorizer.feature")

# Scenario: A user converts a tweet to a feature-vector


@given("a Tweet Vectorizer")
def setup_tweet_vectorizer(katamari, mocker):
    katamari.bias = random.randrange(100) * random.random()
    TWEETS = 1

    TOKENS = "A B C".split()
    katamari.tweets = [TOKENS for tweet in range(TWEETS)]
    katamari.counts = Counter({('A', 0):1,
                               ('B', 1):2,
                               ('C', 0):3})
    katamari.counter = mocker.MagicMock(spec=WordCounter)
    katamari.counter.processed = katamari.tweets
    katamari.vectorizer = TweetVectorizer(tweets=katamari.tweets,
                                          counts=katamari.counts,
                                          bias=katamari.bias)
    katamari.vectorizer._process = mocker.MagicMock()
    katamari.vectorizer._process.return_value = "A B C".split()
    return


@when("the user converts a tweet to a feature-vector")
def extract_features(katamari):
    katamari.actual = katamari.vectorizer.extract_features("A B C")
    katamari.actual_array = katamari.vectorizer.extract_features("A B C", as_array=True)
    katamari.expected = [katamari.bias, 2, 4]
    katamari.expected_array = numpy.array(katamari.expected)
    return


@then("it's the expected feature-vector")
def check_feature_vectors(katamari):
    expect(numpy.allclose(katamari.actual_array, katamari.expected_array)).to(be_true)
    expect(katamari.actual).to(contain_exactly(*katamari.expected))

    expect(katamari.actual_array.shape).to(contain_exactly(1, 3))
    return

# Feature: A Tweet Count Vectorizer

# Scenario: A user retrieves the count vectors

@given("a user sets up the Count Vectorizer with tweets")
def setup_vectorizer(katamari, faker, mocker):
    katamari.bias = random.randrange(100) * random.random()
    TWEETS = 3

    TOKENS = "A B C"
    katamari.tweets = [TOKENS for tweet in range(TWEETS)]
    katamari.counter = mocker.MagicMock(spec=WordCounter)
    katamari.counter.counts = Counter({('A', 0):1,
                                       ('B', 1):2,
                                       ('C', 0):3})
    katamari.vectorizer = TweetVectorizer(tweets=katamari.tweets,
                                          counts=katamari.counter.counts,
                                          bias=katamari.bias)

    katamari.vectorizer._process = mocker.MagicMock()
    katamari.vectorizer._process.return_value = TOKENS.split()
    katamari.negative = numpy.array([sum([katamari.counter.counts[(token, 0)]
                                      for token in TOKENS])
                                      for row in range(TWEETS)])
    katamari.positive = numpy.array([sum([katamari.counter.counts[(token, 1)]
                                      for token in TOKENS])
                                     for row in range(TWEETS)])
    return


@when("the user checks the count vectors")
def check_count_vectors(katamari):
    # kind of silly, but useful for troubleshooting
    katamari.actual_vectors = katamari.vectorizer.vectors
    return


@then("the first column is the bias colum")
def check_bias(katamari):
    expect(all(katamari.actual_vectors[:, Columns.bias]==katamari.bias)).to(be_true)
    return


@and_also("the positive counts are correct")
def check_positive_counts(katamari):
    positive = katamari.actual_vectors[:, Columns.positive]
    expect(numpy.allclose(positive, katamari.positive)).to(be_true)
    return


@and_also("the negative counts are correct")
def check_negative_counts(katamari):
    negative = katamari.actual_vectors[:, Columns.negative]
    expect(numpy.allclose(negative, katamari.negative)).to(be_true)
    return

# Scenario: The vectors are reset


@given("a Tweet Vectorizer with the vectors set")
def setup_vectors(katamari, faker, mocker):
    katamari.vectors = mocker.MagicMock()
    katamari.vectorizer = TweetVectorizer(tweets = [faker.sentence()], counts=None)
    katamari.vectorizer._vectors = katamari.vectors
    return


@when("the user calls the reset method")
def call_reset(katamari):
    expect(katamari.vectorizer.vectors).to(be(katamari.vectors))
    katamari.vectorizer.reset()
    return


@then("the vectors are gone")
def check_vectors_gone(katamari):
    expect(katamari.vectorizer._vectors).to(be(None))
    return

# Scenario: the check-rep is called with bad tweets


@given("a Tweet Vectorizer with bad tweets")
def setup_bad_tweets(katamari):
    katamari.vectorizer = TweetVectorizer(tweets=[5],
                                          counts=Counter())
    return


@when("check-rep is called")
def call_check_rep(katamari):
    def bad_call():
        katamari.vectorizer.check_rep()
    katamari.bad_call = bad_call
    return


@then("it raises an AssertionError")
def check_assertion_error(katamari):
    expect(katamari.bad_call).to(raise_error(AssertionError))
    return

# Scenario: the check-rep is called with a bad word-counter


@given("a Tweet Vectorizer with the wrong counter object")
def setup_bad_counter(katamari, mocker):
    katamari.vectorizer = TweetVectorizer(tweets=["apple"], counts=mocker.MagicMock())
    return

# When check-rep is called
# Then it raises an AssertionError
