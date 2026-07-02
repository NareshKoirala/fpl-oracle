import asyncio
import random
import time
import httpx
from service.oracle.utils.log import Logger

LOG = Logger("FPLClient", "utils")

# =============================================================================
# USER-AGENT ROTATION POOL
# =============================================================================

_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) "
    "Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.5; rv:126.0) "
    "Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.5 Safari/605.1.15",
]


class FPLClient:
    """Async HTTP client with exponential backoff, retries, and UA rotation.

    Usage::

        async with FPLClient() as client:
            data = await client.fetch("https://...")
    """

    def __init__(
        self,
        max_retries: int = 5,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            follow_redirects=True,
            headers={
                "Accept": "application/json",
                "Accept-Language": "en-GB,en;q=0.9",
            },
        )
        return self

    async def __aexit__(self, *exc):
        if self._client:
            await self._client.aclose()

    async def fetch(self, url: str):
        """GET *url* and return parsed JSON, or ``None`` on failure.

        Retries on 429 (rate-limit) and 5xx responses with exponential
        backoff + random jitter.  4xx errors (except 429) are terminal.
        """
        for attempt in range(1, self.max_retries + 1):
            ua = random.choice(_USER_AGENTS)
            try:
                LOG.info(f"[Attempt {attempt}/{self.max_retries}] GET {url}")
                resp = await self._client.get(
                    url, headers={"User-Agent": ua}
                )

                if resp.status_code == 200:
                    LOG.info(f"200 OK — {url}")
                    return resp.json()

                if resp.status_code == 429:
                    wait = int(resp.headers.get("Retry-After", 5))
                    LOG.error(f"429 Rate Limited — waiting {wait}s")
                    await asyncio.sleep(wait)
                    continue

                if resp.status_code >= 500:
                    LOG.error(
                        f"{resp.status_code} Server Error — retrying"
                    )
                else:
                    LOG.error(
                        f"{resp.status_code} Client Error — {url} (no retry)"
                    )
                    return None

            except (
                httpx.ConnectError,
                httpx.ReadTimeout,
                httpx.PoolTimeout,
            ) as e:
                LOG.error(f"Connection error: {type(e).__name__} — {e}")

            except Exception as e:
                LOG.error(f"Unexpected error: {type(e).__name__} — {e}")
                return None

            # Exponential backoff with jitter
            delay = min(
                self.base_delay * (2 ** (attempt - 1)), self.max_delay
            )
            jitter = random.uniform(0, delay * 0.5)
            wait = delay + jitter
            LOG.info(f"Backing off {wait:.1f}s before retry...")
            await asyncio.sleep(wait)

        LOG.error(f"All {self.max_retries} attempts failed — {url}")
        return None
