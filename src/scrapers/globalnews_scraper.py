"""Global News scraper implementation."""

import logging
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
from datetime import datetime
import re

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class GlobalNewsScraper(BaseScraper):
    """Scraper for Global News."""
    
    def _extract_content(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """Extract content from Global News article page."""
        try:
            # Extract headline
            headline = self._extract_headline(soup)
            if not headline:
                logger.warning(f"No headline found for Global News article: {url}")
                return None
            
            # Extract content
            content = self._extract_article_content(soup)
            logger.debug(f"Extracted content length: {len(content)} characters for {url}")
            if len(content) < 100:  # Reduced from 200 to 100
                logger.warning(f"Content too short ({len(content)} chars) for Global News article: {url}")
                logger.debug(f"Content preview: {content[:200]}...")
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
            logger.error(f"Error extracting Global News content from {url}: {e}")
            return None
    
    def _extract_headline(self, soup: BeautifulSoup) -> str:
        """Extract headline with Global News specific selectors."""
        headline_selectors = [
            'h1.c-detail__headline',
            'h1.l-article__headline',
            '.entry-title h1',
            'article h1',
            '.headline h1',
            'h1'
        ]
        
        for selector in headline_selectors:
            headline = self._extract_text_by_selector(soup, selector)
            if headline and len(headline) > 10:
                return headline
        
        return ""
    
    def _extract_article_content(self, soup: BeautifulSoup) -> str:
        """Extract article content with Global News specific selectors."""
        content_parts = []
        
        # Global News specific content selectors (ordered by specificity)
        content_selectors = [
            '.l-article__body p',
            '.c-detail__body p',
            'article p',  # More generic - found to work
            '.entry-content p',
            'article .content p',
            '.post-content p',
            '.content p'
        ]
        
        for selector in content_selectors:
            paragraphs = soup.select(selector)
            if paragraphs:
                for p in paragraphs:
                    # Skip unwanted paragraphs
                    if self._should_skip_paragraph(p):
                        continue
                    
                    text = p.get_text(strip=True)
                    
                    # Filter content
                    if self._is_valid_paragraph(text):
                        content_parts.append(text)
                
                if content_parts:
                    break
        
        return ' '.join(content_parts)
    
    def _should_skip_paragraph(self, paragraph) -> bool:
        """Check if paragraph should be skipped."""
        # Skip paragraphs with certain classes
        classes = paragraph.get('class', [])
        skip_classes = ['advertisement', 'ad', 'social-share', 'related-content', 'author-bio']
        
        if any(skip_class in classes for skip_class in skip_classes):
            return True
        
        # Skip paragraphs with certain parent elements
        parent_classes = []
        if paragraph.parent:
            parent_classes = paragraph.parent.get('class', [])
        
        skip_parent_classes = ['sidebar', 'footer', 'header', 'navigation']
        if any(skip_class in parent_classes for skip_class in skip_parent_classes):
            return True
        
        return False
    
    def _is_valid_paragraph(self, text: str) -> bool:
        """Check if paragraph text is valid content."""
        if not text or len(text) < 30:
            return False
        
        # Skip common unwanted content
        unwanted_phrases = [
            'advertisement',
            'subscribe to',
            'newsletter',
            'follow us',
            'share this story',
            'read more:',
            'watch:',
            'listen:',
            'click here',
            'sign up',
            'terms of service',
            'privacy policy'
        ]
        
        text_lower = text.lower()
        if any(phrase in text_lower for phrase in unwanted_phrases):
            return False
        
        # Skip if mostly punctuation or numbers
        alpha_chars = sum(c.isalpha() for c in text)
        if alpha_chars < len(text) * 0.7:
            return False
        
        return True
    
    def _extract_author(self, soup: BeautifulSoup) -> str:
        """Extract author with Global News specific selectors."""
        author_selectors = [
            '.c-byline__author',
            '.l-article__byline .author',
            '.author-name',
            '.byline-author',
            'span[itemprop="author"]',
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
                    author = re.sub(r'\s*,.*$', '', author)  # Remove everything after comma
                    return author.strip()
        
        return ""
    
    def _extract_published_date(self, soup: BeautifulSoup) -> Optional[datetime]:
        """Extract published date with Global News specific selectors."""
        date_selectors = [
            '.c-byline__date time',
            '.l-article__byline time',
            'time[datetime]',
            'meta[property="article:published_time"]',
            '.publish-date',
            '.timestamp'
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
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string from Global News."""
        try:
            # Clean the date string
            date_str = re.sub(r'\s+', ' ', date_str.strip())
            
            # Global News date formats
            date_formats = [
                '%Y-%m-%dT%H:%M:%S.%fZ',     # ISO with microseconds
                '%Y-%m-%dT%H:%M:%SZ',        # ISO format
                '%Y-%m-%dT%H:%M:%S',         # ISO without Z
                '%Y-%m-%d %H:%M:%S',         # Standard format
                '%B %d, %Y at %I:%M %p',     # "January 1, 2024 at 12:00 PM"
                '%B %d, %Y',                 # "January 1, 2024"
                '%b %d, %Y',                 # "Jan 1, 2024"
                '%d/%m/%Y',                  # "01/01/2024"
                '%m/%d/%Y',                  # "01/01/2024"
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            # Try parsing relative dates
            if 'ago' in date_str.lower():
                return self._parse_relative_date(date_str)
            
            logger.warning(f"Could not parse Global News date: {date_str}")
            
        except Exception as e:
            logger.error(f"Error parsing Global News date '{date_str}': {e}")
        
        return None
    
    def _parse_relative_date(self, date_str: str) -> Optional[datetime]:
        """Parse relative date strings like '2 hours ago'."""
        try:
            from datetime import timedelta
            
            date_str = date_str.lower().strip()
            now = datetime.utcnow()
            
            # Extract number and unit
            match = re.search(r'(\d+)\s*(minute|hour|day|week|month)s?\s+ago', date_str)
            if match:
                amount = int(match.group(1))
                unit = match.group(2)
                
                if unit == 'minute':
                    return now - timedelta(minutes=amount)
                elif unit == 'hour':
                    return now - timedelta(hours=amount)
                elif unit == 'day':
                    return now - timedelta(days=amount)
                elif unit == 'week':
                    return now - timedelta(weeks=amount)
                elif unit == 'month':
                    return now - timedelta(days=amount * 30)  # Approximate
            
        except Exception as e:
            logger.error(f"Error parsing relative date '{date_str}': {e}")
        
        return None
    
    def _create_summary(self, content: str, max_sentences: int = 3) -> str:
        """Create a summary from the article content."""
        if not content:
            return ""
        
        # Split into sentences, handling various punctuation
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
        
        # Take first few sentences
        summary_sentences = sentences[:max_sentences]
        summary = '. '.join(summary_sentences)
        
        if summary and not summary.endswith('.'):
            summary += '.'
        
        return summary
    
    def _extract_image_url(self, soup: BeautifulSoup, base_url: str) -> Optional[str]:
        """Extract image URL with Global News specific selectors."""
        image_selectors = [
            '.c-leadmedia__image img',
            '.l-article__leadmedia img',
            '.featured-image img',
            'meta[property="og:image"]',
            'meta[name="twitter:image"]',
            'article img'
        ]
        
        for selector in image_selectors:
            element = soup.select_one(selector)
            if element:
                img_url = (element.get('content') or 
                          element.get('src') or 
                          element.get('data-src') or
                          element.get('data-lazy-src'))
                
                if img_url:
                    # Convert relative URLs to absolute
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    elif img_url.startswith('/'):
                        from urllib.parse import urljoin
                        img_url = urljoin(base_url, img_url)
                    
                    # Validate image URL
                    if self._is_valid_image_url(img_url):
                        return img_url
        
        return None
    
    def _is_valid_image_url(self, url: str) -> bool:
        """Check if URL is a valid image URL."""
        if not url:
            return False
        
        # Check for common image extensions
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        url_lower = url.lower()
        
        # Check extension
        if any(ext in url_lower for ext in image_extensions):
            return True
        
        # Check for image in path
        if '/image' in url_lower or '/img' in url_lower:
            return True
        
        # Skip placeholder or icon images
        skip_keywords = ['placeholder', 'icon', 'logo', 'avatar', 'default']
        if any(keyword in url_lower for keyword in skip_keywords):
            return False
        
        return True
