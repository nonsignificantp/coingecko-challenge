from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import OneHotEncoder

from .clients import DynamoTable
from .environ import STORAGE_TABLE
from .pipelines import CosineTransformer, SineTransformer

time_encoder = FeatureUnion(
    [
        ("time_sin_fn", SineTransformer()),
        ("time_cos_fn", CosineTransformer()),
    ]
)

compose = ColumnTransformer(
    [
        ("encoder", OneHotEncoder(), [0]),
        ("time_sin_fn", SineTransformer(), [1]),
        ("time_cos_fn", CosineTransformer(), [1]),
    ]
)

pipeline = Pipeline(
    steps=[("feature_creation", compose), ("linear_model", LinearRegression())]
)


def train_model(window):
    with DynamoTable(STORAGE_TABLE) as table:
        X, y = table.get_training_data(window=window)
    model = pipeline.fit(X, y)
    return model
