#!/usr/bin/env python3
"""
Setup Instagram Session with Cookies and Session ID
This script creates a proper Instagram session file using your provided cookies and session data.
"""

import json
import sys
import os
import logging
from pathlib import Path
from urllib.parse import unquote

# Add src directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_session_setup.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def create_instagram_session_file():
    """Create Instagram session file with provided cookies and session data."""
    logger.info("🔧 Creating Instagram session file with provided cookies...")
    
    # Your provided session ID (URL decoded)
    session_id_encoded = "76353320465%3AflQBy2nQ3HzMX7%3A25%3AAYcPwSgfCVUmS7ksTjlJuxI-FsA-jQHHAs3v4G9NmA"
    session_id = unquote(session_id_encoded)  # Decode URL encoding
    
    # Your provided cookies data
    cookies = {
        "ig_nrcb": "1",
        "datr": "upVtaOEiMXyiIf9EEUfBs25L",
        "ig_did": "46D26CE5-828F-48D2-BB79-9AA76381F1C8",
        "mid": "aG2VuwALAAFKweQs-Plo88IzfsWM",
        "ps_l": "1",
        "ps_n": "1",
        "dpr": "1.25",
        "ds_user_id": "76353320465",
        "csrftoken": "Z11qMc6D3SFDLTkvbVeKu7jylHEsd9Dj",
        "sessionid": session_id,
        "wd": "1536x730",
        "rur": '"CCO\\05476353320465\\0541784930560:01fe9f4a53d27abee94cbe1cdf3a9a622c2bc950087b67c6034ddd5f1ee8d0010cd64ac8"',
        "_dd_s": ""
    }
    
    # Create session data structure compatible with instagrapi
    session_data = {
        "user_id": "76353320465",
        "uuid": "46D26CE5-828F-48D2-BB79-9AA76381F1C8",
        "mid": "aG2VuwALAAFKweQs-Plo88IzfsWM",
        "ig_u_rur": "CCO\\05476353320465\\0541784930560:01fe9f4a53d27abee94cbe1cdf3a9a622c2bc950087b67c6034ddd5f1ee8d0010cd64ac8",
        "ig_www_claim": "0",
        "authorization_data": {
            "sessionid": session_id,
            "csrftoken": "Z11qMc6D3SFDLTkvbVeKu7jylHEsd9Dj",
            "ds_user_id": "76353320465"
        },
        "cookies": cookies,
        "last_login": {
            "sessionid": session_id,
            "csrftoken": "Z11qMc6D3SFDLTkvbVeKu7jylHEsd9Dj"
        },
        "device_settings": {
            "app_version": "85.0.0.21.100",
            "android_version": 24,
            "android_release": "7.0",
            "dpi": "640dpi",
            "resolution": "1440x2560",
            "manufacturer": "samsung",
            "device": "SM-G930F",
            "model": "herolte",
            "cpu": "samsungexynos8890",
            "version_code": "314665256"
        },
        "user_agent": "Instagram 85.0.0.21.100 Android (24/7.0; 640dpi; 1440x2560; samsung; SM-G930F; herolte; samsungexynos8890; en_US)",
        "country": "US",
        "country_code": 1,
        "locale": "en_US",
        "timezone_offset": -18000
    }
    
    # Save session file
    session_file = config.instagram_session_file
    try:
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        logger.info(f"✅ Instagram session file created successfully: {session_file}")
        logger.info(f"📱 Session configured for user ID: {session_data['user_id']}")
        logger.info(f"🔑 Session ID: {session_id[:20]}...")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to create session file: {e}")
        return False

def test_session_file():
    """Test if the created session file works."""
    logger.info("🧪 Testing Instagram session file...")
    
    try:
        from instagrapi import Client
        
        client = Client()
        
        # Load the session file we just created
        session_file = config.instagram_session_file
        if not Path(session_file).exists():
            logger.error(f"❌ Session file not found: {session_file}")
            return False
        
        logger.info(f"📂 Loading session from: {session_file}")
        client.load_settings(session_file)
        
        # Try to get account info to test if session works
        logger.info("🔄 Testing session by getting account info...")
        account_info = client.account_info()
        
        logger.info("✅ Session test successful!")
        logger.info(f"📱 Connected to: {account_info.full_name} (@{account_info.username})")
        logger.info(f"👥 Followers: {account_info.follower_count}")
        logger.info(f"📝 Following: {account_info.following_count}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Session test failed: {e}")
        logger.warning("💡 This might be normal - session may need to be refreshed during first use")
        return False

def main():
    """Main function."""
    logger.info("🎯 Instagram Session Setup Starting...")
    logger.info("=" * 50)
    
    # Create session file
    session_created = create_instagram_session_file()
    
    if session_created:
        logger.info("📋 Session file created successfully!")
        
        # Test the session
        test_result = test_session_file()
        
        if test_result:
            logger.info("🎉 Session setup completed successfully!")
            logger.info("💡 You can now run your automation scripts")
        else:
            logger.warning("⚠️  Session file created but test failed")
            logger.info("💡 This is often normal - the session will be validated during first use")
            logger.info("💡 Try running your automation script now")
        
        logger.info("\n📋 Next Steps:")
        logger.info("1. Run: python deploy/manual_automation.py")
        logger.info("2. Or run: python main.py")
        logger.info("3. Check logs for 'Real Instagram client connected'")
        
        return 0
    else:
        logger.error("❌ Failed to create session file")
        return 1

if __name__ == "__main__":
    exit(main())
