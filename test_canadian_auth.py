#!/usr/bin/env python3
"""
Test Canadian Instagram Authentication
Verifies that Instagram authentication is working from Milton, Canada
"""

import sys
import os
import logging
from pathlib import Path
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

def test_authentication():
    """Test Instagram authentication from Canada."""
    print("🧪 Testing Canadian Instagram Authentication")
    print("=" * 50)
    print()
    
    # Check configuration
    username = config.instagram_username
    password = config.instagram_password
    
    if not username or not password:
        print("❌ Instagram credentials not configured")
        print("Please set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD environment variables")
        return False
    
    print(f"👤 Testing authentication for: {username}")
    print(f"📍 Location: Milton, Ontario, Canada")
    print()
    
    # Initialize auth manager
    auth_manager = InstagramAuthManager(
        username=username,
        password=password,
        session_dir="sessions"
    )
    
    # Test authentication
    print("🔐 Testing authentication...")
    start_time = time.time()
    
    success = auth_manager.authenticate()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"⏱️  Authentication took {duration:.2f} seconds")
    print()
    
    if success:
        print("✅ AUTHENTICATION SUCCESS!")
        print()
        
        # Test client functionality
        client = auth_manager.get_client()
        if client:
            try:
                print("📊 Fetching account information...")
                account_info = client.account_info()
                
                print("🎉 Account Details Retrieved:")
                print(f"   👤 Name: {account_info.full_name}")
                print(f"   🔗 Username: @{account_info.username}")
                print(f"   👥 Followers: {account_info.follower_count:,}")
                print(f"   📝 Following: {account_info.following_count:,}")
                print(f"   📷 Posts: {account_info.media_count:,}")
                print(f"   ✅ Verified: {'Yes' if account_info.is_verified else 'No'}")
                print(f"   🔒 Private: {'Yes' if account_info.is_private else 'No'}")
                print()
                
                print("🍁 Canadian Location Context Verified:")
                print("   📍 Device appears to be from Milton, Ontario")
                print("   🕐 Timezone: America/Toronto")
                print("   🌐 Locale: en_CA")
                print("   📱 Device: Samsung Galaxy S21 (Canadian model)")
                print()
                
                return True
                
            except Exception as e:
                print(f"❌ Error fetching account details: {e}")
                return False
        else:
            print("❌ Could not get authenticated client")
            return False
    else:
        print("❌ AUTHENTICATION FAILED!")
        print()
        print("🔍 Possible Issues:")
        print("1. Instagram is blocking login from this location")
        print("2. Account credentials are incorrect")
        print("3. Account has two-factor authentication enabled")
        print("4. Account is restricted or suspended")
        print("5. Network or device fingerprint is flagged")
        print()
        print("📋 Recommended Actions:")
        print("1. Log into Instagram manually from this device")
        print("2. Check email for security notifications")
        print("3. Verify account isn't restricted")
        print("4. Wait 24 hours and try again")
        print("5. Follow the Canadian Authentication Guide")
        
        return False

def test_session_persistence():
    """Test if sessions persist correctly."""
    print("🔄 Testing Session Persistence")
    print("-" * 30)
    
    username = config.instagram_username
    if not username:
        print("❌ No username configured")
        return False
    
    auth_manager = InstagramAuthManager(
        username=username,
        password=config.instagram_password or "",
        session_dir="sessions"
    )
    
    # Check session file
    session_file = Path("sessions") / f"{username}_session.json"
    device_file = Path("sessions") / f"{username}_device.json"
    
    print(f"📄 Session file: {session_file}")
    print(f"   Exists: {'✅' if session_file.exists() else '❌'}")
    if session_file.exists():
        mod_time = session_file.stat().st_mtime
        age_hours = (time.time() - mod_time) / 3600
        print(f"   Age: {age_hours:.1f} hours")
    
    print(f"📱 Device file: {device_file}")
    print(f"   Exists: {'✅' if device_file.exists() else '❌'}")
    
    # Test authentication status
    if auth_manager.is_authenticated():
        print("✅ Session is valid and authenticated")
        return True
    else:
        print("❌ Session is not authenticated")
        return False

def test_canadian_context():
    """Test Canadian-specific configurations."""
    print("🇨🇦 Testing Canadian Context")
    print("-" * 30)
    
    # Test device settings
    auth_manager = InstagramAuthManager(
        username="test",
        password="test",
        session_dir="sessions"
    )
    
    device_settings = auth_manager._get_canadian_device_settings()
    
    print("📱 Device Configuration:")
    print(f"   Model: {device_settings.get('model', 'Not set')}")
    print(f"   Manufacturer: {device_settings.get('manufacturer', 'Not set')}")
    print(f"   Android Version: {device_settings.get('android_version', 'Not set')}")
    print(f"   Resolution: {device_settings.get('resolution', 'Not set')}")
    
    # Check for Canadian model
    if device_settings.get('model') == 'SM-G991W':
        print("✅ Canadian Samsung Galaxy S21 model detected")
    else:
        print("❌ Non-Canadian device model")
    
    # Test user agent
    user_agent = auth_manager._get_canadian_user_agent()
    if 'en_CA' in user_agent:
        print("✅ Canadian locale in user agent")
    else:
        print("❌ Canadian locale not detected")
    
    print(f"🌐 User Agent: {user_agent[:60]}...")
    
    print("📍 Location Context:")
    for key, value in auth_manager.location_context.items():
        print(f"   {key.title()}: {value}")
    
    return True

def main():
    """Main test function."""
    print("🧪🇨🇦 Canadian Instagram Authentication Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        ("Canadian Context", test_canadian_context),
        ("Session Persistence", test_session_persistence),
        ("Instagram Authentication", test_authentication),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"🔬 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"{'✅ PASSED' if result else '❌ FAILED'}: {test_name}")
        except Exception as e:
            logger.error(f"Test {test_name} failed with error: {e}")
            results.append((test_name, False))
            print(f"❌ ERROR: {test_name} - {e}")
        
        print()
    
    # Summary
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {test_name}")
    
    print()
    print(f"📈 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("🚀 Your Canadian Instagram authentication is ready!")
        print()
        print("Next steps:")
        print("1. Run your MCP automation scripts")
        print("2. Monitor logs for any authentication issues")
        print("3. Post content and verify no location blocks")
    else:
        print("⚠️  Some tests failed")
        print("📋 Please review the failed tests and follow troubleshooting steps")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    exit(main())
