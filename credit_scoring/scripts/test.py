from src.pipelines.test import run_testing
import pandas as pd
from argparse import ArgumentParser


def parse_args(*argument_array):
    parser = ArgumentParser()

    parser.add_argument('--testdata-path', required=True,
                        help='The path to the test_data')
    parser.add_argument('--pipe-path', required=True,
                        help='The path to save the pipeline')
    parser.add_argument('--predict-path', required=True,
                        help='The path to save the predict')

    return parser.parse_args(*argument_array)


def main():
    args = parse_args()

    test_data = pd.read_csv(args.testdata_path)
    run_testing(data=test_data,
                pipe_path=args.pipe_path,
                predict_path=args.predict_path)


if __name__ == "__main__":
    main()
