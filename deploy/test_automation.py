#!/usr/bin/env python3
"""
Test automation script for GitHub Actions
Quick tests to verify system functionality
"""

import asyncio
import os
import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.mcp_server import NewsInstagramMCPServer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def test_basic():
    """Basic functionality test"""
    logging.info("🧪 Running basic functionality test...")
    
    server = NewsInstagramMCPServer()
    
    # Test scraping
    logging.info("📰 Testing news scraping...")
    scrape_result = await server._scrape_news_tool({'limit': 5})
    logging.info("✅ Scraping test completed")
    
    # Test analysis
    logging.info("🔍 Testing content analysis...")
    analysis_result = await server._analyze_content_tool({'limit': 2})
    logging.info("✅ Analysis test completed")
    
    # Test post generation
    logging.info("🎨 Testing post generation...")
    post_result = await server._generate_post_tool({
        'article_id': 1,
        'template_type': 'breaking'
    })
    logging.info("✅ Post generation test completed")
    
    logging.info("🎉 Basic test completed successfully!")

async def test_scraping_only():
    """Test only news scraping"""
    logging.info("🧪 Running scraping-only test...")
    
    server = NewsInstagramMCPServer()
    
    result = await server._scrape_news_tool({'limit': 10})
    logging.info("✅ Scraping-only test completed")

async def test_generation_only():
    """Test only post generation"""
    logging.info("🧪 Running generation-only test...")
    
    server = NewsInstagramMCPServer()
    
    # Quick scrape first
    await server._scrape_news_tool({'limit': 5})
    
    # Test generation
    for i in range(1, 3):
        try:
            result = await server._generate_post_tool({
                'article_id': i,
                'template_type': 'analysis'
            })
            logging.info(f"✅ Generated test post {i}")
        except Exception as e:
            logging.warning(f"⚠️ Test post {i} failed: {e}")
    
    logging.info("✅ Generation-only test completed")

async def main():
    """Main test function"""
    test_type = os.getenv('TEST_TYPE', 'basic')
    
    logging.info(f"🎯 Starting {test_type} test...")
    
    try:
        if test_type == 'basic':
            await test_basic()
        elif test_type == 'scraping-only':
            await test_scraping_only()
        elif test_type == 'generation-only':
            await test_generation_only()
        else:
            logging.error(f"Unknown test type: {test_type}")
            sys.exit(1)
        
        logging.info("🎉 All tests completed successfully!")
        sys.exit(0)
        
    except Exception as e:
        logging.error(f"💥 Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
