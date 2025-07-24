"""Tests for news scrapers."""

import pytest
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from src.scrapers import CBCScraper, GlobalNewsScraper, UniversalScraper


class TestCBCScraper(unittest.TestCase):
    """Test CBC scraper functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.source_config = {
            'name': 'CBC News',
            'base_url': 'https://www.cbc.ca',
            'rss_feeds': ['https://www.cbc.ca/cmlink/rss-topstories'],
            'selectors': {
                'headline': 'h1.detailHeadline',
                'content': '.story-content',
                'image': '.lead-media img',
                'author': '.byline-author',
                'date': 'time'
            }
        }
        
        with patch('src.scrapers.base_scraper.DatabaseManager'):
            self.scraper = CBCScraper('cbc', self.source_config)
    
    def test_scraper_initialization(self):
        """Test scraper is properly initialized."""
        self.assertEqual(self.scraper.source_name, 'cbc')
        self.assertEqual(self.scraper.base_url, 'https://www.cbc.ca')
        self.assertIsNotNone(self.scraper.session)
    
    @patch('src.scrapers.base_scraper.feedparser.parse')
    def test_scrape_rss_feeds(self, mock_parse):
        """Test RSS feed scraping."""
        # Mock RSS feed response
        mock_entry = Mock()
        mock_entry.link = 'https://www.cbc.ca/news/test-article'
        mock_entry.title = 'Test Article'
        mock_entry.summary = 'Test summary'
        mock_entry.author = 'Test Author'
        mock_entry.published_parsed = (2024, 1, 1, 12, 0, 0, 0, 1, 0)
        
        mock_feed = Mock()
        mock_feed.entries = [mock_entry]
        mock_parse.return_value = mock_feed
        
        articles = self.scraper.scrape_rss_feeds()
        
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]['url'], 'https://www.cbc.ca/news/test-article')
        self.assertEqual(articles[0]['headline'], 'Test Article')
    
    @patch('src.scrapers.cbc_scraper.requests.Session.get')
    def test_scrape_article_content(self, mock_get):
        """Test individual article scraping."""
        # Mock HTML response
        html_content = '''
        <html>
            <h1 class="detailHeadline">Test Headline</h1>
            <div class="story-content">
                <p>This is test content paragraph 1.</p>
                <p>This is test content paragraph 2.</p>
            </div>
            <div class="byline-author">Test Author</div>
            <time datetime="2024-01-01T12:00:00Z">Jan 1, 2024</time>
        </html>
        '''
        
        mock_response = Mock()
        mock_response.content = html_content.encode()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.scraper.scrape_article_content('https://test.com/article')
        
        self.assertIsNotNone(result)
        self.assertEqual(result['headline'], 'Test Headline')
        self.assertIn('test content', result['content'].lower())


class TestGlobalNewsScraper(unittest.TestCase):
    """Test Global News scraper functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.source_config = {
            'name': 'Global News',
            'base_url': 'https://globalnews.ca',
            'rss_feeds': ['https://globalnews.ca/feed/'],
            'selectors': {
                'headline': 'h1.c-detail__headline',
                'content': '.l-article__body',
                'image': '.c-leadmedia__image img',
                'author': '.c-byline__author',
                'date': '.c-byline__date'
            }
        }
        
        with patch('src.scrapers.base_scraper.DatabaseManager'):
            self.scraper = GlobalNewsScraper('globalnews', self.source_config)
    
    def test_scraper_initialization(self):
        """Test scraper is properly initialized."""
        self.assertEqual(self.scraper.source_name, 'globalnews')
        self.assertEqual(self.scraper.base_url, 'https://globalnews.ca')


class TestUniversalScraper(unittest.TestCase):
    """Test Universal scraper functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.source_config = {
            'name': 'Test News',
            'base_url': 'https://test-news.com',
            'rss_feeds': ['https://test-news.com/feed'],
            'selectors': {
                'headline': 'h1',
                'content': 'article',
                'image': 'img',
                'author': '.author',
                'date': 'time'
            }
        }
        
        with patch('src.scrapers.base_scraper.DatabaseManager'):
            self.scraper = UniversalScraper('test', self.source_config)
    
    def test_scraper_initialization(self):
        """Test scraper is properly initialized."""
        self.assertEqual(self.scraper.source_name, 'test')
        self.assertEqual(self.scraper.base_url, 'https://test-news.com')
    
    @patch('src.scrapers.universal_scraper.NEWSPAPER_AVAILABLE', True)
    @patch('src.scrapers.universal_scraper.Article')
    def test_extract_with_newspaper(self, mock_article_class):
        """Test extraction using newspaper3k."""
        # Mock newspaper3k Article
        mock_article = Mock()
        mock_article.title = 'Test Title'
        mock_article.text = 'Test article content with enough words to pass validation.'
        mock_article.authors = ['Test Author']
        mock_article.publish_date = datetime(2024, 1, 1, 12, 0, 0)
        mock_article.top_image = 'https://test.com/image.jpg'
        
        mock_article_class.return_value = mock_article
        
        result = self.scraper._extract_with_newspaper('https://test.com/article')
        
        self.assertIsNotNone(result)
        self.assertEqual(result['headline'], 'Test Title')
        self.assertIn('Test article content', result['content'])


if __name__ == '__main__':
    unittest.main()
