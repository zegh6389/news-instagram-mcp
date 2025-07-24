#!/usr/bin/env python3
"""Debug Global News scraping to see what content is actually being extracted."""

import sys
import logging
import requests
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_globalnews_page(url: str):
    """Debug a Global News page to see what content is available."""
    print(f"🔍 Debugging Global News URL: {url}")
    print("=" * 80)
    
    try:
        # Fetch the page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        print(f"✅ Successfully fetched page (status: {response.status_code})")
        print(f"📄 Content length: {len(response.text)} characters")
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for common headline selectors
        print("\n📰 Checking for headlines:")
        headline_selectors = [
            'h1.c-detail__headline',
            'h1.l-article__headline',
            '.entry-title h1',
            'article h1',
            '.headline h1',
            'h1'
        ]
        
        for selector in headline_selectors:
            elements = soup.select(selector)
            if elements:
                for i, elem in enumerate(elements[:3]):  # Show first 3
                    text = elem.get_text(strip=True)
                    if text:
                        print(f"  {selector}: '{text[:100]}...'")
                        break
        
        # Check for content selectors
        print("\n📝 Checking for content:")
        content_selectors = [
            '.l-article__body p',
            '.c-detail__body p',
            '.entry-content p',
            'article .content p',
            '.post-content p',
            'article p',  # More generic
            '.content p'  # Even more generic
        ]
        
        for selector in content_selectors:
            paragraphs = soup.select(selector)
            if paragraphs:
                total_text = ""
                valid_paragraphs = 0
                for p in paragraphs[:5]:  # Check first 5 paragraphs
                    text = p.get_text(strip=True)
                    if text and len(text) > 20:  # Basic validation
                        total_text += text + " "
                        valid_paragraphs += 1
                
                if valid_paragraphs > 0:
                    print(f"  {selector}: Found {valid_paragraphs} valid paragraphs")
                    print(f"    Sample: '{total_text[:200]}...'")
                    print(f"    Total length: {len(total_text)} characters")
        
        # Check for any paragraphs at all
        print("\n🔍 All paragraph elements:")
        all_paragraphs = soup.find_all('p')
        print(f"  Total <p> elements found: {len(all_paragraphs)}")
        
        for i, p in enumerate(all_paragraphs[:10]):  # Show first 10
            text = p.get_text(strip=True)
            if text:
                print(f"    P{i+1}: '{text[:100]}...' (length: {len(text)})")
        
        # Check page structure
        print("\n🏗️ Page structure:")
        main_content = soup.find('main') or soup.find('article') or soup.find('.content')
        if main_content:
            print(f"  Found main content container: {main_content.name}")
            if main_content.get('class'):
                print(f"  Classes: {main_content.get('class')}")
        
        # Look for common Global News specific elements
        print("\n🌐 Global News specific elements:")
        gn_elements = [
            '.c-detail',
            '.l-article',
            '.article-content',
            '[data-module="ArticleBody"]'
        ]
        
        for selector in gn_elements:
            elements = soup.select(selector)
            if elements:
                print(f"  Found: {selector} ({len(elements)} elements)")
        
    except Exception as e:
        print(f"❌ Error debugging page: {e}")

if __name__ == "__main__":
    # Test with a specific Global News URL
    test_url = "https://globalnews.ca/news/11301609/bichettes-two-run-shot-caps-wild-blue-jays-win/"
    debug_globalnews_page(test_url)
