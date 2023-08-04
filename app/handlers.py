from .clients import DynamoTable
from .environ import API_KEY, STORAGE_TABLE
from .gecko import CoinGecko
from .inference import ModelRegistry
from .models import PredictRequest, PriceRequest, Response, TrainRequest
from .training import train_model


def event_to_request(model):
    def decorator(fn):
        def wrapper(request, *args, **kwargs):
            return fn(model(**request), *args, **kwargs)

        return wrapper

    return decorator


@event_to_request(model=PriceRequest)
def prices(request, context):
    api = CoinGecko(api_key=API_KEY)
    items = api.get_price(request.coins, request.currencies)
    with DynamoTable(table=STORAGE_TABLE) as table:
        table.put_items(items)


@event_to_request(model=TrainRequest)
def train(request, context):
    model = train_model(request.window)
    with ModelRegistry("models/latest") as registry:
        registry.put_model(model)


@event_to_request(model=PredictRequest)
def predict(request, context):
    with ModelRegistry("models/latest") as registry:
        yhat = registry.predict(request.features)
    return Response(body=yhat).dict()
