"""
Light GBM wrapper to simplify early stopping

@author: Francesco Baldisserri
@creation date: 24/9/2021
"""

from lightgbm import LGBMRegressor, LGBMClassifier
from sklearn.model_selection import train_test_split


class LGBMRegressorWrapper(LGBMRegressor):
    def fit(self, x, y):
        x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2)
        return super().fit(x_train, y_train, eval_set=[(x_val, y_val)],
                           early_stopping_rounds=int(self.n_estimators**0.5),
                           verbose=False)


class LGBMClassifierWrapper(LGBMClassifier):
    def fit(self, x, y):
        x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2)
        return super().fit(x_train, y_train, eval_set=[(x_val, y_val)],
                           early_stopping_rounds=int(self.n_estimators**0.5),
                           verbose=False)