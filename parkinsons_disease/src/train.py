import os
import yaml
from src.scores import scores
from src.pipeline import define_steps, Pipeline

config_path = os.path.join('./config/params_all.yaml')
config = yaml.safe_load(open(config_path))


def run_training(data, labels):
    """The function which runs training and saves the results and the pipe."""
    steps = define_steps()
    pipe = Pipeline(steps)
    model = pipe.fit(data, labels)
    pipe.save_model(model)
    print('Fit is finished.')

    scores(data, labels, model)