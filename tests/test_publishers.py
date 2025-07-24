"""Tests for publishers."""

import pytest
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

from src.publishers import InstagramPublisher, Scheduler
from src.database.models import InstagramPost, NewsArticle


class TestInstagramPublisher(unittest.TestCase):
    """Test Instagram publisher functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        with patch('src.publishers.instagram_publisher.DatabaseManager'), \
             patch('src.publishers.instagram_publisher.INSTAGRAPI_AVAILABLE', False):
            self.publisher = InstagramPublisher()
        
        # Create mock post
        self.mock_post = Mock(spec=InstagramPost)
        self.mock_post.id = 1
        self.mock_post.caption = 'Test caption #test'
        self.mock_post.hashtags = ['#test', '#news']
        self.mock_post.image_path = '/path/to/image.jpg'
        self.mock_post.article_id = 1
    
    def test_validate_post(self):
        """Test post validation."""
        with patch('pathlib.Path.exists', return_value=True):
            validation = self.publisher._validate_post(self.mock_post)
            
            self.assertIn('is_valid', validation)
            self.assertIn('errors', validation)
    
    def test_validate_post_no_caption(self):
        """Test validation fails with no caption."""
        self.mock_post.caption = ''
        
        validation = self.publisher._validate_post(self.mock_post)
        
        self.assertFalse(validation['is_valid'])
        self.assertIn('Caption is empty', validation['errors'])
    
    def test_validate_post_no_image(self):
        """Test validation fails with no image."""
        self.mock_post.image_path = None
        
        validation = self.publisher._validate_post(self.mock_post)
        
        self.assertFalse(validation['is_valid'])
        self.assertIn('No image provided', validation['errors'])
    
    def test_get_posting_guidelines(self):
        """Test getting posting guidelines."""
        guidelines = self.publisher.get_posting_guidelines()
        
        self.assertIn('image_requirements', guidelines)
        self.assertIn('caption_requirements', guidelines)
        self.assertIn('posting_limits', guidelines)


class TestScheduler(unittest.TestCase):
    """Test scheduler functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        with patch('src.publishers.scheduler.DatabaseManager'):
            self.scheduler = Scheduler()
    
    def test_get_next_posting_time(self):
        """Test getting next posting time."""
        with patch.object(self.scheduler, '_get_last_post_time', return_value=None), \
             patch.object(self.scheduler, '_exceeds_daily_limit', return_value=False):
            
            next_time = self.scheduler.get_next_posting_time()
            
            self.assertIsInstance(next_time, datetime)
            self.assertGreater(next_time, datetime.utcnow())
    
    def test_exceeds_daily_limit(self):
        """Test daily limit checking."""
        test_date = datetime.utcnow().date()
        
        with patch.object(self.scheduler.db_manager, 'get_session') as mock_session:
            mock_query = Mock()
            mock_query.filter.return_value = mock_query
            mock_query.count.return_value = 3  # Under limit of 5
            
            mock_session.return_value.query.return_value = mock_query
            mock_session.return_value.close.return_value = None
            
            result = self.scheduler._exceeds_daily_limit(test_date)
            
            self.assertFalse(result)
    
    def test_should_auto_post(self):
        """Test auto-post criteria."""
        # Create mock article
        mock_article = Mock(spec=NewsArticle)
        mock_article.category = 'breaking'
        mock_article.headline = 'Breaking news test'
        mock_article.content = 'This is breaking news content'
        mock_article.image_url = 'https://test.com/image.jpg'
        
        result = self.scheduler._should_auto_post(mock_article)
        
        self.assertTrue(result)
    
    def test_determine_template_type(self):
        """Test template type determination."""
        mock_article = Mock(spec=NewsArticle)
        mock_article.headline = 'Breaking: Test news'
        mock_article.content = 'Breaking news content'
        mock_article.category = 'breaking'
        
        template_type = self.scheduler._determine_template_type(mock_article)
        
        self.assertEqual(template_type, 'breaking')
    
    def test_get_schedule_status(self):
        """Test getting schedule status."""
        with patch.object(self.scheduler.db_manager, 'get_session') as mock_session:
            mock_query = Mock()
            mock_query.filter.return_value = mock_query
            mock_query.order_by.return_value = mock_query
            mock_query.limit.return_value = mock_query
            mock_query.all.return_value = []
            
            mock_session.return_value.query.return_value = mock_query
            mock_session.return_value.close.return_value = None
            
            status = self.scheduler.get_schedule_status()
            
            self.assertIn('is_running', status)
            self.assertIn('upcoming_posts', status)


if __name__ == '__main__':
    unittest.main()
