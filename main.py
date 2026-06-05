import asyncio
from utils.log import Logger
from producer.producer import run_producer
from cook.cook import run_cook
from utils.redis_server import start_live_server

LOG = Logger("Main")


async def main():
    LOG.info("Main Started...")
    start_live_server()
    asyncio.create_task(run_producer())
    asyncio.create_task(run_cook())
    await asyncio.Event().wait()  # keep loop alive


asyncio.run(main())
