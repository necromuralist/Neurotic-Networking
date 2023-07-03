"""NaiveBayes Tweet Sentiment Classifier feature tests."""

# python
from collections import Counter

import math

# pypi
from expects import (
    be,
    be_empty,
    be_true,
    equal,
    expect,
)

from pytest_bdd import (
    given,
    scenarios,
    then,
    when,
)

import pytest_bdd

# this test repo
from fixtures import katamari

# software under test
from neurotic.nlp.twitter.counter import WordCounter
from neurotic.nlp.twitter.naive_bayes import NaiveBayes

scenarios("twitter/naive_bayes.feature")

# ********** #
# Scenario: The user builds the classifier


@given('a Naive Bayes definition')
def a_naive_bayes_definition(katamari):
    katamari.definition = NaiveBayes
    return


@when('the user builds the classifier')
def the_user_builds_the_classifier(katamari):
    katamari.labels = [0, 1, 1]
    katamari.tweets = "alfa bravo charley".split()
    katamari.classifier = katamari.definition(tweets=katamari.tweets,
                                              labels=katamari.labels)
    return


@then('it has the expected attributes')
def it_has_the_expected_attributes(katamari):
    expect(katamari.classifier.tweets).to(be(katamari.tweets))
    expect(katamari.classifier.labels).to(be(katamari.labels))
    katamari.classifier.check_rep()
    return

# ********** #
# Scenario: The user checks the counter

@given("a Naive Bayes classifier")
def build_naive_classifier(katamari):
    katamari.classifier = NaiveBayes(tweets=[], labels=[])
    return


@when("the user checks the counter")
def check_counter(katamari, mocker):
    katamari.counter = mocker.MagicMock(spec=WordCounter)
    katamari.counter_definition = mocker.MagicMock()
    katamari.counter_definition.return_value = katamari.counter
    mocker.patch("neurotic.nlp.twitter.naive_bayes.WordCounter", katamari.counter_definition)
    katamari.actual_counter = katamari.classifier.counter
    return


@then("it is the expected counter")
def expect_counter(katamari):
    expect(katamari.actual_counter).to(be(katamari.counter))
    return

# ********** #
# Scenario: The user checks the log-prior

@given("a valid Naive Bayes Classifier")
def setup_classifier(katamari):
    katamari.tweets = ["a blowfish", "b closing", "c that", "d plane"]
    katamari.labels = [1, 1, 0, 1]
    katamari.counts = Counter({
        ("appl", 0): 5,
        ("b", 1): 2,
        ("c", 1): 4,
        
    })
    katamari.classifier = NaiveBayes(tweets=katamari.tweets,
                                     labels = katamari.labels)
    katamari.classifier.counter._counts = katamari.counts
    return


@when("the user checks the log-odds prior")
def get_log_odds_prior(katamari):
    katamari.expected = math.log(3) - math.log(1)
    katamari.actual = katamari.classifier.logprior
    return


@then("it is close enough")
def expect_close_enough(katamari):
    expect(math.isclose(katamari.actual, katamari.expected)).to(be_true)
    return

# ********** #
# Scenario: The user checks the vocabulary
#  Given a valid Naive Bayes Classifier
 

@when("the user checks the vocabulary")
def check_vocabulary(katamari):
  katamari.actual = katamari.classifier.vocabulary
  katamari.expected = {"appl", "b", "c"}
  return


@then("all the words are there")
def compare_words(katamari):
  expect(katamari.actual ^ katamari.expected).to(be_empty)
  return

# ********** #
# Scenario: The user gets the log-likelihood dictionary
#  Given a valid Naive Bayes Classifier


@when("the user checks the loglikelihoods")
def check_log_likelihoods(katamari):
    katamari.expected = dict(
        appl=math.log(1/9) - math.log(6/8),
        b=math.log(3/9) - math.log(1/8),
        c=math.log(5/9) - math.log(1/8)
    )
    katamari.actual = katamari.classifier.loglikelihood
    return


@then("they are close enough")
def expect_close_values(katamari):
    for word in katamari.classifier.loglikelihood:
        expect(math.isclose(katamari.expected[word],
                            katamari.actual[word])).to(be_true)
    return

# ********** #
# Scenario: User predicts tweet positive probability
#   Given a valid Naive Bayes Classifier


@when("the user makes a tweet prediction")
def check_prediction(katamari):
    katamari.expected = (katamari.classifier.logprior
                         + katamari.classifier.loglikelihood["c"]
                         + katamari.classifier.loglikelihood["b"])
    katamari.actual = katamari.classifier.predict_ratio(
        "c you later b"
    )
    return


@then("it is the expected probability")
def expect_probability(katamari):
    expect(math.isclose(katamari.actual, katamari.expected)).to(be_true)
    return

# ********** #
# Scenario: The user predicts tweet sentiment
#   Given a valid Naive Bayes Classifier


@when("the user predicts the sentiment of tweets")
def check_predict_sentiment(katamari):
    katamari.actual_1 = katamari.classifier.predict_sentiment("c you later b")
    katamari.expected_1 = 1

    katamari.actual_2 = katamari.classifier.predict_sentiment("apple banana tart")
    katamari.expected_2 = 0
    return


@then("the sentiments are the expected ones")
def expect_sentiments(katamari):
    expect(katamari.actual_1).to(equal(katamari.expected_1))
    expect(katamari.actual_2).to(equal(katamari.expected_2))
    return
