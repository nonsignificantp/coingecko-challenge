import json
import time
from decimal import Decimal
from enum import IntEnum
from typing import Callable

import numpy as np
from pydantic import BaseModel, root_validator, validator


class Coins(IntEnum):
    bitcoin = 0
    ethereum = 1
    cardano = 2


class PriceRequest(BaseModel):
    coins: str
    currencies: str = "usd"

    @validator("coins", "currencies", pre=True)
    def comma_join_values(cls, v):
        return ",".join(v)


class TrainRequest(BaseModel):
    window: int


class Predict(BaseModel):
    coin_id: int
    epoch: int = time.time

    @validator("coin_id", pre=True)
    def coin_name_to_id(cls, v):
        return Coins[v].value

    @validator("epoch", pre=True, always=True)
    def add_epoch(cls, v):
        if isinstance(v, Callable):
            return int(v())
        return int(v)


class PredictRequest(BaseModel):
    body: Predict

    @validator("body", pre=True)
    def json_to_dict(cls, v):
        return json.loads(v)

    @property
    def features(self):
        return np.array([[v for _, v in self.body]])


class Price(BaseModel):
    coin_id: int
    currency: str
    price: Decimal
    epoch: int = time.time

    @validator("coin_id", pre=True)
    def coin_name_to_id(cls, v):
        return Coins[v].value

    @validator("epoch", pre=True, always=True)
    def add_epoch(cls, v):
        if isinstance(v, Callable):
            return int(v())
        return int(v)

    @staticmethod
    def from_response(response):
        def _parse(response):
            for k, data in response.items():
                for c, price in data.items():
                    yield {"coin_id": k, "currency": c, "price": price}

        return [Price(**data) for data in _parse(response)]


class Response(BaseModel):
    statusCode: int = 200
    headers: dict = {"Content-Type": "application/json"}
    body: str

    @validator("body", pre=True)
    def body_to_json(cls, v):
        return json.dumps(v)
