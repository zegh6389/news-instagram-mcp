#!/usr/bin/env python3
"""
Interactive Instagram Authentication Script
Handles Instagram challenges including email verification codes.
"""

import sys
import os
import logging
from pathlib import Path
import getpass

# Add src directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from config import config
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def interactive_instagram_login():
    """Interactive Instagram login with challenge handling."""
    logger.info("🔐 Starting interactive Instagram authentication...")
    
    # Load credentials
    username = config.instagram_username
    password = config.instagram_password
    
    if not username or not password:
        logger.error("❌ Instagram credentials not configured")
        return False
    
    logger.info(f"👤 Username: {username}")
    
    # Initialize Instagram client
    client = Client()
    
    try:
        logger.info("🔄 Attempting Instagram login...")
        client.login(username, password)
        logger.info("✅ Login successful!")
        
        # Test account access
        user_info = client.account_info()
        logger.info(f"📱 Connected to: {user_info.full_name} (@{user_info.username})")
        logger.info(f"👥 Followers: {user_info.follower_count}")
        
        # Save session for future use
        session_file = "instagram_session.json"
        client.dump_settings(session_file)
        logger.info(f"💾 Session saved to {session_file}")
        
        return True
        
    except ChallengeRequired as e:
        logger.warning("🔔 Instagram challenge required")
        logger.info("Challenge details:")
        logger.info(f"  Challenge URL: {e.challenge_url}")
        logger.info(f"  Available methods: {e.challenge_choice}")
        
        # Handle email challenge
        if 'email' in str(e.challenge_choice).lower():
            logger.info("📧 Email verification challenge detected")
            logger.info("Please check your email for a 6-digit verification code")
            
            # Get verification code from user
            verification_code = input("Enter the 6-digit verification code from your email: ").strip()
            
            if len(verification_code) == 6 and verification_code.isdigit():
                try:
                    logger.info("🔑 Submitting verification code...")
                    client.challenge_code_handler(verification_code)
                    logger.info("✅ Challenge completed successfully!")
                    
                    # Test account access
                    user_info = client.account_info()
                    logger.info(f"📱 Connected to: {user_info.full_name} (@{user_info.username})")
                    
                    # Save session
                    session_file = "instagram_session.json"
                    client.dump_settings(session_file)
                    logger.info(f"💾 Session saved to {session_file}")
                    
                    return True
                    
                except Exception as challenge_error:
                    logger.error(f"❌ Challenge verification failed: {challenge_error}")
                    return False
            else:
                logger.error("❌ Invalid verification code format")
                return False
        else:
            logger.error(f"❌ Unsupported challenge type: {e.challenge_choice}")
            return False
            
    except LoginRequired as e:
        logger.error(f"❌ Login required: {e}")
        return False
        
    except Exception as e:
        logger.error(f"❌ Authentication error: {e}")
        return False

def main():
    """Main function."""
    print("🎯 Interactive Instagram Authentication")
    print("=" * 50)
    
    success = interactive_instagram_login()
    
    if success:
        print("\n🎉 Authentication completed successfully!")
        print("💡 You can now run the automation scripts")
        print("\nNext steps:")
        print("1. Run: python deploy/manual_automation.py")
        print("2. Or test with GitHub Actions")
    else:
        print("\n❌ Authentication failed")
        print("💡 Please check:")
        print("1. Your email for Instagram verification codes")
        print("2. Instagram account isn't restricted")
        print("3. Credentials are correct")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
