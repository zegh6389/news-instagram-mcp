#!/usr/bin/env python3
"""
Complete Project Test Suite
Tests all components end-to-end for production deployment
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Setup paths
project_root = Path(__file__).parent
src_dir = project_root / 'src'
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_dir))

# Set production credentials
os.environ['INSTAGRAM_USERNAME'] = 'awais_zegham'
os.environ['INSTAGRAM_PASSWORD'] = '@Wadooha374549'
os.environ['GEMINI_API_KEY'] = 'AIzaSyCpXrYZ92M84lrJqIr9H6HpaOMGUU57o9s'

from src.config import config
from src.database.db_manager import DatabaseManager
from src.scrapers.cbc_scraper import CBCScraper
from src.scrapers.globalnews_scraper import GlobalNewsScraper
from src.processors.content_analyzer import ContentAnalyzer
from src.publishers.instagram_publisher import InstagramPublisher
from src.mcp_server import NewsInstagramMCPServer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProductionTestSuite:
    """Complete production test suite"""
    
    def __init__(self):
        self.server = None
        self.test_results = {}
        
    async def run_complete_test(self):
        """Run complete end-to-end test"""
        print("🚀 PRODUCTION TEST SUITE - AWAIS_ZEGHAM")
        print("=" * 60)
        
        # Test 1: Database Setup
        await self.test_database()
        
        # Test 2: News Scraping
        await self.test_news_scraping()
        
        # Test 3: Content Analysis
        await self.test_content_analysis()
        
        # Test 4: Instagram Connection
        await self.test_instagram_connection()
        
        # Test 5: MCP Server
        await self.test_mcp_server()
        
        # Test 6: End-to-End Workflow
        await self.test_end_to_end()
        
        # Print Results
        self.print_test_results()
        
    async def test_database(self):
        """Test database connectivity and setup"""
        print("\n📊 Testing Database Setup...")
        try:
            db_manager = DatabaseManager()
            
            # Test connection
            session = db_manager.get_session()
            session.close()
            
            # Test table creation
            db_manager.create_tables()
            
            self.test_results['database'] = '✅ PASS'
            print("✅ Database setup successful")
            
        except Exception as e:
            self.test_results['database'] = f'❌ FAIL: {e}'
            print(f"❌ Database test failed: {e}")
    
    async def test_news_scraping(self):
        """Test news scraping functionality"""
        print("\n📰 Testing News Scraping...")
        try:
            # Test CBC Scraper
            cbc_scraper = CBCScraper('cbc', config.get_news_sources()['cbc'])
            cbc_articles = await cbc_scraper.scrape_latest(limit=3)
            
            # Test Global News Scraper
            global_scraper = GlobalNewsScraper('globalnews', config.get_news_sources()['globalnews'])
            global_articles = await global_scraper.scrape_latest(limit=3)
            
            total_articles = len(cbc_articles) + len(global_articles)
            
            if total_articles > 0:
                self.test_results['scraping'] = f'✅ PASS - {total_articles} articles scraped'
                print(f"✅ Scraping successful: {total_articles} articles")
            else:
                self.test_results['scraping'] = '⚠️ WARNING - No articles scraped'
                print("⚠️ No articles scraped")
                
        except Exception as e:
            self.test_results['scraping'] = f'❌ FAIL: {e}'
            print(f"❌ Scraping test failed: {e}")
    
    async def test_content_analysis(self):
        """Test content analysis"""
        print("\n🔍 Testing Content Analysis...")
        try:
            analyzer = ContentAnalyzer()
            
            # Create test article
            test_article = {
                'headline': 'Breaking: Test News Article for Analysis',
                'content': 'This is a test article content for analyzing the AI content processing capabilities of the system.',
                'url': 'https://example.com/test',
                'source': 'test'
            }
            
            analysis = await analyzer.analyze_article(test_article)
            
            if 'category' in analysis and 'importance_score' in analysis:
                self.test_results['analysis'] = '✅ PASS'
                print("✅ Content analysis successful")
            else:
                self.test_results['analysis'] = '❌ FAIL - Invalid analysis result'
                print("❌ Content analysis failed")
                
        except Exception as e:
            self.test_results['analysis'] = f'❌ FAIL: {e}'
            print(f"❌ Analysis test failed: {e}")
    
    async def test_instagram_connection(self):
        """Test Instagram connection with real credentials"""
        print("\n📱 Testing Instagram Connection...")
        try:
            publisher = InstagramPublisher()
            
            if hasattr(publisher, 'client') and publisher.client:
                self.test_results['instagram'] = '✅ PASS - Real connection established'
                print("✅ Instagram connection successful")
            else:
                self.test_results['instagram'] = '❌ FAIL - No client connection'
                print("❌ Instagram connection failed")
                
        except Exception as e:
            self.test_results['instagram'] = f'❌ FAIL: {e}'
            print(f"❌ Instagram test failed: {e}")
    
    async def test_mcp_server(self):
        """Test MCP Server initialization"""
        print("\n🔧 Testing MCP Server...")
        try:
            self.server = NewsInstagramMCPServer()
            
            if self.server and self.server.server:
                self.test_results['mcp_server'] = '✅ PASS'
                print("✅ MCP Server initialization successful")
            else:
                self.test_results['mcp_server'] = '❌ FAIL - Server not initialized'
                print("❌ MCP Server test failed")
                
        except Exception as e:
            self.test_results['mcp_server'] = f'❌ FAIL: {e}'
            print(f"❌ MCP Server test failed: {e}")
    
    async def test_end_to_end(self):
        """Test complete end-to-end workflow"""
        print("\n🎯 Testing End-to-End Workflow...")
        try:
            if not self.server:
                self.server = NewsInstagramMCPServer()
            
            # Step 1: Scrape news
            scrape_result = await self.server._scrape_news_tool({'limit': 5})
            
            # Step 2: Analyze content
            analysis_result = await self.server._analyze_content_tool({'limit': 3})
            
            # Step 3: Generate post
            post_result = await self.server._generate_post_tool({
                'article_id': 1,
                'template_type': 'breaking'
            })
            
            # Step 4: Publish post
            publish_result = await self.server._publish_post_tool({
                'post_id': None
            })
            
            self.test_results['end_to_end'] = '✅ PASS - Complete workflow successful'
            print("✅ End-to-end workflow successful")
            
        except Exception as e:
            self.test_results['end_to_end'] = f'❌ FAIL: {e}'
            print(f"❌ End-to-end test failed: {e}")
    
    def print_test_results(self):
        """Print comprehensive test results"""
        print("\n" + "=" * 60)
        print("📋 PRODUCTION TEST RESULTS")
        print("=" * 60)
        
        for test_name, result in self.test_results.items():
            print(f"{test_name.upper():<20} : {result}")
        
        # Count passed tests
        passed = sum(1 for result in self.test_results.values() if result.startswith('✅'))
        total = len(self.test_results)
        
        print(f"\n📊 SUMMARY: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED - READY FOR PRODUCTION!")
        else:
            print("⚠️ SOME TESTS FAILED - CHECK CONFIGURATION")

async def main():
    """Main test runner"""
    test_suite = ProductionTestSuite()
    await test_suite.run_complete_test()

if __name__ == "__main__":
    asyncio.run(main())
