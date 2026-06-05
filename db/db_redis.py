import redis.asyncio as redis
from utils.log import Logger
import os
import shutil
from config.settings import LIVE_HOST, LIVE_PORT

LOG = Logger("RedisDB", "db")


class RedisDB:
    def __init__(self):
        self.client_raw = redis.Redis(host=LIVE_HOST, port=LIVE_PORT, db=0)
        self.client_proc = redis.Redis(host=LIVE_HOST, port=LIVE_PORT, db=1)

        self.d_path = None
        self.c_path = None

    async def dump_raw(self):
        await self.client_raw.save()

        file_config = await self.client_raw.config_get("dbfilename")

        season = await self.hget_one(f"current_gw", "season")
        gw = await self.hget_one(f"current_gw", "current")

        n_path = os.path.join(os.getcwd(), f"snapshots/{file_config["dbfilename"]}")
        c_path = os.path.join(os.getcwd(), f"snapshots/{season}/{gw}/")

        os.makedirs(c_path, exist_ok=True)

        shutil.copy(n_path, c_path)

    def _select(self, db: str):
        return self.client_proc if db[0] == "p" else self.client_raw

    async def flush_raw(self):
        await self.client_raw.flushdb()

    async def flush_proc(self):
        await self.client_proc.flushdb()

    async def delete(self, db):
        client = self._select(db)
        await client.delete(db)

    async def hset_one(self, db, key, value):
        client = self._select(db)
        await client.hset(db, key, value)

    async def hset_dict(self, db, dicts, subDB=None):
        client = self._select(db)
        async with client.pipeline(transaction=True) as pipe:
            for k, v in dicts.items():
                field = f"{subDB}.{k}" if subDB else k
                pipe.hset(db, field, str(v))
            await pipe.execute()

    async def hset_all(self, db, data):
        client = self._select(db)
        await client.hset(db, mapping=data)

    async def hget_all(self, db):
        client = self._select(db)
        byte_data = await client.hgetall(db)
        return {k.decode(): v.decode() for k, v in byte_data.items()}

    async def hget_one(self, db, field):
        client = self._select(db)
        result = await client.hget(db, field)
        return result.decode() if result else None

    async def hscan_section(self, db, section):
        client = self._select(db)
        cursor, byte_data = await client.hscan(db, match=f"{section}.*")
        return {k.decode(): v.decode() for k, v in byte_data.items()}

    async def scan(self, prefix, cursor):
        client = self._select(prefix)
        return await client.scan(cursor, match=prefix)

    async def db_size(self, db):
        client = self._select(db)
        return await client.dbsize()

    async def rpush(self, db, data):
        client = self._select(db)
        await client.rpush(db, data)

    async def get_keys(self, pattern):
        client = self._select(pattern)
        return await client.keys(pattern)

    async def lrange(self, db, start, stop):
        client = self._select(db)
        return await client.lrange(db, start, stop)
