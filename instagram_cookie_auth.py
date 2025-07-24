#!/usr/bin/env python3
"""
Enhanced Instagram Cookie Authentication
This script provides direct cookie injection to bypass Instagram authentication challenges.
"""

import json
import sys
import os
import logging
from pathlib import Path
from urllib.parse import unquote
from typing import Dict, Any, Optional

# Add src directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_cookie_auth.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class InstagramCookieAuthenticator:
    """Handles Instagram authentication using provided cookies and session data."""
    
    def __init__(self):
        self.session_id_encoded = "76353320465%3AflQBy2nQ3HzMX7%3A25%3AAYcPwSgfCVUmS7ksTjlJuxI-FsA-jQHHAs3v4G9NmA"
        self.session_id = unquote(self.session_id_encoded)
        self.user_id = "76353320465"
        
        # Your provided cookies
        self.cookies = {
            "ig_nrcb": "1",
            "datr": "upVtaOEiMXyiIf9EEUfBs25L", 
            "ig_did": "46D26CE5-828F-48D2-BB79-9AA76381F1C8",
            "mid": "aG2VuwALAAFKweQs-Plo88IzfsWM",
            "ps_l": "1",
            "ps_n": "1",
            "dpr": "1.25",
            "ds_user_id": self.user_id,
            "csrftoken": "Z11qMc6D3SFDLTkvbVeKu7jylHEsd9Dj",
            "sessionid": self.session_id,
            "wd": "1536x730",
            "rur": '"CCO\\05476353320465\\0541784930560:01fe9f4a53d27abee94cbe1cdf3a9a622c2bc950087b67c6034ddd5f1ee8d0010cd64ac8"',
            "_dd_s": ""
        }
    
    def create_comprehensive_session_data(self) -> Dict[str, Any]:
        """Create comprehensive session data compatible with instagrapi."""
        session_data = {
            # Core authentication data
            "user_id": self.user_id,
            "uuid": self.cookies["ig_did"],
            "mid": self.cookies["mid"],
            "ig_u_rur": self.cookies["rur"].strip('"'),
            "ig_www_claim": "0",
            
            # Session tokens
            "sessionid": self.session_id,
            "csrftoken": self.cookies["csrftoken"],
            "ds_user_id": self.user_id,
            
            # Authorization data for API calls
            "authorization_data": {
                "sessionid": self.session_id,
                "csrftoken": self.cookies["csrftoken"],
                "ds_user_id": self.user_id,
                "mid": self.cookies["mid"],
                "ig_did": self.cookies["ig_did"]
            },
            
            # All cookies
            "cookies": self.cookies,
            
            # Last successful login data
            "last_login": {
                "sessionid": self.session_id,
                "csrftoken": self.cookies["csrftoken"],
                "ds_user_id": self.user_id,
                "mid": self.cookies["mid"]
            },
            
            # Device settings that match your session
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
            
            # User agent that matches your session
            "user_agent": "Instagram 85.0.0.21.100 Android (24/7.0; 640dpi; 1440x2560; samsung; SM-G930F; herolte; samsungexynos8890; en_US)",
            
            # Location and settings
            "country": "US",
            "country_code": 1,
            "locale": "en_US",
            "timezone_offset": -18000,
            
            # Additional Instagram API settings
            "phone_id": self.cookies["ig_did"],
            "device_id": "android-" + self.cookies["ig_did"].replace("-", "").lower()[:16],
            "family_device_id": self.cookies["ig_did"],
            "session_flush_enabled": False,
            
            # Request headers
            "request_headers": {
                "User-Agent": "Instagram 85.0.0.21.100 Android (24/7.0; 640dpi; 1440x2560; samsung; SM-G930F; herolte; samsungexynos8890; en_US)",
                "X-IG-App-Locale": "en_US",
                "X-IG-Device-Locale": "en_US",
                "X-IG-Mapped-Locale": "en_US",
                "X-Pigeon-Session-Id": self.cookies["ig_did"],
                "X-Pigeon-Rawclienttime": "1642694400.000",
                "X-IG-Bandwidth-Speed-KBPS": "-1.000",
                "X-IG-Bandwidth-TotalBytes-B": "0",
                "X-IG-Bandwidth-TotalTime-MS": "0",
                "X-IG-App-Startup-Country": "US",
                "X-Bloks-Version-Id": "5f56efad68e1edec7801f630b5c122704ec5378adbee6609a448f105f34a9c73",
                "X-IG-WWW-Claim": "0",
                "X-Bloks-Is-Layout-RTL": "false",
                "X-Bloks-Is-Panorama-Enabled": "true",
                "X-IG-Device-ID": self.cookies["ig_did"],
                "X-IG-Family-Device-ID": self.cookies["ig_did"],
                "X-IG-Android-ID": "android-" + self.cookies["ig_did"].replace("-", "").lower()[:16],
                "X-IG-Timezone-Offset": "-18000",
                "X-IG-Connection-Type": "WIFI",
                "X-IG-Capabilities": "3brTvwM=",
                "X-IG-App-ID": "567067343352427",
                "Priority": "u=3",
                "User-Agent": "Instagram 85.0.0.21.100 Android (24/7.0; 640dpi; 1440x2560; samsung; SM-G930F; herolte; samsungexynos8890; en_US)",
                "Accept-Language": "en-US",
                "X-MID": self.cookies["mid"],
                "X-CSRFToken": self.cookies["csrftoken"],
                "Authorization": f"Bearer IGT:2:{self.session_id}",
                "X-Instagram-AJAX": "1007616227",
                "X-Requested-With": "XMLHttpRequest",
                "X-ASBD-ID": "198387",
                "X-IG-Connection-Speed": "-1kbps",
                "X-IG-Bandwidth-Speed-KBPS": "-1.000",
                "Accept": "*/*"
            }
        }
        
        return session_data
    
    def setup_session_file(self) -> bool:
        """Create the Instagram session file with comprehensive data."""
        logger.info("🔧 Setting up Instagram session with provided cookies...")
        
        try:
            session_data = self.create_comprehensive_session_data()
            session_file = config.instagram_session_file
            
            # Create directory if it doesn't exist
            session_path = Path(session_file)
            session_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save session data
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            logger.info(f"✅ Session file created: {session_file}")
            logger.info(f"📱 User ID: {self.user_id}")
            logger.info(f"🔑 Session ID: {self.session_id[:20]}...")
            logger.info(f"🍪 Cookies: {len(self.cookies)} items")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create session file: {e}")
            return False
    
    def test_session(self) -> bool:
        """Test the created session with Instagram API."""
        logger.info("🧪 Testing Instagram session...")
        
        try:
            from instagrapi import Client
            
            client = Client()
            
            # Load our session
            session_file = config.instagram_session_file
            if not Path(session_file).exists():
                logger.error("❌ Session file not found")
                return False
            
            logger.info(f"📂 Loading session from: {session_file}")
            client.load_settings(session_file)
            
            # Set device consistency
            client.set_device(self.cookies["ig_did"])
            client.set_user_agent("Instagram 85.0.0.21.100 Android (24/7.0; 640dpi; 1440x2560; samsung; SM-G930F; herolte; samsungexynos8890; en_US)")
            
            # Test basic API call
            logger.info("🔄 Testing account info retrieval...")
            account_info = client.account_info()
            
            logger.info("✅ Session test successful!")
            logger.info(f"📱 Account: {account_info.full_name} (@{account_info.username})")
            logger.info(f"👥 Followers: {account_info.follower_count}")
            logger.info(f"📝 Following: {account_info.following_count}")
            logger.info(f"📊 Posts: {account_info.media_count}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Session test failed: {e}")
            
            # Provide specific guidance based on error
            if "login_required" in str(e).lower():
                logger.warning("💡 Session may have expired - this is normal for old sessions")
            elif "challenge" in str(e).lower():
                logger.warning("💡 Instagram challenge detected - session may need refresh")
            elif "rate" in str(e).lower():
                logger.warning("💡 Rate limiting detected - wait a few minutes")
            else:
                logger.warning("💡 Unknown error - session may still work during normal operation")
            
            return False

def main():
    """Main function to setup Instagram session with cookies."""
    logger.info("🍪 Instagram Cookie Authentication Setup")
    logger.info("=" * 50)
    
    authenticator = InstagramCookieAuthenticator()
    
    # Setup session file
    logger.info("📋 Step 1: Creating session file...")
    session_setup = authenticator.setup_session_file()
    
    if not session_setup:
        logger.error("❌ Failed to setup session file")
        return 1
    
    # Test session
    logger.info("\n📋 Step 2: Testing session...")
    test_result = authenticator.test_session()
    
    if test_result:
        logger.info("\n🎉 Cookie authentication setup completed successfully!")
        logger.info("✅ Your Instagram session is ready to use")
    else:
        logger.warning("\n⚠️  Session file created but test failed")
        logger.info("💡 This is often normal - the session will be validated during actual use")
    
    logger.info("\n📋 Next Steps:")
    logger.info("1. Run your automation: python deploy/manual_automation.py")
    logger.info("2. Or test with: python main.py")
    logger.info("3. Look for 'Real Instagram client connected' in logs")
    logger.info("4. If you still get errors, run: python interactive_instagram_auth.py")
    
    return 0

if __name__ == "__main__":
    exit(main())
