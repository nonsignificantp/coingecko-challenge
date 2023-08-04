import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class SineTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return np.sin(X)


class CosineTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return np.cos(X)
