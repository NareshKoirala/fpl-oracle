import asyncio
import random as rand
import os
from time import time
from utils.log import Logger
from config.settings import HEAD, BROWSER_WAIT_TIME, SLOW_MOTION
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

LOG = Logger("PlayWright_Browser_Async", "utils")


class PlayWright_async_Browser:
    _playwright_manager = None
    _shared_browser = None
    _user_data_dir = "./pw_session"

    def __init__(self):
        # Every 'bot' gets its own private variables
        self.context = None
        self.page = None
        self.viewport = (1280, 720)  # Default viewport size

    @classmethod
    async def shutdown_engine(cls):
        """Call this once at the very end of your program."""
        if cls._shared_browser:
            await cls._shared_browser.close()
            cls._shared_browser = None  # Clear the shared browser reference
        if cls._playwright_manager:
            await cls._playwright_manager.stop()
            cls._playwright_manager = None  # Clear the manager reference
        LOG.info("Browser engine shut down successfully.")

    @classmethod
    async def _ensure_browser(cls):
        if cls._shared_browser is None:
            LOG.info("Starting shared browser engine...")
            cls._playwright_manager = await async_playwright().start()

            if not os.path.exists(cls._user_data_dir):
                os.makedirs(cls._user_data_dir)
                
            # Persistent context = BrowserContext
            context = await cls._playwright_manager.chromium.launch_persistent_context(
                user_data_dir=cls._user_data_dir,
                headless=HEAD,
                args=["--disable-blink-features=AutomationControlled"],
            )
            # Apply stealth to the shared context ONCE
            await Stealth().apply_stealth_async(context)
            cls._shared_browser = context
            LOG.info("Shared browser engine started successfully.")

    @classmethod
    async def create(cls):
        """The only method the outside world should call to get a new bot."""
        await cls._ensure_browser()  # Step 1: Ensure the process exists

        instance = cls()  # Step 2: Create the worker object
        await instance._init_tab()  # Step 3: Open the tab
        return instance  # Step 4: Hand over the worker

    async def close_page(self):
        """Close the page for this instance."""
        if self.page:
            await self.page.close()
            self.page = None
            LOG.info("Page closed successfully.")

    async def _init_tab(self):
        """Opens a unique tab for this specific instance."""
        
        self.context = self._shared_browser  # Use shared context if not creating a new one
        
        # Each worker gets its own page
        self.page = await self.context.new_page()
        self.width, self.height = (
            self.page.viewport_size["width"],
            self.page.viewport_size["height"],
        )
        LOG.info("New Page with viewport size: {}x{}".format(self.width, self.height))

    async def random_mouse_movement(self):
        """Improved movement: jittery and purposeful."""
        self.width, self.height = (
            self.page.viewport_size["width"],
            self.page.viewport_size["height"],
        )
        for _ in range(rand.randint(2, 4)):
            x = rand.randint((-self.width // 3), self.width // 3)
            y = rand.randint((-self.height // 3), self.height // 3)
            # Move mouse with 'steps' to avoid teleportation

            self.width = self.width // 3 + x
            self.height = self.height // 3 + y

            await self.page.mouse.move(
                self.width, self.height, steps=rand.randint(10, 20)
            )
            await asyncio.sleep(SLOW_MOTION)  # Random sleep between movements

    async def page_load(self, url: str):
        """Utility method to load a new page."""
        try:
            await self.page.goto(url)
            LOG.info(f"Page loaded successfully. URL: {url if url else 'Current URL'}")
        except Exception as e:
            LOG.error(f"Failed to load page {url}: {e}")

    async def get_content(self, tag: str):
        try:
            await self.page.wait_for_selector(
                tag, timeout=BROWSER_WAIT_TIME
            )  # Wait for the specific tag to load

            await asyncio.sleep(SLOW_MOTION)  # Simulate human-like mouse movement

            return await self.page.content()
        except Exception as e:
            LOG.error(f"Scrape failed: {e}")
            return None

    async def click_element(self, selector: str):
        """Utility method to click an element by selector."""
        try:
            await self.page.click(selector)
            LOG.info(f"Clicked element with selector: {selector}")
        except Exception as e:
            LOG.error(f"Failed to click element {selector}: {e}")

    async def get_element(self, selector: str):
        """Utility method to get an element by selector."""
        try:
            await self.page.wait_for_selector(selector, timeout=BROWSER_WAIT_TIME)
            element = await self.page.query_selector(selector)
            LOG.info(f"Element found with selector: {selector}")
            return element
        except Exception as e:
            LOG.error(f"Failed to get element {selector}: {e}")
            return None

    async def page_reload(self):
        """Utility method to reload the current page."""
        try:
            await self.page.reload(wait_until="networkidle")
            LOG.info("Page reloaded successfully.")
        except Exception as e:
            LOG.error(f"Failed to reload page: {e}")
