"""
Base scraper classes with common functionality
"""

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import requests
from loguru import logger
from requests.adapters import HTTPAdapter
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
from urllib3.util.retry import Retry

from src.config import config


class BaseScraper(ABC):
    """Base class for all scrapers with common retry and error handling logic"""

    def __init__(
        self,
        url: str,
        timeout: Optional[int] = None,
        retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize scraper

        Args:
            url: Target URL to scrape
            timeout: Request timeout in seconds
            retries: Number of retry attempts
            headers: Custom HTTP headers
        """
        self.url = url
        self.timeout = timeout or config.scraper.timeout
        self.retries = retries or config.scraper.retries
        self.headers = headers or {"User-Agent": config.scraper.user_agent}

        logger.info(f"Initializing scraper for: {url}")

    @abstractmethod
    def fetch(self) -> Dict[str, Any]:
        """Fetch and parse data from URL"""
        pass

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry strategy"""
        session = requests.Session()

        retry_strategy = Retry(
            total=self.retries,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=config.scraper.backoff_factor,
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    @retry(
        retry=retry_if_exception_type(requests.RequestException),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    def _fetch_with_retry(self, session: requests.Session) -> requests.Response:
        """Fetch URL with automatic retry logic"""
        response = session.get(
            self.url,
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response


class BeautifulSoupScraper(BaseScraper):
    """Scraper using BeautifulSoup for static HTML parsing"""

    def fetch(self) -> Dict[str, Any]:
        """Fetch and parse HTML content"""
        try:
            session = self._create_session()
            response = self._fetch_with_retry(session)

            from bs4 import BeautifulSoup

            soup = BeautifulSoup(response.content, "html.parser")

            logger.info(f"Successfully scraped {self.url}")

            return {
                "url": self.url,
                "status_code": response.status_code,
                "title": soup.title.string if soup.title else None,
                "html": response.text,
                "soup": soup,  # Return BeautifulSoup object for further parsing
            }

        except Exception as e:
            logger.error(f"Failed to scrape {self.url}: {str(e)}")
            raise


class SeleniumScraper(BaseScraper):
    """Scraper using Selenium for JavaScript-heavy sites"""

    def __init__(self, *args, **kwargs):
        """Initialize Selenium scraper with browser setup"""
        super().__init__(*args, **kwargs)
        self.driver = None

    def fetch(self) -> Dict[str, Any]:
        """Fetch content using Selenium browser automation"""
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait

            options = webdriver.ChromeOptions()
            if config.scraper.headless_browser:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            self.driver = webdriver.Chrome(options=options)
            self.driver.get(self.url)

            # Wait for page to load
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "body"))
            )

            from bs4 import BeautifulSoup

            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            logger.info(f"Successfully scraped {self.url} (Selenium)")

            return {
                "url": self.url,
                "title": self.driver.title,
                "html": self.driver.page_source,
                "soup": soup,
            }

        except Exception as e:
            logger.error(f"Failed to scrape {self.url} with Selenium: {str(e)}")
            raise

        finally:
            if self.driver:
                self.driver.quit()


class AsyncScraper(BaseScraper):
    """Asynchronous scraper for high-concurrency scenarios"""

    async def fetch_async(self) -> Dict[str, Any]:
        """Fetch content asynchronously"""
        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.url, headers=self.headers, timeout=self.timeout
                ) as response:
                    content = await response.text()

                    from bs4 import BeautifulSoup

                    soup = BeautifulSoup(content, "html.parser")

                    logger.info(f"Successfully scraped {self.url} (async)")

                    return {
                        "url": self.url,
                        "status_code": response.status,
                        "html": content,
                        "soup": soup,
                    }

        except Exception as e:
            logger.error(f"Failed to async scrape {self.url}: {str(e)}")
            raise

    def fetch(self) -> Dict[str, Any]:
        """Wrapper for async fetch"""
        return asyncio.run(self.fetch_async())


if __name__ == "__main__":
    # Example usage
    scraper = BeautifulSoupScraper("https://example.com")
    result = scraper.fetch()
    print(f"Scraped: {result['title']}")
