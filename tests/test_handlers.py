import json

import pytest

from app.handlers import predict, train


class TestTrainHandler:
    def test_always_success(self, event):
        response = train(event, context=None)
        assert response is None

    @pytest.fixture
    def event(self):
        return {"window": 3600}


class TestPredictHandler:
    @pytest.mark.parametrize("coin", ["bitcoin", "ethereum", "cardano"])
    def test_always_success(self, coin):
        response = predict(self.payload(coin), context=None)
        assert response["statusCode"] == 200

    def payload(self, coin):
        return {"body": json.dumps({"coin_id": coin})}
