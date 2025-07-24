#!/usr/bin/env python3
"""
Live Instagram Demo Script
Creates and publishes a real Instagram post using the MCP server
"""

import asyncio
import sys
import os
from pathlib import Path

# Setup paths properly
project_root = Path(__file__).parent
src_dir = project_root / 'src'

# Add to Python path
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_dir))

# Change to project directory
os.chdir(project_root)

# Import the MCP server
sys.path.insert(0, str(src_dir))
from mcp_server import NewsInstagramMCPServer

async def live_instagram_demo():
    """Run a live demo creating and publishing an Instagram post"""
    
    print('🎯 Live Instagram Demo - Creating Real Post!')
    print('=' * 50)
    
    try:
        server = NewsInstagramMCPServer()
        
        # Step 1: Scrape recent news
        print('\n📰 Step 1: Scraping recent news...')
        await server._scrape_news_tool({'source': 'globalnews', 'limit': 5})
        print('✅ News scraped successfully')
        
        # Step 2: Analyze content
        print('\n🔍 Step 2: Analyzing content...')
        await server._analyze_content_tool({'limit': 3})
        print('✅ Content analyzed')
        
        # Step 3: Check if we have articles to work with
        articles = server.db_manager.get_recent_articles(limit=1)
        if articles:
            article = articles[0]
            print(f'\n📝 Found article: {article.headline[:50]}...')
            
            # Step 4: Generate Instagram post
            print('\n🎨 Step 3: Generating Instagram post...')
            await server._generate_post_tool({
                'article_id': article.id,
                'template_type': 'breaking',
                'caption_style': 'engaging'
            })
            print('✅ Post generated successfully')
            
            # Step 5: Publish to Instagram
            print('\n📱 Step 4: Publishing to Instagram...')
            result = await server._publish_post_tool({
                'post_id': None,  # Will use the latest generated post
                'caption_override': 'Live demo post from News Instagram MCP Server! 🚀 #NewsAutomation #MCP'
            })
            
            print('🎉 SUCCESS: Post published to Instagram!')
            for content in result:
                print(f'📄 Result: {content.text}')
        else:
            print('\n⚠️ No articles found to create post from')
            print('Creating demo post with sample content...')
            
            result = await server._publish_post_tool({
                'post_id': None,
                'caption_override': '🚀 Live Demo: News Instagram MCP Server is now integrated with Claude Desktop! This automated system can scrape news, analyze content, and post to Instagram. #AI #Automation #MCP #NewsBot'
            })
            
            if result:
                print('🎉 SUCCESS: Demo post published!')
                for content in result:
                    print(f'📄 Result: {content.text}')
                
    except Exception as e:
        print(f'❌ Error during demo: {e}')

if __name__ == "__main__":
    asyncio.run(live_instagram_demo())
