# pypi
from expects import (
    be,
    equal,
    expect
    )

from pytest_bdd import (
    given,
    scenarios,
    then,
    when
)

# testing setup
from fixtures import katamari

# software under test
from neurotic.nlp.twitter.counter import WordCounter
from neurotic.nlp.twitter.processor import TwitterProcessor

scenarios("twitter/word_frequencies.feature")

# Scenario: The Word Counter is created


@given("a word counter class")
def setup_class(katamari):
    katamari.definition = WordCounter
    return


@when("the word counter is created")
def create_word_counter(katamari, faker, mocker):
    katamari.tweets = mocker.Mock(list)
    katamari.labels = mocker.Mock(list)
    katamari.processor = mocker.Mock()
    katamari.counter = katamari.definition(tweets=katamari.tweets,
                                           labels=katamari.labels)
    katamari.counter._process = katamari.processor
    return


@then("it has the expected attributes")
def check_attributes(katamari):
    expect(katamari.counter.tweets).to(be(katamari.tweets))
    expect(katamari.counter.labels).to(be(katamari.labels))
    expect(katamari.counter.process).to(be(katamari.processor))
    return


# Scenario: The Word Frequency counter is called


@given("a word frequency counter")
def setup_word_frequency_counter(katamari, mocker):
    processor = TwitterProcessor()
    katamari.tweets = ["a b aab a b c"]
    katamari.labels = [1] * len(katamari.tweets)
    katamari.counter = WordCounter(tweets=katamari.tweets,
                                   labels=katamari.labels)

    bad_sentiment = ["c aab aab"]
    katamari.tweets += bad_sentiment
    katamari.labels += [0]
    # since the tokenizer removes and changes words
    # I'm going to mock it out
    katamari.counter._process = mocker.MagicMock(TwitterProcessor)
    katamari.counter.process.side_effect = lambda x: x.split()
    katamari.expected = {("a", 1): 2, ("b", 1): 2, ("c", 1): 1, ("aab", 1):1,
                         ("c", 0): 1, ("aab", 0): 2}
    return


@when("the counter is called")
def call_counter(katamari):
    katamari.counts = katamari.counter.counts
    return


@then("the counts are the expected")
def check_counts(katamari):
    for key, value in katamari.counts.items():
        expect(katamari.expected[key]).to(equal(value))
    return
