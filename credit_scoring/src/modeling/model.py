import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.base import BaseEstimator


class ModelWrapper(BaseEstimator):
    """Special Class for classifying."""

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100,
                                            max_features=None,
                                            class_weight={1: 0.9, 0: 0.1},
                                            min_samples_split=15,
                                            min_samples_leaf=6,
                                            max_depth=17,
                                            max_samples=0.2,
                                            random_state=0,
                                            n_jobs=-1)

    def fit(self, data: str or pd.DataFrame, labels: str or pd.DataFrame):
        print('Started to fit...')
        self.model.fit(data, labels)
        print('Fit is finished.')
        return self

    def predict(self, data: str or pd.DataFrame) -> pd.DataFrame:
        """Builds sentiment data."""

        print('Prediction is started.')
        prediction = self.model.predict(data)
        print('Prediction is finished.')

        return prediction
