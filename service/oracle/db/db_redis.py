from service.oracle.config.settings import SNAPSHOTS_DIR
import redis.asyncio as redis
from service.oracle.utils.log import Logger
import os
import shutil
from service.oracle.config.settings import LIVE_HOST, LIVE_PORT

LOG = Logger("RedisDB", "db")


def sanitize_value(field_name: str, value) -> str:
    """Ensure that value is converted to a string and gets a sensible default if empty/None/null."""
    if value is None:
        val_str = ""
    elif isinstance(value, bool):
        val_str = "true" if value else "false"
    else:
        val_str = str(value).strip()

    # Normalize uppercase booleans
    if val_str == "True":
        val_str = "true"
    elif val_str == "False":
        val_str = "false"

    if not val_str or val_str.lower() in ("none", "null", ""):
        lower_field = field_name.lower()
        if "name" in lower_field or "news" in lower_field or "status" in lower_field or "code" in lower_field:
            return "None"
        if "time" in lower_field or "date" in lower_field:
            return "1970-01-01"
        if "form" in lower_field or "points" in lower_field or "cost" in lower_field or "value" in lower_field or "ict" in lower_field or "influence" in lower_field or "creativity" in lower_field or "threat" in lower_field or "expected" in lower_field or "xG" in lower_field or "xA" in lower_field or "xP" in lower_field or "xp" in lower_field or "percent" in lower_field:
            if any(kw in lower_field for kw in ("cost", "value", "percent", "xg", "xa", "xp", "ict", "influence", "creativity", "threat")):
                return "0.0"
            return "0"
        if "order" in lower_field or "rank" in lower_field or "played" in lower_field or "wins" in lower_field or "draws" in lower_field or "losses" in lower_field or "goals" in lower_field or "assists" in lower_field or "clean" in lower_field or "conceded" in lower_field or "saves" in lower_field or "starts" in lower_field or "yellow" in lower_field or "red" in lower_field or "bonus" in lower_field or "bps" in lower_field:
            return "0"
        return "0"

    return val_str


class RedisDB:
    def __init__(self):
        self.client_raw = redis.Redis(host=LIVE_HOST, port=LIVE_PORT, db=0)
        self.client_proc = redis.Redis(host=LIVE_HOST, port=LIVE_PORT, db=1)

        self.d_path = None
        self.c_path = None

    # ---------------------------------------------------------
    # RAW SNAPSHOT DUMP
    # ---------------------------------------------------------

    async def dump_raw(self):
        LOG.info("Starting Redis SAVE for raw DB...")

        await self.client_raw.save()
        LOG.info("Redis SAVE completed.")

        file_config = await self.client_raw.config_get("dbfilename")
        db_file = file_config["dbfilename"]

        season = await self.hget_one("status", "season")
        gw = await self.hget_one("status", "current")

        n_path = str(SNAPSHOTS_DIR / db_file)
        c_path = str(SNAPSHOTS_DIR / str(season) / str(gw))

        LOG.info(f"Dump file located at: {n_path}")
        LOG.info(f"Copying dump to: {c_path}")

        os.makedirs(c_path, exist_ok=True)

        shutil.copy(n_path, c_path)

        LOG.info("Redis dump copied successfully.")

    # ---------------------------------------------------------
    # CLIENT SELECTOR
    # ---------------------------------------------------------

    def _select(self, key: str):
        return self.client_proc if key.startswith("proc_") else self.client_raw

    # ---------------------------------------------------------
    # BASIC COMMANDS
    # ---------------------------------------------------------

    async def flush_raw(self):
        LOG.info("Flushing RAW DB...")
        await self.client_raw.flushdb()

    async def flush_proc(self):
        LOG.info("Flushing PROC DB...")
        await self.client_proc.flushdb()

    async def delete(self, db):
        client = self._select(db)
        await client.delete(db)
        LOG.info(f"Deleted key: {db}")

    # ---------------------------------------------------------
    # HASH COMMANDS
    # ---------------------------------------------------------

    async def hset_one(self, db, key, value):
        client = self._select(db)
        await client.hset(db, key, sanitize_value(key, value))

    async def hset_dict(self, db, dicts, subDB=None):
        client = self._select(db)
        async with client.pipeline(transaction=True) as pipe:
            for k, v in dicts.items():
                field = f"{subDB}.{k}" if subDB else k
                pipe.hset(db, field, sanitize_value(k, v))
            await pipe.execute()

    async def hset_all(self, db, data):
        client = self._select(db)
        sanitized_data = {k: sanitize_value(k, v) for k, v in data.items()}
        await client.hset(db, mapping=sanitized_data)

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

    # ---------------------------------------------------------
    # SCAN / KEYS / LISTS
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # SET COMMANDS
    # ---------------------------------------------------------

    async def sadd_one(self, db, member):
        client = self._select(db)
        await client.sadd(db, member)

    async def sadd_all(self, db, memberls):
        client = self._select(db)
        await client.sadd(db, *memberls)

    async def smembers(self, db):
        client = self._select(db)
        return await client.smembers(db)

    # ---------------------------------------------------------
    # ZSET COMMANDS
    # ---------------------------------------------------------

    async def zadd(self, db, score, member):
        client = self._select(db)
        await client.zadd(db, {member: score})

    async def zrange(self, db, start, stop, withscores=False):
        client = self._select(db)
        return await client.zrange(db, start, stop, withscores=withscores)

    async def zrevrange(self, db, start, stop, withscores=False):
        client = self._select(db)
        return await client.zrevrange(db, start, stop, withscores=withscores)

    async def zrangebyscore(self, db, min_score, max_score, withscores=False):
        client = self._select(db)
        return await client.zrangebyscore(
            db, min_score, max_score, withscores=withscores
        )

    async def zrem(self, db, member):
        client = self._select(db)
        await client.zrem(db, member)

    async def zscore(self, db, member):
        client = self._select(db)
        return await client.zscore(db, member)
