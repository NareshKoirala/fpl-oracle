import redis.asyncio as redis  # Note: Use redis.asyncio
from utils.log import Logger

LOG = Logger("RedisDB")

class RedisDB:
    def __init__(self, host='localhost', port=6379, db=0):
        # Redis.from_url is preferred for async clients
        self.client = redis.Redis(host=host, port=port, db=db)

    async def hset_one(self, db, key, value):
        await self.client.hset(db, key, value)
        
    async def hset_dict(self, db, dicts, subDB=None):
        if not subDB:
            return await self.hset_all(db, dicts)

        # Use async pipeline
        async with self.client.pipeline(transaction=True) as pipe:
            for k, v in dicts.items():
                pipe.hset(db, f"{subDB}.{k}", str(v))
            await pipe.execute()

    async def hset_all(self, db, data):
        await self.client.hset(db, mapping=data)

    async def hget_all(self, db):
        byte_data = await self.client.hgetall(db)
        # Decoding remains synchronous/CPU-bound, which is fine
        return {k.decode(): v.decode() for k, v in byte_data.items()}
    
    async def hget_one(self, db, field):
        result = await self.client.hget(db, field)
        return result.decode() if result else None

    async def scan(self, prefix, cursor):
        return await self.client.scan(cursor, match=prefix)

    async def hscan_section(self, db, section):
        cursor, byte_data = await self.client.hscan(db, match=f"{section}.*")
        return {k.decode(): v.decode() for k, v in byte_data.items()}

    async def db_size(self):
        return await self.client.dbsize()