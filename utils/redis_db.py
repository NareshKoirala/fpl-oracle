import redis
from utils.log import Logger

LOG = Logger("RedisDB")

class RedisDB:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def set(self, key: str, value: str):
        self.client.set(key, value)

    def get(self, key: str) -> str:
        return self.client.get(key).decode('utf-8') if self.client.get(key) else None

    def delete(self, key: str):
        self.client.delete(key)