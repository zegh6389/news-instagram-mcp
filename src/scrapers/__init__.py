"""Scrapers package initialization."""

from .base_scraper import BaseScraper
from .cbc_scraper import CBCScraper
from .globalnews_scraper import GlobalNewsScraper
from .universal_scraper import UniversalScraper

__all__ = ['BaseScraper', 'CBCScraper', 'GlobalNewsScraper', 'UniversalScraper']
