"""CBC News scraper implementation."""

import logging
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
from datetime import datetime
import re

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class CBCScraper(BaseScraper):
    """Scraper for CBC News."""
    
    def _extract_content(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """Extract content from CBC article page."""
        try:
            # Extract headline
            headline = self._extract_text_by_selector(soup, self.selectors.get('headline', 'h1'))
            if not headline:
                # Try alternative selectors
                headline = (self._extract_text_by_selector(soup, 'h1.detailHeadline') or
                           self._extract_text_by_selector(soup, 'h1.headline') or
                           self._extract_text_by_selector(soup, 'h1'))
            
            # Extract content
            content_parts = []
            content_selectors = [
                self.selectors.get('content', ''),
                '.story-content',
                '.story',
                'article .content',
                '.articleBody'
            ]
            
            for selector in content_selectors:
                if not selector:
                    continue
                elements = soup.select(selector + ' p')
                if elements:
                    for p in elements:
                        text = p.get_text(strip=True)
                        if text and len(text) > 20:  # Filter out short/empty paragraphs
                            content_parts.append(text)
                    break
            
            content = ' '.join(content_parts)
            
            # Extract author
            author = self._extract_text_by_selector(soup, self.selectors.get('author', ''))
            if not author:
                # Try alternative selectors
                author = (self._extract_text_by_selector(soup, '.byline-author') or
                         self._extract_text_by_selector(soup, '.author') or
                         self._extract_text_by_selector(soup, '.byline'))
            
            # Extract published date
            published_date = None
            date_element = soup.select_one(self.selectors.get('date', 'time'))
            if date_element:
                # Try to get datetime attribute
                date_str = (date_element.get('datetime') or 
                           date_element.get('content') or
                           date_element.get_text(strip=True))
                
                if date_str:
                    published_date = self._parse_date(date_str)
            
            # Extract image URL
            image_url = self._extract_image_url(soup, self.base_url)
            
            # Create summary from first few sentences
            summary = self._create_summary(content)
            
            # Clean and validate content
            headline = self._clean_text(headline)
            content = self._clean_text(content)
            author = self._clean_text(author)
            
            if not headline or len(content) < 100:
                logger.warning(f"Insufficient content for CBC article: {url}")
                return None
            
            return {
                'headline': headline,
                'content': content,
                'summary': summary,
                'author': author,
                'published_date': published_date,
                'image_url': image_url
            }
            
        except Exception as e:
            logger.error(f"Error extracting CBC content from {url}: {e}")
            return None
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string from CBC."""
        try:
            # Common CBC date formats
            date_formats = [
                '%Y-%m-%dT%H:%M:%S.%fZ',  # ISO format with microseconds
                '%Y-%m-%dT%H:%M:%SZ',     # ISO format
                '%Y-%m-%dT%H:%M:%S',      # ISO format without Z
                '%Y-%m-%d %H:%M:%S',      # Standard format
                '%B %d, %Y',              # "January 1, 2024"
                '%b %d, %Y',              # "Jan 1, 2024"
            ]
            
            # Clean the date string
            date_str = re.sub(r'\s+', ' ', date_str.strip())
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            logger.warning(f"Could not parse CBC date: {date_str}")
            
        except Exception as e:
            logger.error(f"Error parsing CBC date '{date_str}': {e}")
        
        return None
    
    def _create_summary(self, content: str, max_sentences: int = 3) -> str:
        """Create a summary from the article content."""
        if not content:
            return ""
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
        
        # Take first few sentences
        summary_sentences = sentences[:max_sentences]
        summary = '. '.join(summary_sentences)
        
        if summary and not summary.endswith('.'):
            summary += '.'
        
        return summary
    
    def _extract_content(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """Enhanced content extraction for CBC with better error handling."""
        try:
            article_data = {}
            
            # Extract headline with multiple fallbacks
            headline_selectors = [
                'h1.detailHeadline',
                'h1.headline',
                '.story-headline h1',
                'article h1',
                'h1'
            ]
            
            headline = ""
            for selector in headline_selectors:
                headline = self._extract_text_by_selector(soup, selector)
                if headline:
                    break
            
            if not headline:
                logger.warning(f"No headline found for CBC article: {url}")
                return None
            
            # Extract content with better paragraph handling
            content_parts = []
            content_selectors = [
                '.story-content p',
                '.story p',
                'article .content p',
                '.articleBody p',
                'div[data-component="TextBlock"] p'
            ]
            
            for selector in content_selectors:
                paragraphs = soup.select(selector)
                if paragraphs:
                    for p in paragraphs:
                        # Skip paragraphs with certain classes or attributes
                        if (p.get('class') and 
                            any(cls in ['advertisement', 'ad', 'social-share'] 
                                for cls in p.get('class'))):
                            continue
                        
                        text = p.get_text(strip=True)
                        
                        # Filter out short paragraphs and common unwanted content
                        if (text and len(text) > 30 and 
                            not any(unwanted in text.lower() for unwanted in 
                                   ['advertisement', 'subscribe', 'newsletter', 'follow us'])):
                            content_parts.append(text)
                    
                    if content_parts:
                        break
            
            content = ' '.join(content_parts)
            
            # Validate content length
            if len(content) < 200:
                logger.warning(f"Content too short for CBC article: {url}")
                return None
            
            # Extract other fields
            author = self._extract_author(soup)
            published_date = self._extract_published_date(soup)
            image_url = self._extract_image_url(soup, self.base_url)
            summary = self._create_summary(content)
            
            return {
                'headline': self._clean_text(headline),
                'content': self._clean_text(content),
                'summary': summary,
                'author': author,
                'published_date': published_date,
                'image_url': image_url
            }
            
        except Exception as e:
            logger.error(f"Error in enhanced CBC content extraction from {url}: {e}")
            return None
    
    def _extract_author(self, soup: BeautifulSoup) -> str:
        """Extract author with multiple fallbacks."""
        author_selectors = [
            '.byline-author',
            '.author-name',
            '.byline',
            'span[itemprop="author"]',
            '.story-byline',
            'meta[name="author"]'
        ]
        
        for selector in author_selectors:
            if selector.startswith('meta'):
                element = soup.select_one(selector)
                if element:
                    return element.get('content', '')
            else:
                author = self._extract_text_by_selector(soup, selector)
                if author:
                    # Clean author name
                    author = re.sub(r'^By\s+', '', author, flags=re.IGNORECASE)
                    return author.strip()
        
        return ""
    
    def _extract_published_date(self, soup: BeautifulSoup) -> Optional[datetime]:
        """Extract published date with multiple fallbacks."""
        date_selectors = [
            'time[datetime]',
            'meta[property="article:published_time"]',
            'meta[name="publishdate"]',
            '.timestamp',
            '.publish-date'
        ]
        
        for selector in date_selectors:
            element = soup.select_one(selector)
            if element:
                date_str = (element.get('datetime') or 
                           element.get('content') or
                           element.get_text(strip=True))
                
                if date_str:
                    parsed_date = self._parse_date(date_str)
                    if parsed_date:
                        return parsed_date
        
        return None
