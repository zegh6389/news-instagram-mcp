#!/usr/bin/env python3
"""
Fix Instagram Authentication Script
Handles re-authentication and challenge verification for Instagram account.
"""

import sys
import os
import logging
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from config import config
from publishers.instagram_publisher import InstagramPublisher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_auth_fix.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def fix_instagram_authentication():
    """Fix Instagram authentication by handling challenges."""
    logger.info("🔧 Starting Instagram authentication fix...")
    
    try:
        # Load credentials
        username = config.instagram_username
        password = config.instagram_password
        
        if not username or not password:
            logger.error("❌ Instagram credentials not configured")
            return False
            
        logger.info(f"🔑 Using Instagram username: {username}")
        
        # Initialize Instagram publisher with fresh session
        publisher = InstagramPublisher()
        
        # Try to connect - this will handle any challenges
        logger.info("🔄 Attempting Instagram connection...")
        result = publisher.connect()
        
        if result:
            logger.info("✅ Instagram authentication successful!")
            
            # Test basic functionality
            logger.info("🧪 Testing Instagram account info...")
            try:
                user_info = publisher.client.account_info()
                logger.info(f"📱 Connected to account: {user_info.full_name} (@{user_info.username})")
                logger.info(f"👥 Followers: {user_info.follower_count}")
                return True
            except Exception as e:
                logger.error(f"❌ Error getting account info: {e}")
                return False
        else:
            logger.error("❌ Instagram authentication failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error during authentication fix: {e}")
        return False

def main():
    """Main function."""
    logger.info("🎯 Instagram Authentication Fix Starting...")
    
    success = fix_instagram_authentication()
    
    if success:
        logger.info("🎉 Instagram authentication fix completed successfully!")
        logger.info("💡 You can now run manual automation again")
    else:
        logger.error("❌ Instagram authentication fix failed")
        logger.error("💡 You may need to:")
        logger.error("   1. Check your email for Instagram verification code")
        logger.error("   2. Verify account credentials")
        logger.error("   3. Check if account is restricted")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
