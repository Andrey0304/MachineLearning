from typing import List, Tuple
import pandas as pd

import dill
from sklearn.pipeline import Pipeline as SkPipe

from src.features import FeatureBuilder
from src.modeling import ModelWrapper


class Pipeline(SkPipe):
    """Class for defining pipeline that encapsulates workflow."""
    def __init__(self, steps: List[Tuple[str, object]]):
        super().__init__(self.__parse_steps(steps))

    @staticmethod
    def __parse_steps(steps):
        return steps

    def save(self, path: str):
        print("Started to save...")
        with open(path, 'wb') as f:
            dill.dump(self, f)
        print("Models are successfully saved")

    @staticmethod
    def save_score(score, score_path: str):
        print("Started to save score...")
        score.to_csv(score_path, index=False)
        print("Scores are successfully saved")

    @staticmethod
    def load(path: str):
        with open(path, 'rb') as f:
            pipe = dill.load(f)
        return pipe
    
    @staticmethod
    def save_predictions(data, predictions, path: str):
        print("Predictions started to save...")
        result = pd.DataFrame({'Client_Id': data.index, 'Predictions': predictions.astype(int)})
        result.to_csv(path, index=False)
        print("Predictions are successfully saved")

def define_steps():
    """Here you define the steps of the main pipeline of the project"""
    transformer = FeatureBuilder()
    model = ModelWrapper()
    steps = [
        ("transformer", transformer),
        ("model", model)
    ]
    return steps
