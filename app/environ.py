import os

API_KEY = os.getenv("COINGECKO_API_KEY")
STORAGE_TABLE = os.getenv("AWS_DYNAMO_TABLE", "coingecko-coin-prices")
REGISTRY = os.getenv("AWS_S3_BUCKET", "coingecko-registry-sandbox")
