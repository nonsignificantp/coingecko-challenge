import pickle
import time

import boto3
import numpy as np
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


class ScanIterator:
    def __init__(self, table, **kwargs):
        self.table = table
        self.kwargs = kwargs
        self.cursor = {}

    def __iter__(self):
        yield from self.next()

    def next(self):
        if self.cursor.get("ExclusiveStartKey") == StopIteration:
            raise StopIteration
        items, self.cursor = self.scan(self.cursor)
        return items

    def scan(self, cursor):
        response = self.table.scan(**self.kwargs, **cursor)
        return self._parse(**response)

    def _parse(self, *, Items, LastEvaluatedKey=StopIteration, **kwargs):
        return Items, {"ExclusiveStartKey": LastEvaluatedKey}


class S3Object:
    client = boto3.client("s3")

    def __init__(self, bucket, key):
        self.bucket = bucket
        self.key = key

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        ...

    def put(self, payload):
        self.client.put_object(Bucket=self.bucket, Key=self.key, Body=payload)

    def get(self):
        try:
            return self.client.get_object(Bucket=self.bucket, Key=self.key)
        except ClientError:
            return None

    def get_model(self):
        if model := self.get():
            return pickle.load(self.get()["Body"])
        return None

    def put_model(self, model):
        self.put(pickle.dumps(model))

    def _parse(self, response):
        ...


class DynamoTable:
    client = boto3.resource("dynamodb")

    def __init__(self, table):
        self.table = self.client.Table(table)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        ...

    def put_item(self, item):
        self.table.put_item(Item=dict(item))

    def put_items(self, items):
        for item in items:
            self.put_item(item)

    def get_training_data(self, window):
        items = ScanIterator(
            self.table,
            ProjectionExpression="coin_id,epoch,price",
            FilterExpression=(
                Key("currency").eq("usd")
                & Key("epoch").gte(int(time.time() - window))
            ),
        )
        return self._parse(items)

    def _parse(self, items):
        def _item(coin_id, epoch, price):
            return int(coin_id), int(epoch), float(price)

        data = np.array([_item(**d) for d in items])
        return data[:, :-1], data[:, -1]
