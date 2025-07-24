#!/usr/bin/env python3
"""
Test Instagram Publishing
This script will publish the generated posts to Instagram.
"""

import sys
import os
import asyncio
import logging
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from deploy.manual_automation import ManualAutomation

async def publish_posts():
    """Publish the generated posts to Instagram."""
    print("=== Publishing Generated Posts to Instagram ===")
    
    automation = ManualAutomation()
    
    # Initialize the automation system
    if not await automation.initialize():
        print("❌ Failed to initialize automation")
        return False
    
    # Get all pending posts from database
    session = automation.server.db_manager.get_session()
    from src.database.models import InstagramPost, PostStatus
    
    posts = session.query(InstagramPost).filter_by(status=PostStatus.DRAFT.value).all()
    
    if not posts:
        print("📝 No draft posts found to publish")
        session.close()
        return True
    
    print(f"📱 Found {len(posts)} posts ready to publish")
    
    published_count = 0
    for i, post in enumerate(posts[:3], 1):  # Publish first 3 posts
        print(f"\n📤 Publishing post {i}: {post.title[:50]}...")
        
        try:
            result = automation.server.instagram_publisher.publish_post(post.id)
            
            if result['success']:
                print(f"✅ Post {i} published successfully!")
                print(f"   Instagram URL: {result.get('url', 'Not available')}")
                published_count += 1
            else:
                print(f"❌ Failed to publish post {i}: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error publishing post {i}: {e}")
    
    session.close()
    
    print(f"\n📊 Publishing Summary:")
    print(f"   Posts Published: {published_count}")
    print(f"   Posts Failed: {len(posts[:3]) - published_count}")
    
    return published_count > 0

if __name__ == "__main__":
    success = asyncio.run(publish_posts())
    exit(0 if success else 1)
