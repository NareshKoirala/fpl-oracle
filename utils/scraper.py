import requests
import asyncio
from utils.log import Logger
from utils.pw_browser_async import PlayWright_async_Browser

LOG = Logger("Scraper")


class Scraper:
    def __init__(self, url: str, enablePW: bool):
        self.url = url
        self.enablePW = enablePW
        self.browser = None
        
        LOG.info(f"Scraper initialized with URL: {self.url}, with PlayWright enabled: {enablePW}")

    def fetch_request(self, url: str = None) -> dict:
        if url:
            LOG.info(f"Updating URL from: {self.url} to: {url}")
            self.url = url  # Update URL if provided

        response = requests.get(self.url)

        if response.status_code == 200:
            LOG.info(f"Data fetched successfully from: {self.url}")
            return response
        else:
            LOG.error(f"Error fetching data: {response.status_code}")
            return None

    async def fetch_playwright(self, tag: str, url: str = None, label: str = None, click: bool = False):
        if not self.enablePW:
            LOG.error("This instancee doesnt have PlayWright enabled")
            return None
        
        self.browser = await PlayWright_async_Browser.create()  # Ensure the browser is initialized before fetching content
        
        if url:
            LOG.info(f"Updating URL from: {self.url} to: {url}")
            self.url = url  # Update URL if provided

        content = await self.browser.get_content(self.url, tag, label, click)

        if content:
            return Scraper.BeautifulSoup_Parse(content, "html.parser")
        else:
            LOG.error("Failed to fetch content with Playwright.")
            return None
        
    @classmethod
    def BeautifulSoup_Parse(cls, content, parser: str):
        from bs4 import BeautifulSoup

        try:
            soup = BeautifulSoup(content, parser)
            return soup
        except Exception as e:
            LOG.error(f"Error parsing content: {e}")
            return None

    async def close(self):
        if not self.enablePW:
            LOG.info("This instancee does not have PlayWright enabled")
            return None
        LOG.info("Closing Scraper instance.")
        await self.browser.shutdown_engine()  # Close the browser instance when done

    async def close_page(self):
        if not self.enablePW:
            LOG.info("This instancee does not have PlayWright enabled")
            return None
        LOG.info("Closing Scraper page.")
        await self.browser.close_page()  # Close the page when done