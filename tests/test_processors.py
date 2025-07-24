"""Tests for content processors."""

import pytest
import unittest
from unittest.mock import Mock, patch, MagicMock, mock_open
from datetime import datetime

from src.processors import ContentAnalyzer, ImageProcessor, CaptionGenerator
from src.database.models import NewsArticle


class TestContentAnalyzer(unittest.TestCase):
    """Test content analyzer functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        with patch('src.processors.content_analyzer.DatabaseManager'):
            self.analyzer = ContentAnalyzer()
        
        # Create mock article
        self.mock_article = Mock(spec=NewsArticle)
        self.mock_article.id = 1
        self.mock_article.headline = 'Breaking: Test News Article'
        self.mock_article.content = 'This is a test news article about breaking news in Canada. The government announced new policies today.'
        self.mock_article.source = 'Test News'
        self.mock_article.category = 'politics'
        self.mock_article.keywords = ['breaking', 'government', 'canada']
        self.mock_article.published_date = datetime.utcnow()
        self.mock_article.scraped_date = datetime.utcnow()
    
    def test_categorize_article(self):
        """Test article categorization."""
        category = self.analyzer._categorize_article(self.mock_article)
        
        # Should detect 'breaking' category due to keywords
        self.assertIn(category, ['breaking', 'politics'])
    
    def test_analyze_sentiment(self):
        """Test sentiment analysis."""
        sentiment = self.analyzer._analyze_sentiment(self.mock_article)
        
        self.assertIn('polarity', sentiment)
        self.assertIn('classification', sentiment)
        self.assertIn(sentiment['classification'], ['positive', 'negative', 'neutral'])
    
    def test_extract_keywords(self):
        """Test keyword extraction."""
        keywords = self.analyzer._extract_keywords(self.mock_article)
        
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)
    
    def test_calculate_importance_score(self):
        """Test importance score calculation."""
        score = self.analyzer._calculate_importance_score(self.mock_article)
        
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 10.0)


class TestImageProcessor(unittest.TestCase):
    """Test image processor functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        with patch('src.processors.image_processor.DatabaseManager'):
            self.processor = ImageProcessor()
    
    @patch('src.processors.image_processor.requests.get')
    def test_download_image(self, mock_get):
        """Test image downloading."""
        # Mock response
        mock_response = Mock()
        mock_response.headers = {'content-type': 'image/jpeg'}
        mock_response.iter_content.return_value = [b'fake_image_data']
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with patch('src.processors.image_processor.Path.exists', return_value=False), \
             patch('builtins.open', mock_open()), \
             patch.object(self.processor, '_verify_image', return_value=True):
            
            result = self.processor.download_image('https://test.com/image.jpg', 1)
            
            self.assertIsNotNone(result)
    
    def test_get_image_info(self):
        """Test getting image information."""
        # This would require a real image file, so we'll mock it
        with patch('PIL.Image.open') as mock_open:
            mock_img = Mock()
            mock_img.width = 1080
            mock_img.height = 1350
            mock_img.mode = 'RGB'
            mock_img.format = 'JPEG'
            mock_open.return_value.__enter__.return_value = mock_img
            
            with patch('pathlib.Path.exists', return_value=True), \
                 patch('pathlib.Path.stat') as mock_stat:
                mock_stat.return_value.st_size = 1024000
                
                info = self.processor.get_image_info('test.jpg')
                
                self.assertEqual(info['width'], 1080)
                self.assertEqual(info['height'], 1350)


class TestCaptionGenerator(unittest.TestCase):
    """Test caption generator functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        with patch('src.processors.caption_generator.DatabaseManager'):
            self.generator = CaptionGenerator()
        
        # Create mock article
        self.mock_article = Mock(spec=NewsArticle)
        self.mock_article.id = 1
        self.mock_article.headline = 'Test News Headline'
        self.mock_article.content = 'This is test content for the news article.'
        self.mock_article.summary = 'Test summary'
        self.mock_article.source = 'Test News'
        self.mock_article.category = 'general'
        self.mock_article.keywords = ['test', 'news']
        self.mock_article.published_date = datetime.utcnow()
    
    def test_determine_template_type(self):
        """Test template type determination."""
        template_type = self.generator._determine_template_type(self.mock_article)
        
        self.assertIn(template_type, ['breaking', 'analysis', 'feature'])
    
    def test_get_hashtags(self):
        """Test hashtag generation."""
        hashtags = self.generator._get_hashtags(self.mock_article)
        
        self.assertIsInstance(hashtags, list)
        self.assertGreater(len(hashtags), 0)
        
        # All hashtags should start with #
        for hashtag in hashtags:
            self.assertTrue(hashtag.startswith('#'))
    
    def test_validate_caption(self):
        """Test caption validation."""
        test_caption = "This is a test caption #test #news"
        
        validation = self.generator.validate_caption(test_caption)
        
        self.assertIn('is_valid', validation)
        self.assertIn('length', validation)
        self.assertIn('hashtag_count', validation)
    
    def test_generate_template_caption(self):
        """Test template-based caption generation."""
        result = self.generator._generate_template_caption(self.mock_article, 'feature')
        
        self.assertIn('caption', result)
        self.assertIn('hashtags', result)
        self.assertIn('template_type', result)
        self.assertEqual(result['template_type'], 'feature')


if __name__ == '__main__':
    unittest.main()
