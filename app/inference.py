import pickle
from pathlib import Path

from .clients import S3Object
from .environ import REGISTRY


class Artifact:
    base = Path(__file__).parent

    def __new__(cls, tag):
        with S3Object(REGISTRY, tag) as registry:
            model = registry.get_model()
        return model


class ModelRegistry:
    artifact = Artifact("models/latest")

    def __init__(self, key):
        self.key = key

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        ...

    def predict(self, X):
        return self.artifact.predict(X)[0]

    def put_model(self, model):
        with S3Object(REGISTRY, self.key) as registry:
            registry.put_model(model)
