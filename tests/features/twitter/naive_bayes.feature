Feature: NaiveBayes Tweet Sentiment Classifier

Scenario: The user builds the classifier
  Given a Naive Bayes definition
  When the user builds the classifier
  Then it has the expected attributes

Scenario: The user checks the counter
  Given a Naive Bayes classifier
  When the user checks the counter
  Then it is the expected counter

Scenario: The user checks the log-prior
 Given a valid Naive Bayes Classifier
 When the user checks the log-odds prior
 Then it is close enough

Scenario: The user checks the vocabulary
  Given a valid Naive Bayes Classifier
  When the user checks the vocabulary
  Then all the words are there

Scenario: The user gets the log-likelihood dictionary
  Given a valid Naive Bayes Classifier
  When the user checks the loglikelihoods
  Then they are close enough

Scenario: User predicts tweet positive probability
  Given a valid Naive Bayes Classifier
  When the user makes a tweet prediction
  Then it is the expected probability

Scenario: The user predicts tweet sentiment
  Given a valid Naive Bayes Classifier
  When the user predicts the sentiment of tweets
  Then the sentiments are the expected ones
