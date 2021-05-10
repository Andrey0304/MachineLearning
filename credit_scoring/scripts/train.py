"""This is dedicated for training related staff."""
from src.pipelines import run_training
from src.features.build_features import detect_outliers
from src.pipelines.scores import evaluate_model
from argparse import ArgumentParser
import pandas as pd


def parse_args(*argument_array):
    parser = ArgumentParser()

    parser.add_argument('--traindata-path', required=True,
                        help='The path to the train_data')
    parser.add_argument('--pipe-path', required=True,
                        help='The path to save the pipeline')
    parser.add_argument('--score-path', required=True,
                        help='The path to save the score')

    return parser.parse_args(*argument_array)


def main():
    args = parse_args()
    df = pd.read_csv(args.traindata_path)
    df = detect_outliers(df)

    features = df.drop(columns="Delinquent90")
    labels = df["Delinquent90"]

    run_training(data=features, labels=labels, pipe_path=args.pipe_path)
    evaluate_model(data=features, labels=labels, score_path=args.score_path)


if __name__ == "__main__":
    main()
