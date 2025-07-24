#!/usr/bin/env python3
"""
Test and fix content scraping issues
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.mcp_server import NewsInstagramMCPServer

async def test_content_scraping():
    """Test content scraping with improved error handling"""
    
    print('🔧 Testing Content Scraping Fixes')
    print('=' * 50)
    
    try:
        server = NewsInstagramMCPServer()
        
        # Test each news source individually
        sources = ['globalnews', 'cbc', 'ctv']
        
        for source in sources:
            print(f'\n📰 Testing {source.upper()} scraping...')
            
            try:
                result = await server._scrape_news_tool({
                    'source': source, 
                    'limit': 3
                })
                
                if result and len(result) > 0:
                    print(f'✅ {source}: Successfully scraped content')
                    # Parse the response to get actual article count
                    response_text = result[0].text
                    if 'Total articles found:' in response_text:
                        lines = response_text.split('\n')
                        for line in lines:
                            if 'Total articles found:' in line:
                                print(f'   {line.strip()}')
                            elif 'Successfully scraped:' in line:
                                print(f'   {line.strip()}')
                            elif 'Failed:' in line:
                                print(f'   {line.strip()}')
                else:
                    print(f'⚠️ {source}: No content returned')
                    
            except Exception as e:
                print(f'❌ {source}: Error - {e}')
        
        # Check database for scraped articles
        print('\n📊 Checking database for articles...')
        articles = server.db_manager.get_recent_articles(limit=10)
        
        if articles:
            print(f'✅ Found {len(articles)} articles in database:')
            for article in articles[:3]:  # Show first 3
                print(f'   - {article.source}: {article.headline[:60]}...')
                print(f'     Content length: {len(article.content)} characters')
        else:
            print('⚠️ No articles found in database')
            
        # Test content analysis
        print('\n🔍 Testing content analysis...')
        analysis_result = await server._analyze_content_tool({'limit': 5})
        
        if analysis_result:
            print('✅ Content analysis completed')
            print(f'   Response preview: {analysis_result[0].text[:100]}...')
        else:
            print('❌ Content analysis failed')
            
    except Exception as e:
        print(f'❌ Error during testing: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_content_scraping())
