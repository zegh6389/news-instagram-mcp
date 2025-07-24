#!/usr/bin/env python3
"""Test Instagram connection and session validity."""

import logging
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from config import config
from publishers.instagram_publisher import InstagramPublisher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_instagram_connection():
    """Test Instagram connection and session validity."""
    logger.info("🔍 Testing Instagram connection...")
    
    # Initialize publisher
    publisher = InstagramPublisher()
    
    if not publisher.client:
        logger.error("❌ Instagram client not initialized")
        return False
    
    try:
        # Test connection
        if publisher.connect():
            logger.info("✅ Instagram connection successful")
            
            # Get account info
            account_info = publisher.client.account_info()
            logger.info(f"📱 Connected as: @{account_info.username}")
            logger.info(f"👥 Followers: {account_info.follower_count}")
            logger.info(f"📝 Posts: {account_info.media_count}")
            
            # Test uploading a simple text story (less likely to fail)
            try:
                # Just test if we can access user info without actually posting
                user_id = publisher.client.user_id
                logger.info(f"🆔 User ID: {user_id}")
                logger.info("✅ Session is valid and ready for posting")
                return True
                
            except Exception as e:
                logger.error(f"❌ Session test failed: {e}")
                return False
                
        else:
            logger.error("❌ Failed to connect to Instagram")
            return False
            
    except Exception as e:
        logger.error(f"❌ Instagram connection error: {e}")
        return False

if __name__ == "__main__":
    success = test_instagram_connection()
    sys.exit(0 if success else 1)
