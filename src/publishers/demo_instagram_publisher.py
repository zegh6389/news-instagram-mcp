#!/usr/bin/env python3
"""
Demo Instagram Publisher - Simulates publishing without real Instagram API calls
This is for demonstration purposes when Instagram credentials aren't available
"""

import logging
import time
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

from ..database import DatabaseManager, InstagramPost, PostStatus

logger = logging.getLogger(__name__)

class DemoInstagramPublisher:
    """Demo publisher that simulates Instagram posting for testing."""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.client = "DEMO_CLIENT"  # Simulated client
        logger.info("Demo Instagram Publisher initialized (simulation mode)")
    
    def publish_post(self, post_id: int, caption_override: Optional[str] = None) -> Dict[str, Any]:
        """Simulate publishing a post to Instagram."""
        try:
            session = self.db_manager.get_session()
            post = session.query(InstagramPost).filter_by(id=post_id).first()
            
            if not post:
                session.close()
                return {'success': False, 'error': f'Post {post_id} not found'}
            
            # Use override caption if provided
            caption = caption_override or post.caption
            
            # Simulate posting delay
            time.sleep(2)
            
            # Generate fake Instagram post URL and ID
            fake_instagram_id = f"DEMO_{post_id}_{int(time.time())}"
            fake_post_url = f"https://instagram.com/p/{fake_instagram_id}/"
            
            # Update post status
            post.status = PostStatus.PUBLISHED.value
            post.instagram_id = fake_instagram_id
            post.instagram_url = fake_post_url
            post.published_at = datetime.utcnow()
            
            session.commit()
            session.close()
            
            logger.info(f"✅ DEMO: Successfully 'published' post {post_id}")
            logger.info(f"📱 Simulated Instagram URL: {fake_post_url}")
            logger.info(f"📝 Caption: {caption[:100]}...")
            
            return {
                'success': True,
                'instagram_id': fake_instagram_id,
                'url': fake_post_url,
                'message': f'Demo post published successfully! (Simulation mode)',
                'caption_length': len(caption)
            }
            
        except Exception as e:
            logger.error(f"Error in demo publishing: {e}")
            return {'success': False, 'error': str(e)}
    
    def publish_story(self, post_id: int) -> Dict[str, Any]:
        """Simulate publishing a story to Instagram."""
        try:
            # Simulate story posting
            time.sleep(1)
            
            fake_story_id = f"STORY_DEMO_{post_id}_{int(time.time())}"
            
            logger.info(f"✅ DEMO: Successfully 'published' story for post {post_id}")
            
            return {
                'success': True,
                'story_id': fake_story_id,
                'message': 'Demo story published successfully! (Simulation mode)'
            }
            
        except Exception as e:
            logger.error(f"Error in demo story publishing: {e}")
            return {'success': False, 'error': str(e)}
    
    def schedule_post(self, post_id: int, scheduled_time: datetime) -> Dict[str, Any]:
        """Simulate scheduling a post."""
        try:
            session = self.db_manager.get_session()
            post = session.query(InstagramPost).filter_by(id=post_id).first()
            
            if not post:
                session.close()
                return {'success': False, 'error': f'Post {post_id} not found'}
            
            post.status = PostStatus.SCHEDULED.value
            post.scheduled_for = scheduled_time
            
            session.commit()
            session.close()
            
            logger.info(f"✅ DEMO: Successfully 'scheduled' post {post_id} for {scheduled_time}")
            
            return {
                'success': True,
                'scheduled_for': scheduled_time.isoformat(),
                'message': f'Demo post scheduled successfully! (Simulation mode)'
            }
            
        except Exception as e:
            logger.error(f"Error in demo scheduling: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_account_info(self) -> Dict[str, Any]:
        """Simulate getting account information."""
        return {
            'username': 'demo_news_account',
            'follower_count': 1234,
            'following_count': 567,
            'post_count': 89,
            'bio': 'Demo News Instagram Account (Simulation Mode)',
            'is_demo': True
        }
    
    def is_available(self) -> bool:
        """Check if the demo publisher is available."""
        return True
