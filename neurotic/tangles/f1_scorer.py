from neurotic.tangles.timer import Timer


class F1Scorer:
    """Calculates the F1 and other scores
    
    Args:
     predictor: callable that gets passed and image and outputs boolean
     true_images: images that should be predicted as True
     false_images: images that shouldn't be matched by the predictor
     done_message: what to announce when done
    """
    def __init__(self, predictor: callable, true_images:list,
                 false_images: list,
                 done_message: str="Scoring Done") -> None:
        self.predictor = predictor
        self.true_images = true_images
        self.false_images = false_images
        self.done_message = done_message
        self._timer = None
        self._false_image_predictions = None
        self._true_image_predictions = None
        self._false_positives = None
        self._false_negatives = None
        self._true_positives = None
        self._true_negatives = None
        self._false_positive_rate = None
        self._precision = None
        self._recall = None
        self._f1 = None
        self._accuracy = None
        self._specificity = None
        return

    @property
    def timer(self) -> Timer:
        if self._timer is None:
            self._timer = Timer(message=self.done_message, emit=False)
        return self._timer

    @property
    def false_image_predictions(self) -> list:
        """Predictions made on the false-images"""
        if self._false_image_predictions is None:
            self._false_image_predictions = [self.predictor(str(image))
                                             for image in self.false_images]
        return self._false_image_predictions

    @property
    def true_image_predictions(self) -> list:
        """Predictions on the true-images"""
        if self._true_image_predictions is None:
            self._true_image_predictions = [self.predictor(str(image))
                                            for image in self.true_images]
        return self._true_image_predictions

    @property
    def true_positives(self) -> int:
        """count of correct positive predictions"""
        if self._true_positives is None:
            self._true_positives = sum(self.true_image_predictions)
        return self._true_positives

    @property
    def false_positives(self) -> int:
        """Count of incorrect positive predictions"""
        if self._false_positives is None:
            self._false_positives = sum(self.false_image_predictions)
        return self._false_positives

    @property
    def false_negatives(self) -> int:
        """Count of images that were incorrectly classified as negative"""
        if self._false_negatives is None:
            self._false_negatives = len(self.true_images) - self.true_positives
        return self._false_negatives

    @property
    def true_negatives(self) -> int:
        """Count of images that were correctly ignored"""
        if self._true_negatives is None:
            self._true_negatives = len(self.false_images) - self.false_positives
        return self._true_negatives

    @property
    def accuracy(self) -> float:
        """fraction of correct predictions"""
        if self._accuracy is None:
            self._accuracy = (
                (self.true_positives + self.true_negatives)
                /(len(self.true_images) + len(self.false_images)))
        return self._accuracy

    @property
    def precision(self) -> float:
        """True-Positive with penalty for false positives"""
        if self._precision is None:
            self._precision = self.true_positives/(
                self.true_positives + self.false_positives)
        return self._precision
    
    @property
    def recall(self) -> float:
        """fraction of correct images correctly predicted"""
        if self._recall is None:
            self._recall = (
                self.true_positives/len(self.true_images))
        return self._recall

    @property
    def false_positive_rate(self) -> float:
        """fraction of incorrect images predicted as positive"""
        if self._false_positive_rate is None:
            self._false_positive_rate = (
                self.false_positives/len(self.false_images))
        return self._false_positive_rate

    @property
    def specificity(self) -> float:
        """metric for how much to believe a negative prediction

        Specificity is 1 - false positive rate so you only need one or the other
        """
        if self._specificity is None:
            self._specificity = self.true_negatives/(self.true_negatives
                                                     + self.false_positives)
        return self._specificity

    @property
    def f1(self) -> float:
        """Harmonic Mean of the precision and recall"""
        if self._f1 is None:
            TP = 2 * self.true_positives
            self._f1 = (TP)/(TP + self.false_negatives + self.false_positives)
        return self._f1
        
    def __call__(self) -> None:
        """Emits the F1 and other scores as an org-table
        """
        self.timer.start()
        print("|Metric|Value|")
        print("|-+-|")
        print("|Accuracy|{:.2f}|".format(self.accuracy))
        print("|Precision|{:.2f}|".format(self.precision))
        print("|Recall|{:.2f}|".format(self.recall))
        print("|Specificity|{:.2f}".format(self.specificity))
        print("|F1|{:.2f}|".format(self.f1))
        self.timer.end()
        print("|Ended|{}|".format(self.timer.ended))
        print("|Elapsed|{}|".format(self.timer.ended - self.timer.started))
        return
