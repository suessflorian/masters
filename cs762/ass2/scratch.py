from sklearn.preprocessing import MinMaxScaler
import pandas as pd


from sklearn.base import BaseEstimator, ClassifierMixin
from dataclasses import dataclass
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.metrics import accuracy_score
import numpy as np

@dataclass
class Final(Improved):
    _scaler = MinMaxScaler()

    def fit(self, features, labels):
        """ fit globally configures the classifier, vectorizer and
        normalizer onto the features and labels provided.
        """
        reviews = features.loc[:, 'review']

        self._vectorizer = self._configure_vectorizer(reviews)
        count_vectors = self._vectorizer.transform(reviews)

        self._normalizer = self._configure_normalizer(count_vectors)
        self._classifier = self._configure_classifier()

        checkin_times = np.array(features['mean_checkin_time']).reshape(-1, 1)
        scaled_mean_checkin_times = self._scaler.fit_transform(checkin_times)

        combined_features = np.hstack((
            self._transform_count_vectors(count_vectors).toarray(),
            scaled_mean_checkin_times)
        )

        return self._classifier.fit(combined_features, labels)

    def predict(self, features):
        reviews = features.loc[:, 'review']

        count_vectors = self._vectorizer.transform(reviews)
        checkin_times = np.array(features['mean_checkin_time']).reshape(-1, 1)
        scaled_mean_checkin_times = self._scaler.fit_transform(checkin_times)

        combined_features = np.hstack((
            self._normalize_count_vectors(count_vectors).toarray(),
            scaled_mean_checkin_times)
        )

        return self._classifier.predict(combined_features)
