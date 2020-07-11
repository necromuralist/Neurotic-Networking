Feature: A Word Frequency Counter

In order to get a sense of how the words correlate with sentiment
I want to be able to count word-sentiment pairs.

Scenario: The Word Counter is created
  Given a word counter class
  When the word counter is created
  Then it has the expected attributes

Scenario: The Word Frequency counter is called
  Given a word frequency counter
  When the counter is called
  Then the counts are the expected
