from dotenv import load_dotenv
import os
from redis import StrictRedis

load_dotenv()


class Redis:
    @staticmethod
    def client():
        redis_url = os.getenv("REDIS_URL", "")
        client = StrictRedis.from_url(redis_url)
        return client
