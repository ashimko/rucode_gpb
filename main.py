import argparse
import numpy as np
import pandas as pd
from data_processor import data_processor

# функции get_stats и squeeze требуются здесь
# так как они используются в FunctionalTransformer
# в обученных scikit-learn Pipelines


def get_stats(x: np.array) -> np.array:
    if isinstance(x, pd.DataFrame):
        x = x.values
    return np.hstack([x // 10**i for i in range(12)])


def squeeze(x):
    return x[:, 0]


def main():
    parser = argparse.ArgumentParser(description='Anonymize data.')
    parser.add_argument('--numb_label_encoder', type=str, default='./models/numb_label_encoder.pkl',
                        help='path to scikit-learn label encoder of numeric anonymized classes')
    parser.add_argument('--text_label_encoder', type=str, default='./models/text_label_encoder.pkl',
                        help='path to scikit-learn label encoder of text anonymized classes')
    parser.add_argument('--numb_pipe', type=str, default='./models/numb_pipe.pkl',
                        help='path to scikit-learn pipeline used for process numb features')
    parser.add_argument('--text_pipe', type=str, default='./models/text_pipe.pkl',
                        help='path to scikit-learn pipeline used for process text features')
    parser.add_argument('--mode', type=str, default='tabular',
                        help='Prediction mode: either tabular or raw')
    parser.add_argument('--input_tabular_data', type=str, default='./data/test_data/application.csv',
                        help='path to tabular data in csv format')
    parser.add_argument('--input_raw_text_data', type=str, default='./data/test_data/X_text_test_raw.csv',
                        help='path to text raw format data (should be csv)')
    parser.add_argument('--input_raw_numb_data', type=str, default='./data/test_data/X_numb_test_raw.csv',
                        help='path to numb raw format data (should be csv)')
    parser.add_argument('--output_tabular_data_path', type=str, default='./data/output/application_transformed.csv',
                        help='path for saving anonymized tabular data')
    parser.add_argument('--output_text_raw_data_path', type=str,
                        default='./data/output/X_text_test_raw_transformed.csv',
                        help='Absolute path for saving anonymized raw text data')
    parser.add_argument('--output_numb_raw_data_path', type=str,
                        default='./data/output/X_numb_test_raw_transformed.csv',
                        help='Absolute path for saving anonymized raw numb data')
    args = parser.parse_args()
    data_processor(args)


if __name__ == '__main__':
    main()
