from utils.log import Logger
from utils.settings import HEAD, BROWSER_WAIT_TIME, AGENT

LOG = Logger("PlayWright_Browser")


class PlayWright_sync_Browser:
    # --- Shared across ALL instances ---
    _playwright_manager = None
    _shared_browser = None

    def __init__(self):
        self._ensure_browser_is_running()
        
        # Version 2.0.3 Class-based approach 
        from playwright_stealth import Stealth
        self.stealth = Stealth() 

        self.context = self._shared_browser.new_context(user_agent=AGENT)
        
        # Apply to the context so ALL pages inherit the stealth 
        self.stealth.apply_stealth_sync(self.context)
        
        self.page = self.context.new_page()

    @classmethod
    def _ensure_browser_is_running(cls):
        """Logic to launch the engine only once."""
        if cls._shared_browser is None:
            # We use cls instead of self because these are Class variables
            from playwright.sync_api import sync_playwright

            cls._playwright_manager = sync_playwright().start()
            cls._shared_browser = cls._playwright_manager.chromium.launch(headless=HEAD)
            LOG.info("Browser engine started successfully.")

    @classmethod
    def shutdown_engine(cls):
        """Call this once at the very end of your program."""
        if cls._shared_browser:
            cls._shared_browser.close()
        if cls._playwright_manager:
            cls._playwright_manager.stop()
        LOG.info("Browser engine shut down successfully.")

    def get_content(self, url, tag: str):
        try:
            self.page.goto(url)
            self.page.wait_for_selector(
                tag, timeout=BROWSER_WAIT_TIME
            )  # Wait for the specific tag to load
            return self.page.content()
        except Exception as e:
            LOG.error(f"Scrape failed: {e}")
            return None

    def close_instance(self):
        """Closes the tab, but leaves the browser alive for others."""
        self.page.close()
        self.context.close()
