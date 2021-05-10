from src.pipelines.pipeline import Pipeline
import pandas as pd

def run_testing(data, pipe_path: str, predict_path: str):
    """The function which runs testing and loads the results and the pipe."""
    model = Pipeline.load(pipe_path)
    predictions = model.predict(data)
    Pipeline.save_predictions(data, predictions, predict_path)
