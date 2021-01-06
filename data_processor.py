import pandas as pd
import numpy as np
from scipy import stats

from utils import load_from_pickle
from replacers import replace_data


def data_processor(args):
    numb_label_encoder = load_from_pickle(args.numb_label_encoder)
    text_label_encoder = load_from_pickle(args.text_label_encoder)
    numb_pipe = load_from_pickle(args.numb_pipe)
    text_pipe = load_from_pickle(args.text_pipe)

    if args.mode == 'tabular':
        data = pd.read_csv(args.input_tabular_data)
        text_cols = data.head(0).select_dtypes(include=object).columns
        numb_cols = data.head(0).select_dtypes(include='number').columns

        for col in text_cols:
            predicted_class = text_pipe.predict(data[col].values.reshape(-1, 1))
            print('true', col)
            predicted_class = text_label_encoder.inverse_transform(predicted_class)
            predicted_class = stats.mode(predicted_class)[0][0]

            if predicted_class in ['lastname', 'firstname', 'middlename']:
                replaced_data = replace_data(data[[col, 'sex']], predicted_class=predicted_class)
                data[col] = replaced_data
            else:
                replaced_data = replace_data(data[col], predicted_class=predicted_class)
                data[col] = replaced_data
            print('predicted', predicted_class)
            data.to_csv(args.output_tabular_data_path, index=False)

        for col in numb_cols:
            predicted_class = numb_pipe.predict(data[col].values.reshape(-1, 1))
            print('true', col)
            predicted_class = numb_label_encoder.inverse_transform(predicted_class)
            predicted_class = stats.mode(predicted_class)[0][0]
            replaced_data = replace_data(data[col], predicted_class=predicted_class)
            data[col] = replaced_data
            print('predicted', predicted_class)
            data.to_csv(args.output_tabular_data_path, index=False)
    elif args.mode == 'raw':
        X_text_test = pd.read_csv(args.input_raw_text_data)
        predicted_text_classes = text_pipe.predict(X_text_test.values.reshape(-1, 1))
        predicted_text_classes = text_label_encoder.inverse_transform(predicted_text_classes)

        for predicted_class in np.unique(predicted_text_classes):
            print(predicted_class)
            mask = predicted_text_classes == predicted_class
            if predicted_class in ['lastname', 'firstname', 'middlename']:
                name_data = X_text_test.loc[mask].rename(columns={'0': predicted_class}).copy()
                sex_data = pd.DataFrame(np.random.choice([0, 1], size=sum(mask)), columns=['sex'],
                                        index=name_data.index)
                name_data = pd.concat([name_data, sex_data], axis=1)
                replaced_data = replace_data(name_data, predicted_class=predicted_class)
                X_text_test.loc[mask, '0'] = replaced_data.values
            else:
                replaced_data = replace_data(X_text_test.loc[mask, '0'], predicted_class=predicted_class)
                X_text_test.loc[mask, '0'] = replaced_data.values
        X_text_test.to_csv(args.output_text_raw_data_path, index=False)

        X_numb_test = pd.read_csv(args.input_raw_numb_data)
        predicted_numb_classes = numb_pipe.predict(X_numb_test.values.reshape(-1, 1))
        predicted_numb_classes = numb_label_encoder.inverse_transform(predicted_numb_classes)

        for predicted_class in np.unique(predicted_numb_classes):
            print(predicted_class)
            mask = predicted_numb_classes == predicted_class
            if predicted_class in ['lastname', 'firstname', 'middlename']:
                name_data = X_numb_test.loc[mask]
                sex_data = pd.DataFrame(np.random.choice([0, 1], size=sum(mask)), columns=['sex'])
                name_data = pd.concat([name_data, sex_data], axis=1)
                replaced_data = replace_data(name_data, predicted_class=predicted_class)
                X_numb_test.loc[mask, '0'] = replaced_data.values
            else:
                replaced_data = replace_data(X_numb_test.loc[mask, '0'], predicted_class=predicted_class)
                X_numb_test.loc[mask, '0'] = replaced_data.values
        X_numb_test.to_csv(args.output_numb_raw_data_path, index=False)
    else:
        raise ValueError("mode should be either 'tabular' or 'raw")
