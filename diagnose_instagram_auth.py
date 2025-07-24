#!/usr/bin/env python3
"""
Instagram Authentication Diagnostic Tool
Helps diagnose Instagram authentication issues and provides specific guidance
"""

import os
import sys
import json
from datetime import datetime

# Add src to path
sys.path.append('src')

def main():
    print("🔍 Instagram Authentication Diagnostic Tool")
    print("=" * 50)
    
    # Check if credentials are available
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')
    
    if not username or not password:
        print("❌ Instagram credentials not found in environment variables")
        print("💡 Set them with:")
        print("   $env:INSTAGRAM_USERNAME='your_username'")
        print("   $env:INSTAGRAM_PASSWORD='your_password'")
        return
    
    print(f"✅ Found credentials for: {username}")
    print(f"🌍 Target location: Milton, Ontario, Canada")
    print()
    
    try:
        from auth.instagram_auth_manager import InstagramAuthManager
        
        # Create auth manager
        auth_manager = InstagramAuthManager(username, password)
        
        # Get detailed status
        status = auth_manager.get_auth_status()
        
        print("📊 AUTHENTICATION STATUS")
        print("-" * 30)
        print(f"🔐 Authenticated: {'✅' if status['authenticated'] else '❌'}")
        print(f"💾 Session exists: {'✅' if status['session_exists'] else '❌'}")
        print(f"📱 Device profile: {'✅' if status['device_profile_exists'] else '❌'}")
        print(f"📍 Location: {status['location']}")
        
        if 'session_age_days' in status:
            print(f"⏰ Session age: {status['session_age_days']} days")
            if status.get('session_expired'):
                print("⚠️  Session expired (>30 days)")
        
        if 'error' in status:
            print(f"❌ Error: {status['error']}")
        
        print()
        
        if status['recommendations']:
            print("💡 RECOMMENDATIONS")
            print("-" * 20)
            for rec in status['recommendations']:
                print(f"   {rec}")
        else:
            print("✅ No specific recommendations - try authentication test")
        
        print()
        print("🧪 TESTING AUTHENTICATION...")
        print("-" * 30)
        
        # Test authentication
        if auth_manager.authenticate():
            print("✅ Authentication successful!")
            
            # Get account info
            client = auth_manager.get_client()
            if client:
                try:
                    account_info = client.account_info()
                    print(f"👤 Account: @{account_info.username}")
                    print(f"👥 Followers: {account_info.follower_count:,}")
                    print(f"📝 Following: {account_info.following_count:,}")
                    print("🎉 Ready for automation!")
                except Exception as e:
                    print(f"⚠️  Basic auth works but account info failed: {e}")
            
        else:
            print("❌ Authentication failed!")
            print()
            print("🔧 TROUBLESHOOTING STEPS")
            print("-" * 25)
            print("1. 📱 Open Instagram app on your phone")
            print("2. 🔑 Log in manually with your credentials")
            print("3. ✅ Complete any security prompts or updates")
            print("4. 🌍 Make sure you're in Milton, Ontario, Canada")
            print("5. ⏰ Wait 2-4 hours after manual login")
            print("6. 🔄 Run this diagnostic again")
            print()
            print("📧 If you see 'ForceAppUpgrade' or 'Manual Login' errors:")
            print("   → Instagram requires manual verification on your device")
            print("   → This is normal security behavior")
            print("   → Automation will work after manual login")
    
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Install requirements: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("💡 Check the logs for more details")

if __name__ == "__main__":
    main()
