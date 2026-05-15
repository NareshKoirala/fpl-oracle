import redis
from utils.log import Logger

LOG = Logger("RedisDB")

class RedisDB:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def hset_one(self, db, key, value):
        self.client.hset(f"{db}", key, value)

    def hset_all(self, db, data):
        self.client.hset(f"{db}", mapping=data)

    def hget_all(self, db):
        byte_data = self.client.hgetall(f"{db}")
        return {k.decode(): v.decode() for k,v in byte_data.items()}
    