from service.oracle.utils.log import Logger
from service.oracle.utils.pw_browser_async import PlayWright_async_Browser
import httpx

LOG = Logger("Scraper", "utils")


class Scraper:
    def __init__(self):
        self.url = None
        self.enablePW = None
        self.browser = None

    # ---------------------------------------------------------
    # PLAYWRIGHT ENABLE
    # ---------------------------------------------------------

    async def enable_playwright(self):
        if not self.enablePW:
            LOG.info("\n========== ENABLING PLAYWRIGHT FOR SCRAPER ==========")
            self.enablePW = True
            self.browser = await PlayWright_async_Browser.create()
            LOG.info("Playwright enabled for this Scraper instance.\n")
        else:
            LOG.info("Playwright already enabled for this Scraper instance.")

    # ---------------------------------------------------------
    # HTTPX FETCH
    # ---------------------------------------------------------

    async def fetch_request(self, url: str) -> dict:
        if url:
            LOG.info(f"\n========== HTTPX REQUEST ==========\nUpdating URL → {url}")
            self.url = url

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                LOG.info(f"HTTP GET → {url} | Status: {response.status_code}")

                if response.status_code == 200:
                    LOG.info("HTTPX fetch successful.\n")
                    return response.json()

                LOG.error(f"HTTPX fetch failed with status {response.status_code}\n")
                return None

            except Exception as e:
                LOG.error(f"HTTPX request error: {e}\n")
                return None

    # ---------------------------------------------------------
    # PLAYWRIGHT FETCH
    # ---------------------------------------------------------

    async def fetch_playwright(self, tag: str, url: str = None):
        if not self.enablePW:
            LOG.error("Playwright not enabled for this Scraper instance.")
            return None

        LOG.info(f"\n========== PLAYWRIGHT FETCH ==========\nSelector: {tag}")

        content = await self.browser.get_content(tag)

        if content:
            LOG.info("Playwright content fetched successfully. Parsing HTML...\n")
            return Scraper.BeautifulSoup_Parse(content, "html.parser")

        LOG.error("Playwright failed to fetch content.\n")
        return None

    # ---------------------------------------------------------
    # BEAUTIFULSOUP PARSER
    # ---------------------------------------------------------

    @classmethod
    def BeautifulSoup_Parse(cls, content, parser: str):
        from bs4 import BeautifulSoup

        try:
            soup = BeautifulSoup(content, parser)
            LOG.info("BeautifulSoup parsing successful.")
            return soup
        except Exception as e:
            LOG.error(f"BeautifulSoup parsing error: {e}")
            return None

    # ---------------------------------------------------------
    # BROWSER CONTROL
    # ---------------------------------------------------------

    async def close_browser(self):
        if not self.enablePW:
            LOG.info("Playwright not enabled — nothing to close.")
            return None

        LOG.info("\n========== CLOSING SCRAPER BROWSER ==========")
        await self.browser.shutdown_engine()
        LOG.info("Scraper browser closed.\n")

    async def close_page(self):
        if not self.enablePW:
            LOG.info("Playwright not enabled — no page to close.")
            return None

        LOG.info("Closing Scraper page...")
        await self.browser.close_page()
        LOG.info("Scraper page closed.\n")

    # ---------------------------------------------------------
    # PAGE ACTIONS
    # ---------------------------------------------------------

    async def page_load(self, url: str):
        if not self.enablePW:
            LOG.info("Playwright not enabled — cannot load page.")
            return None

        LOG.info(f"\n========== PAGE LOAD ==========\nURL → {url}")
        await self.browser.page_load(url)

    async def click_element(self, selector: str):
        if not self.enablePW:
            LOG.info("Playwright not enabled — cannot click element.")
            return None

        LOG.info(f"\n========== CLICK ELEMENT ==========\nSelector → {selector}")
        await self.browser.click_element(selector)

    async def get_element(self, selector: str):
        if not self.enablePW:
            LOG.info("Playwright not enabled — cannot get element.")
            return None

        LOG.info(f"\n========== GET ELEMENT ==========\nSelector → {selector}")
        return await self.browser.get_element(selector)

    async def page_reload(self):
        if not self.enablePW:
            LOG.info("Playwright not enabled — cannot reload page.")
            return None

        LOG.info("\n========== PAGE RELOAD ==========")
        await self.browser.page_reload()
