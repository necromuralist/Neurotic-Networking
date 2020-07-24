Feature: A Tweet Count Vectorizer

Scenario: A user converts a tweet to a feature-vector

Given a Tweet Vectorizer
When the user converts a tweet to a feature-vector
Then it's the expected feature-vector

Scenario: A user retrieves the count vectors
Given a user sets up the Count Vectorizer with tweets
When the user checks the count vectors
Then the first column is the bias colum
And the positive counts are correct
And the negative counts are correct

Scenario: The vectors are reset
Given a Tweet Vectorizer with the vectors set
When the user calls the reset method
Then the vectors are gone

Scenario: the check-rep is called with bad tweets
Given a Tweet Vectorizer with bad tweets
When check-rep is called
Then it raises an AssertionError

Scenario: the check-rep is called with a bad word-counter
Given a Tweet Vectorizer with the wrong counter object
When check-rep is called
Then it raises an AssertionError
