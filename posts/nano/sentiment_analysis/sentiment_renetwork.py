from sentiment_network import SentimentNetwork

class SentimentRenetwork(SentimentNetwork):
    """Re-do of the Sentiment Network

    .. uml::
    
       SentimentRenetwork --|> SentimentNetwork

    This is a re-implementation that doesn't use counts as inputs
    """
    def update_input_layer(self, review: str) -> None:
        """Update the counts in the input layer

        Args:
         review: A movie review
        """
        self.input_layer *= 0
        tokens = set(review.split(self.tokenizer))
        for token in tokens:
            if token in self.word_to_index:
                self.input_layer[:, self.word_to_index[token]] = 1
        return
