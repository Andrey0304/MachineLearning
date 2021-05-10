import pandas as pd
from src.pipeline import Pipeline


def run_predict(data):
    model = Pipeline.load_model()
    predict = model.predict(data)
    result = pd.DataFrame({'Id': data.index, 'Predictions': predict})

    Pipeline.save_predict(result)
