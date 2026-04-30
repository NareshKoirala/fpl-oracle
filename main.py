import asyncio
from utils.log import Logger
from producer.producer import run_scrapers


LOG = Logger("Main")

asyncio.run(run_scrapers())
