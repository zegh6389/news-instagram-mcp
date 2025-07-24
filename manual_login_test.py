#!/usr/bin/env python3
"""
Manual Instagram Login Helper
Use this after completing manual login on your phone to test automation
"""

import os
import sys
import getpass

# Add src to path
sys.path.append('src')

def main():
    print("🔑 Manual Instagram Login Helper")
    print("=" * 40)
    print("Use this tool AFTER you've manually logged into Instagram on your phone")
    print()
    
    # Get credentials
    username = input("📱 Instagram username: ").strip()
    if not username:
        print("❌ Username required")
        return
    
    password = getpass.getpass("🔒 Instagram password: ")
    if not password:
        print("❌ Password required")
        return
    
    print(f"\n🍁 Testing authentication for @{username} from Milton, Canada...")
    
    try:
        from auth.instagram_auth_manager import InstagramAuthManager
        
        # Create auth manager
        auth_manager = InstagramAuthManager(username, password)
        
        # Test authentication
        print("🔄 Attempting authentication...")
        if auth_manager.authenticate():
            print("✅ SUCCESS! Authentication working!")
            
            # Get account details
            client = auth_manager.get_client()
            if client:
                try:
                    account_info = client.account_info()
                    print(f"👤 Logged in as: @{account_info.username}")
                    print(f"👥 Followers: {account_info.follower_count:,}")
                    print("💾 Session saved for automation")
                    print()
                    print("🎉 Your automation is now ready to work!")
                    print("💡 You can now run the daily automation without issues")
                    
                except Exception as e:
                    print(f"⚠️  Auth works but account info failed: {e}")
                    print("✅ This is usually fine for automation")
        else:
            print("❌ Authentication still failing")
            print()
            print("🔧 Next steps:")
            print("1. 📱 Double-check you manually logged in on Instagram app")
            print("2. ✅ Complete any pending security verifications")
            print("3. 🌍 Ensure you're in Milton, Ontario, Canada")
            print("4. ⏰ Wait 2-4 hours and try again")
            print("5. 📧 Check email for Instagram security alerts")
    
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Run: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
