#!/usr/bin/env python3
"""
Canadian Instagram Authentication Script
Special authentication script designed for Milton, Ontario, Canada location
This helps establish a trusted session from your Canadian location.
"""

import sys
import os
import logging
from pathlib import Path
import getpass
import time

# Add src directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from config import config
from auth import InstagramAuthManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def canadian_instagram_setup():
    """Setup Instagram authentication from Milton, Canada."""
    print("🍁 Canadian Instagram Authentication Setup")
    print("=" * 50)
    print(f"📍 Location: Milton, Ontario, Canada")
    print(f"🕐 Time Zone: America/Toronto")
    print()
    
    # Load credentials
    username = config.instagram_username
    password = config.instagram_password
    
    if not username or not password:
        print("❌ Instagram credentials not found in environment variables")
        print()
        print("Please set the following environment variables:")
        print("  INSTAGRAM_USERNAME=your_username")
        print("  INSTAGRAM_PASSWORD=your_password")
        print()
        print("Or create a .env file with these variables")
        return False
    
    print(f"👤 Username: {username}")
    print()
    
    # Initialize Canadian auth manager
    print("🔧 Initializing Canadian Instagram authentication...")
    auth_manager = InstagramAuthManager(
        username=username,
        password=password,
        session_dir="sessions"
    )
    
    print("📱 Device Profile: Samsung Galaxy S21 (Canadian model SM-G991W)")
    print("🌐 Locale: en_CA (English - Canada)")
    print("🕐 Timezone: America/Toronto")
    print()
    
    # Attempt authentication
    print("🔐 Attempting Instagram authentication from Canada...")
    print("⏳ This may take a moment...")
    print()
    
    success = auth_manager.authenticate()
    
    if success:
        print("🎉 SUCCESS! Instagram authentication completed")
        print("✅ Canadian session established successfully")
        print()
        
        # Verify account details
        client = auth_manager.get_client()
        if client:
            try:
                account_info = client.account_info()
                print("📊 Account Details:")
                print(f"   Name: {account_info.full_name}")
                print(f"   Username: @{account_info.username}")
                print(f"   Followers: {account_info.follower_count:,}")
                print(f"   Following: {account_info.following_count:,}")
                print(f"   Posts: {account_info.media_count:,}")
                print()
            except Exception as e:
                logger.warning(f"Could not fetch account details: {e}")
        
        print("💾 Session saved for future use")
        print("🔄 Your automation scripts can now use this authenticated session")
        print()
        print("🚀 Next Steps:")
        print("1. Test posting with: python deploy/manual_automation.py")
        print("2. Set up GitHub Actions for automated posting")
        print("3. Monitor the logs for any additional authentication challenges")
        
        return True
    else:
        print("❌ FAILED: Instagram authentication unsuccessful")
        print()
        print("🔍 Troubleshooting Steps:")
        print()
        print("1. 📧 Check Email for Security Alerts")
        print("   - Instagram may have sent a security notification")
        print("   - Look for emails about 'suspicious login attempts'")
        print("   - Click 'This was me' if you see such emails")
        print()
        print("2. 🌐 Manual Login Required")
        print("   - Open Instagram in your web browser")
        print("   - Log in manually from this same device/location")
        print("   - Complete any security challenges or verifications")
        print("   - This establishes trust for this location")
        print()
        print("3. 📱 App Login (Recommended)")
        print("   - Install Instagram mobile app on this device")
        print("   - Log in through the mobile app")
        print("   - This helps Instagram recognize this as a trusted device")
        print()
        print("4. ⏰ Wait and Retry")
        print("   - If blocked, wait 24 hours before retrying")
        print("   - Instagram's security systems need time to reset")
        print()
        print("5. 🔐 Account Security Check")
        print("   - Ensure your account isn't restricted or suspended")
        print("   - Check if two-factor authentication is enabled")
        print("   - Verify account email and phone number")
        
        return False

def test_existing_session():
    """Test if there's already a valid Canadian session."""
    print("🔍 Checking for existing Canadian Instagram session...")
    
    username = config.instagram_username
    if not username:
        print("❌ No username configured")
        return False
    
    auth_manager = InstagramAuthManager(
        username=username,
        password=config.instagram_password or "",
        session_dir="sessions"
    )
    
    if auth_manager.is_authenticated():
        client = auth_manager.get_client()
        if client:
            try:
                account_info = client.account_info()
                print(f"✅ Valid session found for @{account_info.username}")
                print(f"🍁 Location context: Milton, Ontario, Canada")
                return True
            except Exception as e:
                print(f"❌ Session validation failed: {e}")
    
    print("❌ No valid session found")
    return False

def main():
    """Main function."""
    print("🍁🔐 Canadian Instagram Authentication Manager")
    print("=" * 60)
    print()
    
    # Check for existing session first
    if test_existing_session():
        print()
        print("🎉 You're already authenticated!")
        print("💡 Your Instagram automation is ready to use")
        return 0
    
    print()
    
    # Perform fresh authentication
    success = canadian_instagram_setup()
    
    if success:
        print()
        print("🎊 AUTHENTICATION COMPLETE!")
        print("🇨🇦 Your Instagram account is now authenticated from Milton, Canada")
        print("🤖 Automation scripts can now post without location blocks")
        return 0
    else:
        print()
        print("💔 Authentication failed - please follow troubleshooting steps above")
        return 1

if __name__ == "__main__":
    exit(main())
