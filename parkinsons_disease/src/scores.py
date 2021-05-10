from sklearn.model_selection import cross_val_score, StratifiedKFold
from src.pipeline import Pipeline


def scores(data, labels, model):
    kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

    accuracy = cross_val_score(model, data, labels, cv=kfold, scoring="accuracy").mean()
    precision = cross_val_score(model, data, labels, cv=kfold, scoring="precision").mean()
    recall = cross_val_score(model, data, labels, cv=kfold, scoring="recall").mean()
    f1 = cross_val_score(model, data, labels, cv=kfold, scoring="f1").mean()

    metrics = {"accuracy": float(accuracy),
               "precision": float(precision),
               "recall": float(recall),
               "f1": float(f1)}

    Pipeline.save_scores(metrics)
