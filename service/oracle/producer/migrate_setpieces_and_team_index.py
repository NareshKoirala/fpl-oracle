import asyncio
import redis.asyncio as redis
from service.oracle.config.settings import LIVE_HOST, LIVE_PORT
from service.oracle.utils.log import Logger

LOG = Logger("Migration", "producer")

async def run_migration():
    LOG.info("Starting Redis DB 0 data standard migration...")
    r = redis.Redis(host=LIVE_HOST, port=LIVE_PORT, db=0, decode_responses=True)
    
    # 1. Migrate set-piece order values of "0" to ""
    metas = await r.keys("player:*:meta")
    set_pieces_migrated = 0
    
    for mkey in metas:
        vals = await r.hgetall(mkey)
        updates = {}
        for field in ("penalties_order", "direct_freekicks_order", "corners_and_indirect_freekicks_order"):
            if vals.get(field) == "0":
                updates[field] = ""
        
        if updates:
            await r.hset(mkey, mapping=updates)
            set_pieces_migrated += 1
            
    LOG.info(f"Set-piece order fields migrated for {set_pieces_migrated} players.")

    # 2. Copy index:team:{name} to index:team_name:{name}
    team_indices = await r.keys("index:team:*")
    indices_copied = 0
    
    for tkey in team_indices:
        # Avoid double-matching if there are already index:team_name:* keys
        if tkey.startswith("index:team_name:"):
            continue
            
        name = tkey.split("index:team:")[-1]
        tid = await r.hget(tkey, "tid")
        if tid:
            dest_key = f"index:team_name:{name}"
            await r.hset(dest_key, "tid", tid)
            indices_copied += 1
            
    LOG.info(f"Team indexes copied: {indices_copied} indexes mapped.")
    
    # Save the updated DB
    LOG.info("Saving raw database snapshot...")
    await r.save()
    LOG.info("Migration complete!")
    await r.aclose()

if __name__ == "__main__":
    asyncio.run(run_migration())
