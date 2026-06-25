import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import asyncio
from service.oracle.utils.log import Logger
from service.oracle.producer.producer import run_producer
from service.oracle.cook.cook import run_cook
from service.oracle.utils.redis_server import start_live_server

LOG = Logger("Main")


async def main():
    LOG.info("Main Started...")
    start_live_server()
    asyncio.create_task(run_producer())
    asyncio.create_task(run_cook())
    await asyncio.Event().wait()  # keep loop alive


asyncio.run(main())
