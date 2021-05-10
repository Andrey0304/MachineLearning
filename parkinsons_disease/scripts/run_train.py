import pandas as pd
from argparse import ArgumentParser
from src.train import run_training


def parse_args(*argument_array):
    parser = ArgumentParser()
    parser.add_argument('--traindata-path', required=True,
                        help='The path to the train_data')

    return parser.parse_args(*argument_array)


def main():
    args = parse_args()
    data = pd.read_csv(args.traindata_path)

    features = data.drop(columns=["status"])
    labels = data["status"]

    run_training(features, labels)


if __name__ == "__main__":
    main()
