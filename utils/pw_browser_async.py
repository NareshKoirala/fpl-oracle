import asyncio
import random as rand
import os
from utils.log import Logger
from utils.settings import HEAD, BROWSER_WAIT_TIME, AGENT
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

    @classmethod
    def shutdown_engine(cls):
        """Call this once at the very end of your program."""
        if cls._shared_browser:
            cls._shared_browser.close()
        if cls._playwright_manager:
            cls._playwright_manager.stop()
        LOG.info("Browser engine shut down successfully.")

    @classmethod
    async def _ensure_browser(cls):
        """Private helper to make sure the engine is running."""
        if cls._shared_browser is None:
            LOG.info("Starting shared browser engine...")
            cls._playwright_manager = await async_playwright().start()
            if not os.path.exists(cls._user_data_dir):
                os.makedirs(cls._user_data_dir)
            
            # We use launch_persistent_context instead of chromium.launch
            cls.context = await cls._playwright_manager.chromium.launch_persistent_context(
                user_data_dir=cls._user_data_dir,
                headless=HEAD, 
                args=[
                    "--disable-blink-features=AutomationControlled",
                ]
            )
            # This context stays open, and we create pages from it
            cls._shared_browser = cls.context

    @classmethod
    async def create(cls):
        """The only method the outside world should call to get a new bot."""
        await cls._ensure_browser()  # Step 1: Ensure the process exists

        instance = cls()  # Step 2: Create the worker object
        await instance._init_tab()  # Step 3: Open the tab
        return instance  # Step 4: Hand over the worker

    async def _init_tab(self):
        """Opens a unique tab for this specific instance."""
        # Note: we access the class variable _shared_browser here
        self.stealth = Stealth()
        self.context = await self._shared_browser.new_context(user_agent=AGENT)
        await Stealth().apply_stealth_async(self.context)
        self.page = await self.context.new_page()
        
    async def random_mouse_movement(self):
        """Improved movement: jittery and purposeful."""
        for _ in range(rand.randint(2, 5)):
            x = rand.randint(100, 700)
            y = rand.randint(100, 700)
            # Move mouse with 'steps' to avoid teleportation
            await self.page.mouse.move(x, y, steps=rand.randint(5, 15))
            await asyncio.sleep(rand.uniform(0.1, 0.5))

    async def failed_page(self):
        await self.page.go_back()
        await self.random_mouse_movement()
        await self.page.go_forward()
        await self.random_mouse_movement()