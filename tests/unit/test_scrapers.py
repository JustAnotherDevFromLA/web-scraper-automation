"""
Unit tests for scrapers module
"""

import pytest

from src.scrapers import AsyncScraper, BeautifulSoupScraper


@pytest.mark.unit
@pytest.mark.scraper
def test_beautifulsoup_scraper_initialization():
    """Test scraper initialization"""
    scraper = BeautifulSoupScraper("https://example.com")

    assert scraper.url == "https://example.com"
    assert scraper.timeout == 30
    assert scraper.retries == 3


@pytest.mark.unit
@pytest.mark.scraper
def test_scraper_with_custom_timeout():
    """Test scraper with custom timeout"""
    scraper = BeautifulSoupScraper("https://example.com", timeout=60, retries=5)

    assert scraper.timeout == 60
    assert scraper.retries == 5


@pytest.mark.unit
@pytest.mark.scraper
def test_scraper_headers():
    """Test custom headers"""
    custom_headers = {"User-Agent": "CustomBot/1.0"}
    scraper = BeautifulSoupScraper("https://example.com", headers=custom_headers)

    assert scraper.headers == custom_headers


@pytest.mark.unit
@pytest.mark.scraper
@pytest.mark.asyncio
async def test_async_scraper_initialization():
    """Test async scraper initialization"""
    scraper = AsyncScraper("https://example.com")

    assert scraper.url == "https://example.com"
    assert hasattr(scraper, "fetch_async")
