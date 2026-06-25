import asyncio
import random as rand
import os
from time import time
from service.oracle.utils.log import Logger
from service.oracle.config.settings import HEAD, BROWSER_WAIT_TIME, SLOW_MOTION, PW_SESSION_DIR
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

LOG = Logger("PlayWright_Browser_Async", "utils")


class PlayWright_async_Browser:
    _playwright_manager = None
    _shared_browser = None
    _user_data_dir = str(PW_SESSION_DIR)

    def __init__(self):
        self.context = None
        self.page = None
        self.viewport = (1280, 720)

    # ---------------------------------------------------------
    # ENGINE CONTROL
    # ---------------------------------------------------------

    @classmethod
    async def shutdown_engine(cls):
        LOG.info("\n========== SHUTTING DOWN PLAYWRIGHT ENGINE ==========")

        if cls._shared_browser:
            await cls._shared_browser.close()
            cls._shared_browser = None
            LOG.info("Shared browser context closed.")

        if cls._playwright_manager:
            await cls._playwright_manager.stop()
            cls._playwright_manager = None
            LOG.info("Playwright manager stopped.")

        LOG.info("Playwright engine shutdown complete.\n")

    @classmethod
    async def _ensure_browser(cls):
        if cls._shared_browser is None:
            LOG.info("\n========== STARTING PLAYWRIGHT ENGINE ==========")

            cls._playwright_manager = await async_playwright().start()
            LOG.info("Playwright manager started.")

            if not os.path.exists(cls._user_data_dir):
                os.makedirs(cls._user_data_dir)
                LOG.info(f"Created user data directory: {cls._user_data_dir}")

            context = await cls._playwright_manager.chromium.launch_persistent_context(
                user_data_dir=cls._user_data_dir,
                headless=HEAD,
                args=["--disable-blink-features=AutomationControlled"],
            )

            cls._shared_browser = context
            LOG.info("Shared persistent browser context created.\n")

    @classmethod
    async def create(cls):
        LOG.info("\n========== CREATING NEW PLAYWRIGHT BOT ==========")

        await cls._ensure_browser()
        instance = cls()
        await instance._init_tab()

        LOG.info("Bot created successfully.\n")
        return instance

    # ---------------------------------------------------------
    # PAGE / TAB CONTROL
    # ---------------------------------------------------------

    async def close_page(self):
        if self.page:
            await self.page.close()
            LOG.info("Page closed.")
            self.page = None

    async def _init_tab(self):
        self.context = self._shared_browser
        self.page = await self.context.new_page()

        self.width = self.page.viewport_size["width"]
        self.height = self.page.viewport_size["height"]

        LOG.info(f"New page opened. Viewport: {self.width}x{self.height}")

    # ---------------------------------------------------------
    # HUMAN-LIKE MOUSE MOVEMENT
    # ---------------------------------------------------------

    async def random_mouse_movement(self):
        self.width = self.page.viewport_size["width"]
        self.height = self.page.viewport_size["height"]

        LOG.info("Performing random mouse movement...")

        for _ in range(rand.randint(2, 4)):
            x = rand.randint((-self.width // 3), self.width // 3)
            y = rand.randint((-self.height // 3), self.height // 3)

            self.width = self.width // 3 + x
            self.height = self.height // 3 + y

            await self.page.mouse.move(
                self.width, self.height, steps=rand.randint(10, 20)
            )
            await asyncio.sleep(SLOW_MOTION)

        LOG.info("Mouse movement complete.")

    # ---------------------------------------------------------
    # PAGE ACTIONS
    # ---------------------------------------------------------

    async def page_load(self, url: str):
        LOG.info(f"Loading page: {url}")

        try:
            await self.page.goto(url)
            LOG.info(f"Page loaded successfully → {url}")
        except Exception as e:
            LOG.error(f"Failed to load page {url}: {e}")

    async def page_reload(self):
        LOG.info("Reloading page...")

        try:
            await self.page.reload(wait_until="networkidle")
            LOG.info("Page reloaded successfully.")
        except Exception as e:
            LOG.error(f"Failed to reload page: {e}")

    # ---------------------------------------------------------
    # SCRAPING UTILITIES
    # ---------------------------------------------------------

    async def get_content(self, tag: str):
        LOG.info(f"Waiting for selector: {tag}")

        try:
            await self.page.wait_for_selector(tag, timeout=BROWSER_WAIT_TIME)
            await asyncio.sleep(SLOW_MOTION)

            LOG.info(f"Selector found: {tag}")
            return await self.page.content()

        except Exception as e:
            LOG.error(f"Failed to get content for selector {tag}: {e}")
            return None

    async def click_element(self, selector: str):
        LOG.info(f"Clicking element: {selector}")

        try:
            await self.page.click(selector)
            LOG.info(f"Clicked element: {selector}")
        except Exception as e:
            LOG.error(f"Failed to click element {selector}: {e}")

    async def get_element(self, selector: str):
        LOG.info(f"Getting element: {selector}")

        try:
            await self.page.wait_for_selector(selector, timeout=BROWSER_WAIT_TIME)
            element = await self.page.query_selector(selector)

            LOG.info(f"Element found: {selector}")
            return element

        except Exception as e:
            LOG.error(f"Failed to get element {selector}: {e}")
            return None
