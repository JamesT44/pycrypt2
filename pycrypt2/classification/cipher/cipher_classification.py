import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
import pandas as pd
from joblib import dump, load
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier

from pycrypt_statistics import Statistics


class CipherClassifier(object):
    def __init__(self, model_file="cipher_model.joblib", scaler_file="cipher_scaler.joblib", retrain=False,
                 training_file="cipher_reference_data.csv",
                 model=RandomForestClassifier(max_depth=13, n_estimators=100), stats_kwargs=None):
        self.model_file = os.path.join(os.path.dirname(__file__), model_file)
        self.scaler_file = os.path.join(os.path.dirname(__file__), scaler_file)
        if stats_kwargs is None:
            self.stats = Statistics()
        else:
            self.stats = Statistics(**stats_kwargs)
        if not retrain and os.path.exists(self.model_file) and os.path.exists(self.scaler_file):
            self.model = load(self.model_file)
            self.scaler = load(self.scaler_file)
        else:
            print("First time training model")
            dataframe = pd.read_csv(os.path.join(os.path.dirname(__file__), training_file))
            arr = dataframe.values
            x = arr[:, 1:]
            y = arr[:, 0]

            self.scaler = preprocessing.MinMaxScaler()
            x_scaled = self.scaler.fit_transform(x)
            self.model = model.fit(x_scaled, y)
            dump(self.model, self.model_file)
            dump(self.scaler, self.scaler_file)

    def identify(self, text):
        return list(sorted(zip(self.model.classes_, self.model.predict_proba(self.scaler.transform(np.array(
            self.stats.id_stats(text)).reshape(1, -1)))[0]), key=lambda x: x[1], reverse=True))


if __name__ == '__main__':
    CipherClassifier(retrain=True)
