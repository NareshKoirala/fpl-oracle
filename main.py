import asyncio
from utils.log import Logger
from producer.producer import run_producer
from cook.cook import run_cook

LOG = Logger("Main")

async def main():
    LOG.info("Main Started...")
    asyncio.create_task(run_producer())
    asyncio.create_task(run_cook())
    await asyncio.Event().wait()  # keep loop alive


asyncio.run(main())
