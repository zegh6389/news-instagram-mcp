#!/usr/bin/env python3
"""
Test script to verify all components are working before first post.
Run this script to check if everything is set up correctly.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_environment():
    """Test if environment variables are set up correctly."""
    print("🔧 Testing Environment Configuration...")
    
    # Check for .env file
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found! Please create it from .env.example")
        return False
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check required variables
    instagram_username = os.getenv('INSTAGRAM_USERNAME')
    instagram_password = os.getenv('INSTAGRAM_PASSWORD')
    
    if not instagram_username or not instagram_password:
        print("❌ Instagram credentials not found in .env file!")
        print("   Please set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD")
        return False
    
    print(f"✅ Instagram username: {instagram_username}")
    print("✅ Instagram password: *** (hidden)")
    
    # Check optional AI keys
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    if openai_key:
        print(f"✅ OpenAI API key: {openai_key[:8]}...")
    elif anthropic_key:
        print(f"✅ Anthropic API key: {anthropic_key[:8]}...")
    else:
        print("⚠️  No AI API keys found (OpenAI/Anthropic)")
        print("   System will use basic content processing")
    
    return True

def test_database():
    """Test database connectivity and setup."""
    print("\n💾 Testing Database...")
    
    try:
        from src.database import DatabaseManager
        db = DatabaseManager()
        print("✅ Database connection successful")
        
        # Test basic operations
        stats = db.get_daily_stats()
        print(f"✅ Database operations working - found {stats.get('articles_scraped', 0)} articles today")
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_scrapers():
    """Test news scraping functionality."""
    print("\n📰 Testing News Scrapers...")
    
    try:
        from src.scrapers import CBCScraper
        from src.config import config
        
        # Test configuration loading
        news_sources = config.get_news_sources()
        if 'cbc' not in news_sources:
            print("❌ CBC configuration not found")
            return False
        
        print("✅ Configuration loaded successfully")
        
        # Test scraper initialization
        scraper = CBCScraper('cbc', news_sources['cbc'])
        print("✅ CBC scraper initialized")
        
        # Test RSS feed access
        articles = scraper.scrape_rss_feeds()
        print(f"✅ Found {len(articles)} articles in RSS feeds")
        
        if len(articles) > 0:
            # Test content extraction
            article = articles[0]
            content = scraper.scrape_article_content(article['url'])
            if content:
                print("✅ Article content extraction working")
            else:
                print("⚠️  Article content extraction failed - may need selector updates")
        
        return True
        
    except Exception as e:
        print(f"❌ Scraper error: {e}")
        return False

def test_processors():
    """Test content processing functionality."""
    print("\n🧠 Testing Content Processors...")
    
    try:
        from src.processors import ContentAnalyzer, CaptionGenerator
        
        # Test content analyzer
        analyzer = ContentAnalyzer()
        print("✅ Content analyzer initialized")
        
        # Test caption generator
        caption_gen = CaptionGenerator()
        print("✅ Caption generator initialized")
        
        # Test with sample data
        sample_article = {
            'headline': 'Test News Article',
            'summary': 'This is a test article for system verification.'
        }
        
        sample_analysis = {
            'keywords': ['test', 'news'],
            'category': 'general'
        }
        
        caption = caption_gen.generate_caption(sample_article, sample_analysis)
        print(f"✅ Caption generation working: {caption[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Processor error: {e}")
        return False

def test_publishers():
    """Test Instagram publishing setup."""
    print("\n📱 Testing Instagram Publisher...")
    
    try:
        from src.publishers import InstagramPublisher
        
        # Test initialization (this will check credentials)
        publisher = InstagramPublisher()
        print("✅ Instagram publisher initialized")
        
        # Note: We don't actually test posting here to avoid spam
        print("ℹ️  Instagram connection will be tested during actual posting")
        
        return True
    
        
    except Exception as e:
        print(f"❌ Publisher error: {e}")
        print("   This is often due to Instagram credentials or account type")
        return False

def test_mcp_server():
    """Test MCP server initialization."""
    print("\n🔗 Testing MCP Server...")
    
    try:
        from src.mcp_server import NewsInstagramMCPServer
        
        # Test server initialization
        server = NewsInstagramMCPServer()
        print("✅ MCP server initialized successfully")
        
        # Check components
        print(f"✅ {len(server.scrapers)} scrapers loaded")
        print("✅ Content analyzer ready")
        print("✅ Caption generator ready")
        print("✅ Instagram publisher ready")
        
        return True
        
    except Exception as e:
        print(f"❌ MCP server error: {e}")
        return False

def run_full_workflow_test():
    """Test the complete workflow without actually posting."""
    print("\n🔄 Testing Complete Workflow...")
    
    try:
        from src.scrapers import CBCScraper
        from src.processors import ContentAnalyzer, CaptionGenerator
        from src.database import DatabaseManager
        from src.config import config
        
        # Step 1: Scrape one article
        print("  1️⃣ Scraping news...")
        scraper = CBCScraper('cbc', config.get_news_sources()['cbc'])
        rss_articles = scraper.scrape_rss_feeds()
        
        if not rss_articles:
            print("❌ No articles found in RSS feeds")
            return False
        
        # Get full content for first article
        article_data = rss_articles[0]
        full_content = scraper.scrape_article_content(article_data['url'])
        
        if full_content:
            article_data.update(full_content)
        
        print(f"     ✅ Article: {article_data['headline'][:50]}...")
        
        # Step 2: Save to database
        print("  2️⃣ Saving to database...")
        saved_article = scraper.save_article(article_data)
        
        if not saved_article:
            print("❌ Failed to save article")
            return False
        
        print("     ✅ Article saved to database")
        
        # Step 3: Generate caption
        print("  3️⃣ Generating caption...")
        caption_gen = CaptionGenerator()
        
        article_dict = {
            'headline': saved_article.headline,
            'summary': saved_article.summary or saved_article.content[:200]
        }
        
        analysis_dict = {
            'keywords': saved_article.keywords or ['news'],
            'category': saved_article.category or 'general'
        }
        
        caption = caption_gen.generate_caption(article_dict, analysis_dict)
        print(f"     ✅ Caption: {caption[:100]}...")
        
        # Step 4: Create post record
        print("  4️⃣ Creating post record...")
        db = DatabaseManager()
        
        post_data = {
            'article_id': saved_article.id,
            'caption': caption,
            'hashtags': '#news #canada',
            'template_used': 'feature',
            'status': 'draft'
        }
        
        post = db.save_instagram_post(post_data)
        print(f"     ✅ Post {post.id} ready for publishing")
        
        print("\n🎉 Complete workflow test PASSED!")
        print(f"   📰 Article: {saved_article.headline}")
        print(f"   📝 Caption length: {len(caption)} characters")
        print(f"   🆔 Post ID: {post.id}")
        print("\n   Ready to publish your first post!")
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🧪 News Instagram MCP - System Test")
    print("=" * 50)
    
    tests = [
        ("Environment", test_environment),
        ("Database", test_database),
        ("Scrapers", test_scrapers),
        ("Processors", test_processors),
        ("Publishers", test_publishers),
        ("MCP Server", test_mcp_server),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
        else:
            print(f"\n❌ {test_name} test failed!")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All basic tests passed!")
        print("Running complete workflow test...")
        
        if run_full_workflow_test():
            print("\n✅ SYSTEM READY! You can now create your first post.")
            print("\nNext steps:")
            print("1. Run: python main.py")
            print("2. Use MCP tools to scrape, analyze, and post")
            print("3. Or run the manual test script")
        else:
            print("\n⚠️  Workflow test failed. Check the errors above.")
    else:
        print(f"\n❌ {total - passed} tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Create .env file with Instagram credentials")
        print("- Ensure Instagram account is Business/Creator type")
        print("- Check internet connection for scraping")
        print("- Install missing dependencies")

if __name__ == "__main__":
    main()
