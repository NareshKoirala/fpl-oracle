from utils.log import Logger

HEAD = False  # Set to True if you want to run in headless mode (no browser window)
LOG = Logger("PlayWright_Browser")
AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"


class PlayWright_Browser:
    # --- Shared across ALL instances ---
    _playwright_manager = None
    _shared_browser = None

    def __init__(self):
        # 1. Check if the shared browser exists. If not, start it.
        self._ensure_browser_is_running()

        # 2. Every NEW instance gets its OWN private context and page.
        # This prevents "tab clobbering."
        self.context = self._shared_browser.new_context(user_agent=AGENT)
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
                tag, timeout=5000
            )  # Wait for the specific tag to load
            return self.page.content(), "html.parser"
        except Exception as e:
            LOG.error(f"Scrape failed: {e}")
            return None

    def close_instance(self):
        """Closes the tab, but leaves the browser alive for others."""
        self.page.close()
        self.context.close()
