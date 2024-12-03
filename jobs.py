from models import Record
from services import Redis
import json


def update_data():
    record = Record.fetch_or_crawl()
    redis = Redis.client()
    result = redis.setex("data", 60, json.dumps(record.serializer_redis()))
    print(result)


if __name__ == "__main__":
    update_data()
