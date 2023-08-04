import numpy as np
import pytest

from app.models import PredictRequest


class TestPredictRequestModel:
    def test_request_init(self, model):
        assert isinstance(model, PredictRequest)

    def test_request_attr_coin_id(self, model):
        assert model.body.coin_id == 0

    def test_request_features_len(self, model):
        assert len(model.features) == 1

    def test_request_features_type(self, model):
        assert isinstance(model.features, np.ndarray)

    def test_request_features_elements(self, model):
        assert len(model.features[0]) == 2

    def test_model_has_epoch(self, model):
        assert isinstance(model.body.epoch, int)

    def test_always_success(self):
        assert True

    @pytest.fixture
    def model(self):
        return PredictRequest(body='{"coin_id": "bitcoin"}')
