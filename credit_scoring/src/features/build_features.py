import pandas as pd
import numpy as np
from sklearn.base import TransformerMixin
import collections


class FeatureBuilder(TransformerMixin):
    """Special Class for cleaning data and building features."""

    def __init__(self):
        pass

    def fit(self, X=None, y=None):
        return self

    def transform(self, X: str or pd.DataFrame, y=None) -> pd.DataFrame:
        """Builds features and saves data.
        Args:
            data: data pandas DataFrame
        """
        df = X.copy(deep=True)
        df['NumDependents'].fillna(df['NumDependents'].median(), inplace=True)
        df['Income'].fillna(df['Income'].median(), inplace=True)
        df.index = df["client_id"]
        df.drop(columns="client_id", inplace=True)
        df['Age'] = df['Age'].astype(int)
        df['Age'] = pd.qcut(df.Age.values, 5).codes
        df['NumLoans'] = pd.qcut(df['NumLoans'].values, 5).codes
        df['NumDependents'] = pd.cut(df['NumDependents'],
                                     bins=[-1, 0, 4, np.inf])
        df['NumRealEstateLoans'] = pd.cut(df['NumRealEstateLoans'],
                                          bins=[-1, 5, 7, np.inf])
        df["Num30-59Delinquencies"] = pd.cut(df["Num30-59Delinquencies"],
                                             bins=[-1, 0.5, 1, 2, 5, np.inf])
        df["Num60-89Delinquencies"] = pd.cut(df["Num60-89Delinquencies"],
                                             bins=[-1, 0.5, 1, 4, np.inf])

        df = pd.get_dummies(df, columns=["Age"], prefix="Age")
        df = pd.get_dummies(df, columns=["NumLoans"], prefix="NumLoans")
        df = pd.get_dummies(df, columns=['Num30-59Delinquencies'],
                            prefix="Num30-59")
        df = pd.get_dummies(df, columns=["Num60-89Delinquencies"],
                            prefix="Num60-89")
        df = pd.get_dummies(df, columns=["NumDependents"],
                            prefix="NumDependents")
        df = pd.get_dummies(df, columns=["NumRealEstateLoans"],
                            prefix="NumRealEstateLoans")

        print(f"Features are successfully built.")
        return df

    def fit_transform(self, X: pd.DataFrame, y=None):
        self.fit(X, y)
        return self.transform(X, y)


def build_features(df):
    """Returns the data in the form of pandas DataFrame."""
    obj = FeatureBuilder()
    return obj.transform(df)


def detect_outliers(df):
    print("Started detect outliers...")
    data = df[df["Delinquent90"] == 0].drop(
        columns=["Delinquent90", 'client_id'])

    outlier_indices = []
    for col in data.columns:
        IQR = np.percentile(data[col], 80)
        outlier_list_col = data[data[col] > IQR].index
        outlier_indices.extend(outlier_list_col)

    outlier_indices = collections.Counter(outlier_indices)
    multiple_outliers = list(k for k, v in outlier_indices.items() if v > 2)

    df = df.drop(multiple_outliers, axis=0).reset_index(drop=True)
    print("Outliers have been successfully removed")
    return df
