import requests
from utils.log import Logger
from utils.pw_browser import PlayWright_Browser

LOG = Logger("Scraper")


class Scraper:
    def __init__(self, url: str, enablePW: bool):
        self.url = url
        self.enablePW = enablePW
        
        if enablePW:
            self.browser = PlayWright_Browser()  # Initialize the browser instance
            
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

    def fetch_playwright(self, tag: str, url: str = None):
        if not self.enablePW:
            LOG.error("This instancee doesnt have PlayWright enabled")
            return None
        
        if url:
            LOG.info(f"Updating URL from: {self.url} to: {url}")
            self.url = url  # Update URL if provided

        content = self.browser.get_content(self.url, tag)

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

    def close(self):
        if not self.enablePW:
            LOG.info("This instancee with no PlayWright is closed")
            return None
        LOG.info("Closing Scraper instance.")
        self.browser.close_instance()  # Close the browser instance when done

    def __del__(self):
        LOG.info("Scraper instance destroyed.")
        self.close()  # Ensure browser is closed when the Scraper instance is destroyed
