# from python
import random
import string

# from pypi
from expects import (
    contain_exactly,
    equal,
    expect
)
from pytest_bdd import (
    given,
    scenarios,
    then,
    when,
)

And = when


# fixtures
from fixtures import katamari, processor

scenarios("../../features/twitter/tweet_preprocessing.feature")


#Scenario: A tweet with a stock symbol is cleaned


@given("a tweet with a stock symbol in it")
def setup_stock_symbol(katamari, faker):
    symbol = "".join(random.choices(string.ascii_uppercase, k=4))
    head, tail = faker.sentence(), faker.sentence()
    katamari.to_clean = (f"{head} ${symbol} "
                         f"{tail}")

    # the cleaner ignores spaces so there's going to be two spaces between
    # the head and tail after the symbol is removed
    katamari.expected = f"{head}  {tail}"
    return

#   When the tweet is cleaned
#   Then it has the text removed


# Scenario: A re-tweet is cleaned.

@given("a tweet that has been re-tweeted")
def setup_re_tweet(katamari, faker):
    katamari.expected = faker.sentence()
    spaces = " " * random.randrange(1, 10)
    katamari.to_clean = f"RT{spaces}{katamari.expected}"
    return


@when("the tweet is cleaned")
def process_tweet(katamari, processor):
    katamari.actual = processor.clean(katamari.to_clean)
    return


@then("it has the text removed")
def check_cleaned_text(katamari):
    expect(katamari.expected).to(equal(katamari.actual))
    return


# Scenario: The tweet has a hyperlink

@given("a tweet with a hyperlink")
def setup_hyperlink(katamari, faker):
    base = faker.sentence()
    katamari.expected = base
    katamari.to_clean = base + faker.uri() + "\n" * random.randrange(5)
    return


@given("a tweet with hash symbols")
def setup_hash_symbols(katamari, faker):
    expected = faker.sentence()
    tokens = expected.split()
    expected_tokens = expected.split()

    for count in range(random.randrange(1, 10)):
        index = random.randrange(len(tokens))
        word = faker.word()
        tokens = tokens[:index] + [f"#{word}"] + tokens[index:]
        expected_tokens = expected_tokens[:index] + [word] + expected_tokens[index:]
    katamari.to_clean = " ".join(tokens)
    katamari.expected = " ".join(expected_tokens)
    return


# Scenario: The text is tokenized


@given("a string of text")
def setup_text(katamari):
    katamari.text = "Time flies like an Arrow, fruit flies like a BANANAAAA!"
    katamari.expected = ("time flies like an arrow , "
                         "fruit flies like a bananaaa !").split()
    return


@when("the text is tokenized")
def tokenize(katamari, processor):
    katamari.actual = processor.tokenizer.tokenize(katamari.text)
    return


@then("it is the expected list of strings")
def check_tokens(katamari):
    expect(katamari.actual).to(contain_exactly(*katamari.expected))
    return


#Scenario: The user removes stop words and punctuation


@given("a tokenized string")
def setup_tokenized_string(katamari):
    katamari.source = ("now is the winter of our discontent , "
                       "made glorious summer by this son of york ;").split()
    katamari.expected = ("winter discontent made glorious "
                         "summer son york".split())
    return


@when("the string is un-stopped")
def un_stop(katamari, processor):
    katamari.actual = processor.remove_useless_tokens(katamari.source)
    return
#  Then it is the expected list of strings


# Scenario: The user stems the tokens
#  Given a tokenized string
#  When the string is un-stopped
 

@And("tokens are stemmed")
def stem_tokens(katamari, processor):
    katamari.actual = processor.stem(katamari.actual)
    katamari.expected = "winter discont made gloriou summer son york".split()
    return


#  Then it is the expected list of strings


# Scenario: The user calls the processor


@given("a tweet")
def setup_tweet(katamari, faker):
    katamari.words = "How now, brown cow? Whither and dither the smelly laulau. Boooooow Wooooow!"
    katamari.tweet = f"RT {katamari.words}  #bocceballs {faker.uri()}"
    katamari.expected = "brown cow whither dither smelli laulau booow wooow boccebal".split()
    return


@when("the processor is called with the tweet")
def process_tweet(katamari, processor):
    katamari.actual = processor(katamari.tweet)
    return


@then("it returns the cleaned, tokenized, and stemmed list")
def check_processed_tweet(katamari):
    expect(katamari.actual).to(contain_exactly(*katamari.expected))
    return
