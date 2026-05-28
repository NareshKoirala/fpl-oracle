import requests
from utils.log import Logger
from utils.pw_browser_async import PlayWright_async_Browser
import httpx

LOG = Logger("Scraper", "utils")


class Scraper:
    def __init__(self):
        self.url = None
        self.enablePW = None
        self.browser = None

    async def enable_playwright(self):
        """Enable Playwright for this instance."""
        if not self.enablePW:
            LOG.info("Enabling Playwright for this Scraper instance.")
            self.enablePW = True
            self.browser = (
                await PlayWright_async_Browser.create()
            )  # Initialize the browser when enabling
        else:
            LOG.info("Playwright is already enabled for this Scraper instance.")

    # 1. Change to 'async def'
    async def fetch_request(self, url: str) -> dict:
        """Fetches data using httpx library (non-blocking)."""

        if url:
            LOG.info(f"Updating URL from: {self.url} to: {url}")
            self.url = url  # Update URL if provided

        async with httpx.AsyncClient() as client:
            response = await client.get(url)  # 3. 'await' the network call

            if response.status_code == 200:
                LOG.info(f"Data fetched successfully from: {self.url}")
                return response.json()  # Return the data directly
            else:
                LOG.error(f"Error fetching data: {response.status_code}")
                return None

    async def fetch_playwright(self, tag: str, url: str = None):
        """Fetches data using Playwright."""
        if not self.enablePW:
            LOG.error("This instancee doesnt have PlayWright enabled")
            return None

        content = await self.browser.get_content(tag)

        if content:
            return Scraper.BeautifulSoup_Parse(content, "html.parser")
        else:
            LOG.error("Failed to fetch content with Playwright.")
            return None

    @classmethod
    def BeautifulSoup_Parse(cls, content, parser: str):
        """Utility method to parse HTML content with BeautifulSoup."""
        from bs4 import BeautifulSoup

        try:
            soup = BeautifulSoup(content, parser)
            return soup
        except Exception as e:
            LOG.error(f"Error parsing content: {e}")
            return None

    async def close_browser(self):
        """Close the browser instance."""
        if not self.enablePW:
            LOG.info("This instancee does not have PlayWright enabled")
            return None
        LOG.info("Closing Scraper instance.")
        await self.browser.shutdown_engine()  # Close the browser instance when done

    async def close_page(self):
        """Close the page for this instance."""
        if not self.enablePW:
            LOG.info("This instancee does not have PlayWright enabled")
            return None
        LOG.info("Closing Scraper page.")
        await self.browser.close_page()  # Close the page when done

    async def page_load(self, url: str):
        """Utility method to load a new page."""
        if not self.enablePW:
            LOG.info("This instancee does not have PlayWright enabled")
            return None
        LOG.info(f"Loading page: {url}")
        await self.browser.page_load(url)  # Load the page when needed

    async def click_element(self, selector: str):
        """Utility method to click an element by selector."""
        if not self.enablePW:
            LOG.info("This instancee does not have PlayWright enabled")
            return None
        LOG.info(f"Clicking element with selector: {selector}")
        await self.browser.click_element(selector)  # Click the element when needed

    async def get_element(self, selector: str):
        """Utility method to get an element by selector."""
        if not self.enablePW:
            LOG.info("This instancee does not have PlayWright enabled")
            return None
        LOG.info(f"Getting element with selector: {selector}")
        return await self.browser.get_element(selector)  # Get the element when needed

    async def page_reload(self):
        """Utility method to reload the current page."""
        if not self.enablePW:
            LOG.info("This instancee does not have PlayWright enabled")
            return None
        LOG.info("Reloading page.")
        await self.browser.page_reload()  # Reload the page when needed
