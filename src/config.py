"""Configuration management for the news-instagram-mcp project."""

import os
import yaml
from typing import Dict, Any, List
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Main configuration class."""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.load_configs()
    
    def load_configs(self):
        """Load all configuration files."""
        # Environment variables
        self.instagram_username = os.getenv('INSTAGRAM_USERNAME')
        self.instagram_password = os.getenv('INSTAGRAM_PASSWORD')
        self.instagram_session_file = os.getenv('INSTAGRAM_SESSION_FILE', 'instagram_session.json')
        
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.openai_model = os.getenv('OPENAI_MODEL', 'gpt-4')
        
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.gemini_model = os.getenv('GEMINI_MODEL', 'gemini-pro')
        
        # Database URL with proper fallback for GitHub Actions
        database_url = os.getenv('DATABASE_URL')
        if not database_url or database_url == 'sqlite:///tmp/news_instagram.db':
            # For GitHub Actions or when DATABASE_URL is not properly set
            self.database_url = 'sqlite:////tmp/news_instagram.db'
        else:
            self.database_url = database_url
        
        self.user_agent = os.getenv('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        self.request_delay = int(os.getenv('REQUEST_DELAY', '2'))
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        
        self.max_caption_length = int(os.getenv('MAX_CAPTION_LENGTH', '2200'))
        self.image_max_width = int(os.getenv('IMAGE_MAX_WIDTH', '1080'))
        self.image_max_height = int(os.getenv('IMAGE_MAX_HEIGHT', '1350'))
        
        self.post_schedule_interval = int(os.getenv('POST_SCHEDULE_INTERVAL', '3600'))
        self.max_posts_per_day = int(os.getenv('MAX_POSTS_PER_DAY', '5'))
        
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.log_file = os.getenv('LOG_FILE', 'logs/news_instagram.log')
        
        # Load YAML configurations
        self.news_sources = self._load_yaml_config('config/news_sources.yaml')
        self.instagram_config = self._load_yaml_config('config/instagram_config.yaml')
        self.template_config = self._load_yaml_config('config/template_config.yaml')
    
    def _load_yaml_config(self, config_path: str) -> Dict[str, Any]:
        """Load a YAML configuration file."""
        full_path = self.base_dir / config_path
        try:
            with open(full_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Warning: Configuration file {config_path} not found")
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file {config_path}: {e}")
            return {}
    
    def get_news_sources(self) -> Dict[str, Any]:
        """Get enabled news sources."""
        sources = {}
        for source_id, source_config in self.news_sources.get('news_sources', {}).items():
            if source_config.get('enabled', False):
                sources[source_id] = source_config
        return sources
    
    def get_categories(self) -> Dict[str, Any]:
        """Get news categories configuration."""
        return self.news_sources.get('categories', {})
    
    def get_content_filters(self) -> Dict[str, Any]:
        """Get content filtering rules."""
        return self.news_sources.get('content_filters', {})
    
    def get_instagram_posting_config(self) -> Dict[str, Any]:
        """Get Instagram posting configuration."""
        return self.instagram_config.get('instagram', {}).get('posting', {})
    
    def get_hashtags_config(self) -> Dict[str, Any]:
        """Get hashtags configuration."""
        return self.instagram_config.get('hashtags', {})
    
    def get_caption_templates(self) -> Dict[str, str]:
        """Get caption templates."""
        return self.instagram_config.get('captions', {}).get('templates', {})
    
    def get_template_config(self, template_name: str) -> Dict[str, Any]:
        """Get specific template configuration."""
        return self.template_config.get('templates', {}).get(template_name, {})

# Global configuration instance
config = Config()
