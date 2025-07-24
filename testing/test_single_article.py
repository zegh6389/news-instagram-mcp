#!/usr/bin/env python3
"""Test the improved Global News scraper."""

import logging
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.scrapers.globalnews_scraper import GlobalNewsScraper

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def test_globalnews_scraper():
    """Test the Global News scraper."""
    print("🧪 Testing improved Global News scraper...")
    
    # Create scraper with proper config
    source_config = {
        'base_url': 'https://globalnews.ca',
        'rss_feeds': ['https://globalnews.ca/feed/'],
        'selectors': {}
    }
    scraper = GlobalNewsScraper('globalnews', source_config)
    test_url = "https://globalnews.ca/news/11301609/bichettes-two-run-shot-caps-wild-blue-jays-win/"
    
    print(f"📰 Testing URL: {test_url}")
    
    result = scraper.scrape_article_content(test_url)
    
    if result:
        print("✅ SUCCESS!")
        print(f"📄 Headline: {result.get('headline', 'N/A')}")
        print(f"📝 Content length: {len(result.get('content', ''))} characters")
        print(f"👤 Author: {result.get('author', 'N/A')}")
        print(f"📅 Published: {result.get('published_date', 'N/A')}")
        print(f"🖼️ Image: {result.get('image_url', 'N/A')}")
        print(f"📋 Summary: {result.get('summary', 'N/A')[:100]}...")
        
        # Show content preview
        content = result.get('content', '')
        if content:
            print(f"\n📖 Content preview (first 300 chars):")
            print(f"{content[:300]}...")
    else:
        print("❌ FAILED - No content extracted")

if __name__ == "__main__":
    test_globalnews_scraper()
