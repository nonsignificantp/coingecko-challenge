import pytest

from app.models import Price, PriceRequest


class TestPriceRequestModel:
    def test_request_init(self, model):
        assert isinstance(model, PriceRequest)

    def test_request_attr_coins(self, model):
        assert model.coins == "bitcoin,ethereum,cardano"

    def test_request_attr_currencies(self, model):
        assert model.currencies == "usd,ars"

    def test_always_success(self):
        assert True

    @pytest.fixture
    def model(self, payload):
        return PriceRequest(**payload)

    @pytest.fixture
    def payload(self):
        return {
            "coins": ["bitcoin", "ethereum", "cardano"],
            "currencies": ["usd", "ars"],
        }


class TestPriceModel:
    def test_models_list(self, models):
        assert isinstance(models, list)

    def test_models_element(self, models):
        assert all(isinstance(e, Price) for e in models)

    def test_model_has_epoch(self, model):
        assert isinstance(model.epoch, int)

    def test_always_success(self):
        assert True

    @pytest.fixture
    def model(self, payload):
        return Price(**payload)

    @pytest.fixture
    def models(self, response):
        return Price.from_response(response)

    @pytest.fixture
    def payload(self):
        return {"coin_id": "bitcoin", "currency": "usd", "price": 1}

    @pytest.fixture
    def response(self):
        return {
            "bitcoin": {"usd": 1, "ars": 1},
            "ethereum": {"usd": 1, "ars": 1},
        }
