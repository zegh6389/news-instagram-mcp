"""Base scraper class for news sources."""

import requests
import time
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from datetime import datetime
import feedparser

from ..config import config
from ..database import DatabaseManager, NewsArticle

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Abstract base class for news scrapers."""
    
    def __init__(self, source_name: str, source_config: Dict[str, Any]):
        self.source_name = source_name
        self.source_config = source_config
        self.base_url = source_config.get('base_url', '')
        self.selectors = source_config.get('selectors', {})
        self.rss_feeds = source_config.get('rss_feeds', [])
        self.db_manager = DatabaseManager()
        
        # Setup requests session
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': config.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def scrape_rss_feeds(self) -> List[Dict[str, Any]]:
        """Scrape articles from RSS feeds."""
        articles = []
        
        for feed_url in self.rss_feeds:
            try:
                logger.info(f"Scraping RSS feed: {feed_url}")
                
                # Set socket timeout for feedparser
                import socket
                original_timeout = socket.getdefaulttimeout()
                socket.setdefaulttimeout(10.0)  # Reduced from 15 to 10 seconds
                
                try:
                    # Use requests to fetch RSS first to handle timeouts better
                    response = self.session.get(feed_url, timeout=8)
                    response.raise_for_status()
                    
                    # Parse the fetched content
                    feed = feedparser.parse(response.text)
                    
                    if feed.bozo:
                        logger.warning(f"RSS feed {feed_url} has parsing issues: {feed.bozo_exception}")
                        # Continue processing even with parsing issues
                        
                    logger.info(f"Found {len(feed.entries)} entries in RSS feed")
                    
                    articles_from_feed = 0
                    for entry in feed.entries:
                        try:
                            article_data = self._parse_rss_entry(entry)
                            if article_data:
                                articles.append(article_data)
                                articles_from_feed += 1
                        except Exception as e:
                            logger.warning(f"Error parsing RSS entry from {feed_url}: {e}")
                            continue
                    
                    logger.info(f"Successfully parsed {articles_from_feed} articles from {feed_url}")
                        
                finally:
                    # Restore original timeout
                    socket.setdefaulttimeout(original_timeout)
                    
                time.sleep(config.request_delay)
                
            except Exception as e:
                logger.error(f"Error scraping RSS feed {feed_url}: {e}")
                continue  # Continue with next feed
        
        logger.info(f"Total articles scraped: {len(articles)}")
        return articles
    
    def _parse_rss_entry(self, entry) -> Optional[Dict[str, Any]]:
        """Parse an RSS feed entry."""
        try:
            # Extract basic information
            url = entry.link
            headline = entry.title
            summary = getattr(entry, 'summary', '')
            author = getattr(entry, 'author', '')
            
            # Parse published date
            published_date = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_date = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                published_date = datetime(*entry.updated_parsed[:6])
            
            return {
                'url': url,
                'source': self.source_name,
                'headline': headline,
                'content': summary,  # Will be updated with full content later
                'summary': summary,
                'author': author,
                'published_date': published_date,
                'scraped_date': datetime.utcnow()
            }
        except Exception as e:
            logger.error(f"Error parsing RSS entry: {e}")
            return None
    
    def scrape_article_content(self, url: str) -> Optional[Dict[str, Any]]:
        """Scrape full article content from URL."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract content using selectors
            content_data = self._extract_content(soup, url)
            
            if content_data:
                content_data['url'] = url
                content_data['source'] = self.source_name
                content_data['scraped_date'] = datetime.utcnow()
            
            time.sleep(config.request_delay)
            return content_data
            
        except Exception as e:
            logger.error(f"Error scraping article {url}: {e}")
            return None
    
    @abstractmethod
    def _extract_content(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """Extract content from parsed HTML. Must be implemented by subclasses."""
        pass
    
    def _extract_text_by_selector(self, soup: BeautifulSoup, selector: str) -> str:
        """Extract text using CSS selector."""
        try:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        except Exception as e:
            logger.error(f"Error extracting text with selector '{selector}': {e}")
        return ""
    
    def _extract_image_url(self, soup: BeautifulSoup, base_url: str) -> Optional[str]:
        """Extract main article image URL."""
        try:
            # Try multiple selectors for images
            image_selectors = [
                self.selectors.get('image', ''),
                'meta[property="og:image"]',
                'meta[name="twitter:image"]',
                '.article-image img',
                '.lead-image img',
                'article img'
            ]
            
            for selector in image_selectors:
                if not selector:
                    continue
                    
                element = soup.select_one(selector)
                if element:
                    # Get image URL from different attributes
                    img_url = (element.get('content') or 
                              element.get('src') or 
                              element.get('data-src'))
                    
                    if img_url:
                        # Convert relative URLs to absolute
                        if img_url.startswith('//'):
                            img_url = 'https:' + img_url
                        elif img_url.startswith('/'):
                            img_url = urljoin(base_url, img_url)
                        
                        return img_url
        except Exception as e:
            logger.error(f"Error extracting image URL: {e}")
        
        return None
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove common unwanted phrases
        unwanted_phrases = [
            "Click here to subscribe",
            "Advertisement",
            "Sign up for our newsletter",
            "Follow us on",
            "Share this story"
        ]
        
        for phrase in unwanted_phrases:
            text = text.replace(phrase, "")
        
        return text.strip()
    
    def _categorize_article(self, headline: str, content: str) -> str:
        """Categorize article based on content."""
        text = (headline + " " + content).lower()
        categories = config.get_categories()
        
        for category, category_config in categories.items():
            keywords = category_config.get('keywords', [])
            if any(keyword.lower() in text for keyword in keywords):
                return category
        
        return 'general'
    
    def _extract_keywords(self, headline: str, content: str) -> List[str]:
        """Extract keywords from article content."""
        # Simple keyword extraction - can be enhanced with NLP
        text = (headline + " " + content).lower()
        
        # Common news keywords
        news_keywords = [
            'breaking', 'urgent', 'alert', 'developing', 'exclusive',
            'government', 'politics', 'election', 'parliament', 'minister',
            'economy', 'business', 'finance', 'market', 'inflation',
            'health', 'medical', 'hospital', 'covid', 'pandemic',
            'weather', 'storm', 'climate', 'temperature', 'forecast',
            'sports', 'hockey', 'olympics', 'game', 'match'
        ]
        
        found_keywords = []
        for keyword in news_keywords:
            if keyword in text:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def save_article(self, article_data: Dict[str, Any]) -> Optional[NewsArticle]:
        """Save article to database."""
        try:
            # Add category and keywords
            article_data['category'] = self._categorize_article(
                article_data.get('headline', ''),
                article_data.get('content', '')
            )
            article_data['keywords'] = self._extract_keywords(
                article_data.get('headline', ''),
                article_data.get('content', '')
            )
            
            return self.db_manager.save_article(article_data)
        except Exception as e:
            logger.error(f"Error saving article: {e}")
            return None
    
    def run_scraping_session(self) -> Dict[str, int]:
        """Run a complete scraping session."""
        logger.info(f"Starting scraping session for {self.source_name}")
        
        stats = {
            'articles_found': 0,
            'articles_scraped': 0,
            'articles_failed': 0
        }
        
        try:
            # Get articles from RSS feeds
            rss_articles = self.scrape_rss_feeds()
            stats['articles_found'] = len(rss_articles)
            
            for article_data in rss_articles:
                try:
                    # Get full article content
                    full_content = self.scrape_article_content(article_data['url'])
                    
                    if full_content:
                        # Merge RSS data with full content
                        article_data.update(full_content)
                        
                        # Save to database
                        saved_article = self.save_article(article_data)
                        
                        if saved_article:
                            stats['articles_scraped'] += 1
                            logger.info(f"Successfully scraped: {article_data['headline']}")
                        else:
                            stats['articles_failed'] += 1
                    else:
                        stats['articles_failed'] += 1
                        
                except Exception as e:
                    logger.error(f"Error processing article {article_data.get('url', 'unknown')}: {e}")
                    stats['articles_failed'] += 1
            
            logger.info(f"Scraping session completed for {self.source_name}: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error in scraping session for {self.source_name}: {e}")
            return stats
