import asyncio
from utils.log import Logger
from producer.producer import run_scrapers
from cook.cook import run_cook

LOG = Logger("Main")

async def main():
    await asyncio.gather(run_scrapers(), run_cook())

asyncio.run(main())
