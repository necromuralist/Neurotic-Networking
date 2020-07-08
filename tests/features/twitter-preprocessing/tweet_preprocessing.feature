Feature: Tweet pre-processor

Scenario: A re-tweet is cleaned.

  Given a tweet that has been re-tweeted
  When the tweet is cleaned
  Then it has the text removed

Scenario: The tweet has a hyperlink
  Given a tweet with a hyperlink
  When the tweet is cleaned
  Then it has the text removed

Scenario: A tweet has hash symbols in it.
  Given a tweet with hash symbols
  When the tweet is cleaned
  Then it has the text removed

Scenario: The text is tokenized
  Given a string of text
  When the text is tokenized
  Then it is the expected list of strings

Scenario: The user removes stop words and punctuation
  Given a tokenized string
  When the string is un-stopped
  Then it is the expected list of strings

Scenario: The user stems the tokens
  Given a tokenized string
  When the string is un-stopped
  And tokens are stemmed
  Then it is the expected list of strings

Scenario: The user calls the processor
  Given a tweet
  When the processor is called with the tweet
  Then it returns the cleaned, tokenized, and stemmed list
