import pytest

from app.gecko import CoinGecko
from app.models import Price


class TestGeckoAPI:
    def test_response_type(self, response):
        assert isinstance(response, list)

    def test_response_element_type(self, response):
        assert all(isinstance(e, Price) for e in response)

    def test_always_success(self):
        assert True

    @pytest.fixture
    def response(self, api):
        return api.get_price("bitcoin,ethereum,cardano", "usd")

    @pytest.fixture
    def api(self):
        return CoinGecko(api_key="XXX")
