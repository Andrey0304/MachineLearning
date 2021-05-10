import pandas as pd
from sklearn.base import TransformerMixin


class FeatureBuilder(TransformerMixin):
    """Special Class for cleaning data and building features."""

    def __init__(self):
        pass

    def fit(self, X=None, y=None):
        return self

    def transform(self, X: pd.DataFrame, y=None):
        features = X.copy(deep=True)
        features['Jitter:DDP__^3'] = features['Jitter:DDP'] ** 3
        features['MDVP:Jitter(Abs)__^5'] = features['MDVP:Jitter(Abs)'] ** 5
        features['Shimmer:DDA__^2'] = features['Shimmer:DDA'] ** 2

        features.drop(columns=['name',
                               'Shimmer:APQ3',
                               'MDVP:RAP',
                               'MDVP:Shimmer',
                               'MDVP:Jitter(%)',
                               'MDVP:Shimmer(dB)',
                               'MDVP:PPQ',
                               'spread1',
                               'Shimmer:APQ5',
                               'Jitter:DDP',
                               'MDVP:Jitter(Abs)',
                               'Shimmer:DDA'],
                      inplace=True)
        print("Features are successfully built.")
        return features

    def fit_transform(self, X: pd.DataFrame, y=None):
        self.fit(X, y)
        return self.transform(X, y)
