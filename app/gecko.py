import requests

from .models import Price


def output(model):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            response = fn(*args, **kwargs)
            return model.from_response(response.json())

        return wrapper

    return decorator


class CoinGecko:
    endpoint = "https://api.coingecko.com/api/v3/%s"

    def __init__(self, api_key):
        self.api_key = api_key

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        ...

    @output(model=Price)
    def get_price(self, coins, currencies):
        return self.call(
            "GET", "simple/price", ids=coins, vs_currencies=currencies
        )

    def call(self, method, resource, **params):
        return requests.request(method, self.url(resource), params=params)

    def url(self, resource):
        return self.endpoint % resource
