import yaml
import os
from typing import List, Tuple
import dill
from sklearn.pipeline import Pipeline as SkPipe
from src.preprocessing import FeatureBuilder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

config_path = os.path.join('./config/params_all.yaml')
config = yaml.safe_load(open(config_path))


class Pipeline(SkPipe):
    """Class for defining pipeline that encapsulates workflow."""

    def __init__(self, steps: List[Tuple[str, object]]):
        super().__init__(self.__parse_steps(steps))

    @staticmethod
    def __parse_steps(steps):
        return steps

    @staticmethod
    def save_scores(metrics):
        with open(config['score_path'], 'wb') as file:
            yaml.safe_dump(metrics, file, encoding='UTF-8', allow_unicode=True)
        print('Scores are succesfuly saved.')

    @staticmethod
    def save_model(model):
        with open(config['model_path'], "wb") as file:
            dill.dump(model, file)
        print('Model are successfuly saved.')

    @staticmethod
    def load_model():
        with open(config['model_path'], "rb") as file:
            model = dill.load(file)
        return model

    @staticmethod
    def save_predict(result):
        result.to_csv(config['predict_path'], index=False)
        print('Result are successfuly saved.')


def define_steps():
    """Here you define the steps of the main pipeline of the project"""
    transformer = FeatureBuilder()
    model = KNeighborsClassifier(**config['model'])
    scaler = StandardScaler()
    steps = [
        ("transformer", transformer),
        ("scaler", scaler),
        ("model", model)
    ]
    return steps
