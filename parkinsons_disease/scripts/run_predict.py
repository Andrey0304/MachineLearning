import pandas as pd
from src.test import run_predict
from argparse import ArgumentParser


def parse_args(*argument_array):
    parser = ArgumentParser()
    parser.add_argument('--testdata-path', required=True,
                        help='The path to the test_data')

    return parser.parse_args(*argument_array)


def main():
    args = parse_args()
    data = pd.read_csv(args.testdata_path)
    run_predict(data)


if __name__ == "__main__":
    main()
