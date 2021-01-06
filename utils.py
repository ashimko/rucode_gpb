import pickle


def load_from_pickle(path: str):
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model


def save_to_pickle(model, path):
    with open(path, 'wb') as f:
        pickle.dump(model, f)
