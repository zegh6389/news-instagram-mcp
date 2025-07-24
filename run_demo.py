#!/usr/bin/env python3
"""
Demo launcher for News Instagram MCP Server
Handles all import setup automatically
"""

import sys
import os
import asyncio
from pathlib import Path

def setup_paths():
    """Setup Python paths for proper imports"""
    project_root = Path(__file__).parent
    src_dir = project_root / 'src'
    
    # Add to Python path
    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(src_dir))
    
    # Set working directory
    os.chdir(project_root)
    
    return project_root, src_dir

async def run_live_demo():
    """Run the live Instagram demo"""
    
    print("🚀 Starting News Instagram MCP Demo...")
    print("=" * 50)
    
    try:
        # Setup paths
        setup_paths()
        
        # Import after path setup
        from mcp_server import NewsInstagramMCPServer
        
        print("\n🔧 Initializing MCP server...")
        server = NewsInstagramMCPServer()
        
        # Step 1: Scrape recent news
        print("\n📰 Step 1: Scraping recent news...")
        scrape_result = await server._scrape_news_tool({'limit': 5})
        print("✅ News scraped successfully")
        
        # Step 2: Analyze content
        print("\n🔍 Step 2: Analyzing content...")
        analysis_result = await server._analyze_content_tool({'limit': 3})
        print("✅ Content analyzed")
        
        # Step 3: Check for articles
        print("\n📝 Step 3: Finding articles...")
        articles = server.db_manager.get_recent_articles(limit=1)
        
        if articles:
            article = articles[0]
            print(f"\n📄 Found article: {article.headline[:50]}...")
            
            # Step 4: Generate Instagram post
            print("\n🎨 Step 4: Generating Instagram post...")
            post_result = await server._generate_post_tool({
                'article_id': article.id,
                'template_type': 'breaking'
            })
            print("✅ Post generated successfully")
            
            # Step 5: Publish to Instagram
            print("\n📱 Step 5: Publishing to Instagram...")
            publish_result = await server._publish_post_tool({
                'post_id': None,  # Will use latest generated post
            })
            
            print("🎉 SUCCESS: Post published!")
            for content in publish_result:
                print(f"📄 Result: {content.text}")
                
        else:
            print("\n⚠️ No articles found - creating demo post...")
            
            # Create demo post
            demo_result = await server._publish_post_tool({
                'post_id': None,
                'caption_override': '🚀 Live Demo: News Instagram MCP Server is working! This automated system scrapes news, analyzes content, and posts to Instagram. #AI #Automation #MCP #NewsBot'
            })
            
            if demo_result:
                print("🎉 SUCCESS: Demo post published!")
                for content in demo_result:
                    print(f"📄 Result: {content.text}")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure you're in the project directory and all dependencies are installed")
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(run_live_demo())
    except KeyboardInterrupt:
        print("\n⏹️ Demo stopped by user")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
