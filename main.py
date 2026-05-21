import asyncio
from utils.log import Logger
from producer.producer import run_scrapers
from db.all_fixtures import get_fixtures

LOG = Logger("Main")


asyncio.run(run_scrapers())
