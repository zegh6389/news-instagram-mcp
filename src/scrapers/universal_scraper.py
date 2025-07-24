"""Universal scraper for news sources using newspaper3k and fallback methods."""

import logging
from typing import Dict, Any, Optional, List
from bs4 import BeautifulSoup
from datetime import datetime
import re
from urllib.parse import urljoin

# Set up logger first
logger = logging.getLogger(__name__)

try:
    from newspaper import Article, Config as NewspaperConfig
    NEWSPAPER_AVAILABLE = True
except ImportError:
    NEWSPAPER_AVAILABLE = False
    logger.warning("newspaper3k not available, using fallback methods")

from .base_scraper import BaseScraper

class UniversalScraper(BaseScraper):
    """Universal scraper that can handle various news sources."""
    
    def __init__(self, source_name: str, source_config: Dict[str, Any]):
        super().__init__(source_name, source_config)
        
        # Setup newspaper3k if available
        if NEWSPAPER_AVAILABLE:
            self.newspaper_config = NewspaperConfig()
            self.newspaper_config.browser_user_agent = self.session.headers['User-Agent']
            self.newspaper_config.request_timeout = 30
            self.newspaper_config.number_threads = 1
    
    def _extract_content(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """Extract content using multiple methods."""
        
        # Try newspaper3k first if available
        if NEWSPAPER_AVAILABLE:
            newspaper_result = self._extract_with_newspaper(url)
            if newspaper_result:
                return newspaper_result
        
        # Fallback to manual extraction
        return self._extract_with_selectors(soup, url)
    
    def _extract_with_newspaper(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract content using newspaper3k library."""
        try:
            article = Article(url, config=self.newspaper_config)
            article.download()
            article.parse()
            
            # Validate extracted content
            if not article.title or len(article.text) < 200:
                logger.warning(f"Insufficient content from newspaper3k for {url}")
                return None
            
            # Create summary
            summary = self._create_summary(article.text)
            
            return {
                'headline': self._clean_text(article.title),
                'content': self._clean_text(article.text),
                'summary': summary,
                'author': ', '.join(article.authors) if article.authors else '',
                'published_date': article.publish_date,
                'image_url': article.top_image if article.top_image else None
            }
            
        except Exception as e:
            logger.error(f"Error extracting with newspaper3k from {url}: {e}")
            return None
    
    def _extract_with_selectors(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """Extract content using CSS selectors and heuristics."""
        try:
            # Extract headline
            headline = self._extract_headline_universal(soup)
            if not headline:
                logger.warning(f"No headline found for {url}")
                return None
            
            # Extract content
            content = self._extract_content_universal(soup)
            if len(content) < 200:
                logger.warning(f"Content too short for {url}")
                return None
            
            # Extract other fields
            author = self._extract_author_universal(soup)
            published_date = self._extract_date_universal(soup)
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
            logger.error(f"Error in universal selector extraction from {url}: {e}")
            return None
    
    def _extract_headline_universal(self, soup: BeautifulSoup) -> str:
        """Extract headline using universal selectors."""
        # Try configured selector first
        if self.selectors.get('headline'):
            headline = self._extract_text_by_selector(soup, self.selectors['headline'])
            if headline:
                return headline
        
        # Universal headline selectors in order of preference
        headline_selectors = [
            'h1[class*="headline"]',
            'h1[class*="title"]',
            'h1[class*="head"]',
            'article h1',
            'main h1',
            '.article-title h1',
            '.post-title h1',
            '.entry-title h1',
            '.content-title h1',
            'meta[property="og:title"]',
            'title',
            'h1'
        ]
        
        for selector in headline_selectors:
            if selector == 'meta[property="og:title"]':
                element = soup.select_one(selector)
                if element:
                    return element.get('content', '')
            elif selector == 'title':
                element = soup.select_one(selector)
                if element:
                    title = element.get_text(strip=True)
                    # Clean up title (remove site name)
                    title = re.sub(r'\s*[-|–]\s*.*$', '', title)
                    if len(title) > 10:
                        return title
            else:
                headline = self._extract_text_by_selector(soup, selector)
                if headline and len(headline) > 10:
                    return headline
        
        return ""
    
    def _extract_content_universal(self, soup: BeautifulSoup) -> str:
        """Extract content using universal selectors."""
        content_parts = []
        
        # Try configured selector first
        if self.selectors.get('content'):
            elements = soup.select(self.selectors['content'] + ' p')
            if elements:
                for p in elements:
                    text = p.get_text(strip=True)
                    if self._is_valid_paragraph(text):
                        content_parts.append(text)
                
                if content_parts:
                    return ' '.join(content_parts)
        
        # Universal content selectors
        content_selectors = [
            'article p',
            'main p',
            '[class*="content"] p',
            '[class*="article"] p',
            '[class*="story"] p',
            '[class*="post"] p',
            '[class*="body"] p',
            '.entry-content p',
            '.post-content p',
            '.article-content p',
            '.story-content p'
        ]
        
        for selector in content_selectors:
            paragraphs = soup.select(selector)
            if paragraphs:
                temp_content = []
                for p in paragraphs:
                    if self._should_skip_paragraph_universal(p):
                        continue
                    
                    text = p.get_text(strip=True)
                    if self._is_valid_paragraph(text):
                        temp_content.append(text)
                
                if len(temp_content) >= 3:  # Require at least 3 paragraphs
                    content_parts = temp_content
                    break
        
        return ' '.join(content_parts)
    
    def _should_skip_paragraph_universal(self, paragraph) -> bool:
        """Check if paragraph should be skipped using universal rules."""
        # Check paragraph classes
        classes = paragraph.get('class', [])
        skip_classes = [
            'advertisement', 'ad', 'ads', 'social', 'share', 'related',
            'sidebar', 'footer', 'header', 'navigation', 'nav', 'menu',
            'author-bio', 'bio', 'byline', 'caption', 'credit',
            'tags', 'category', 'meta', 'timestamp'
        ]
        
        paragraph_classes = ' '.join(classes).lower()
        if any(skip_class in paragraph_classes for skip_class in skip_classes):
            return True
        
        # Check parent element classes
        parent = paragraph.parent
        if parent:
            parent_classes = ' '.join(parent.get('class', [])).lower()
            if any(skip_class in parent_classes for skip_class in skip_classes):
                return True
        
        # Check for specific attributes
        if paragraph.get('data-module') or paragraph.get('data-ad'):
            return True
        
        return False
    
    def _is_valid_paragraph(self, text: str) -> bool:
        """Enhanced paragraph validation."""
        if not text or len(text) < 30:
            return False
        
        # Skip common unwanted content patterns
        unwanted_patterns = [
            r'advertisement',
            r'subscribe\s+to',
            r'newsletter',
            r'follow\s+us',
            r'share\s+this',
            r'read\s+more:?',
            r'watch:?',
            r'listen:?',
            r'click\s+here',
            r'sign\s+up',
            r'terms\s+of\s+service',
            r'privacy\s+policy',
            r'cookie\s+policy',
            r'©\s*\d{4}',  # Copyright
            r'all\s+rights\s+reserved'
        ]
        
        text_lower = text.lower()
        if any(re.search(pattern, text_lower) for pattern in unwanted_patterns):
            return False
        
        # Check for meaningful content
        word_count = len(text.split())
        if word_count < 8:
            return False
        
        # Check character composition
        alpha_chars = sum(c.isalpha() for c in text)
        if alpha_chars < len(text) * 0.6:  # At least 60% alphabetic
            return False
        
        return True
    
    def _extract_author_universal(self, soup: BeautifulSoup) -> str:
        """Extract author using universal selectors."""
        # Try configured selector first
        if self.selectors.get('author'):
            author = self._extract_text_by_selector(soup, self.selectors['author'])
            if author:
                return self._clean_author_name(author)
        
        # Universal author selectors
        author_selectors = [
            '[class*="author"]',
            '[class*="byline"]',
            '[class*="writer"]',
            'span[itemprop="author"]',
            'meta[name="author"]',
            'meta[property="article:author"]',
            '.by-author',
            '.article-author',
            '.post-author'
        ]
        
        for selector in author_selectors:
            if selector.startswith('meta'):
                element = soup.select_one(selector)
                if element:
                    author = element.get('content', '')
                    if author:
                        return self._clean_author_name(author)
            else:
                author = self._extract_text_by_selector(soup, selector)
                if author:
                    return self._clean_author_name(author)
        
        return ""
    
    def _clean_author_name(self, author: str) -> str:
        """Clean and format author name."""
        if not author:
            return ""
        
        # Remove common prefixes
        author = re.sub(r'^(By|Author|Written by)\s+', '', author, flags=re.IGNORECASE)
        
        # Remove everything after comma or pipe
        author = re.sub(r'\s*[,|]\s*.*$', '', author)
        
        # Remove common suffixes
        author = re.sub(r'\s+(Reporter|Journalist|Staff|Writer).*$', '', author, flags=re.IGNORECASE)
        
        return author.strip()
    
    def _extract_date_universal(self, soup: BeautifulSoup) -> Optional[datetime]:
        """Extract published date using universal selectors."""
        # Try configured selector first
        if self.selectors.get('date'):
            date_element = soup.select_one(self.selectors['date'])
            if date_element:
                date_str = (date_element.get('datetime') or 
                           date_element.get('content') or
                           date_element.get_text(strip=True))
                if date_str:
                    return self._parse_date_universal(date_str)
        
        # Universal date selectors
        date_selectors = [
            'time[datetime]',
            'meta[property="article:published_time"]',
            'meta[property="article:modified_time"]',
            'meta[name="publishdate"]',
            'meta[name="date"]',
            '[class*="date"]',
            '[class*="time"]',
            '[class*="publish"]'
        ]
        
        for selector in date_selectors:
            element = soup.select_one(selector)
            if element:
                date_str = (element.get('datetime') or 
                           element.get('content') or
                           element.get_text(strip=True))
                
                if date_str:
                    parsed_date = self._parse_date_universal(date_str)
                    if parsed_date:
                        return parsed_date
        
        return None
    
    def _parse_date_universal(self, date_str: str) -> Optional[datetime]:
        """Parse date string using various formats."""
        try:
            # Clean the date string
            date_str = re.sub(r'\s+', ' ', date_str.strip())
            
            # Common date formats
            date_formats = [
                '%Y-%m-%dT%H:%M:%S.%fZ',
                '%Y-%m-%dT%H:%M:%SZ',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d',
                '%B %d, %Y at %I:%M %p',
                '%B %d, %Y',
                '%b %d, %Y',
                '%d %B %Y',
                '%d %b %Y',
                '%m/%d/%Y',
                '%d/%m/%Y',
                '%Y/%m/%d'
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            logger.warning(f"Could not parse date: {date_str}")
            
        except Exception as e:
            logger.error(f"Error parsing date '{date_str}': {e}")
        
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
