from sklearn.model_selection import StratifiedKFold, cross_val_score
from src.pipelines.pipeline import define_steps, Pipeline
import pandas as pd


def evaluate_model(data, labels, score_path):
    str_kfold = StratifiedKFold(n_splits=3, shuffle=True, random_state=0)

    steps = define_steps()
    pipe = Pipeline(steps)

    metrics = pd.DataFrame(
        {"score_type": ["balanced_accuracy", "f1", "roc_auc"]})
    metrics.set_index("score_type")

    balanc_acc = cross_val_score(pipe, data, labels, cv=str_kfold, scoring="balanced_accuracy").mean()
    f1 = cross_val_score(pipe, data, labels, cv=str_kfold, scoring="f1").mean()
    roc_auc = cross_val_score(pipe, data, labels, cv=str_kfold, scoring="recall").mean()

    metrics["value"] = [balanc_acc, f1, roc_auc]
    Pipeline.save_score(metrics, score_path)

    return metrics
