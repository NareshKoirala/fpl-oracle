import asyncio
import random as rand
import time
import os
from utils.log import Logger
from config.settings import HEAD, BROWSER_WAIT_TIME, AGENT
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

LOG = Logger("PlayWright_Browser_Async")


class PlayWright_async_Browser:
    _playwright_manager = None
    _shared_browser = None
    _user_data_dir = "./playwright_pantry_session"

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

            cls._shared_browser = context
            # Apply stealth to the shared context ONCE
            await Stealth().apply_stealth_async(cls._shared_browser)

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
        # Use the shared persistent context
        self.context = self.__class__._shared_browser

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
        for _ in range(rand.randint(1, 4)):
            x = rand.randint((-self.width // 4), self.width // 4)
            y = rand.randint((-self.height // 4), self.height // 4)
            # Move mouse with 'steps' to avoid teleportation

            self.width = self.width // 2 + x
            self.height = self.height // 2 + y

            await self.page.mouse.move(
                self.width, self.height, steps=rand.randint(10, 20)
            )
            await asyncio.sleep(rand.uniform(0.1, 0.5))

    async def get_content(self, url, tag: str, label: str = None, click: bool = False):
        try:
            await self.page.goto(url)
            await self.page.wait_for_selector(
                tag, timeout=BROWSER_WAIT_TIME
            )  # Wait for the specific tag to load

            if label:
                await self.page.get_by_label(
                    label
                ).click()  # Click the label if provided
                LOG.info(f"Content loaded for {label} at URL: {url}")

            if click and not label:
                await self.page.click(
                    'button svg use[href$="icn-chevron-right"]'
                )  # Click the tag if click is True and no label
                LOG.info(f"Content loaded and clicked for tag: {tag} at URL: {url}")
            
            await asyncio.sleep(rand.uniform(3, 5))  # Random sleep after click
            return await self.page.content()
        except Exception as e:
            LOG.error(f"Scrape failed: {e}")
            return None


