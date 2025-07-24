#!/usr/bin/env python3
"""
Debug GitHub Actions Environment
Check if credentials are properly configured in GitHub Actions
"""

import os
import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def check_environment():
    """Check GitHub Actions environment variables"""
    print("🔍 GITHUB ACTIONS ENVIRONMENT DEBUG")
    print("=" * 50)
    
    # Check environment variables
    required_vars = ['INSTAGRAM_USERNAME', 'INSTAGRAM_PASSWORD', 'GEMINI_API_KEY']
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            if var == 'INSTAGRAM_PASSWORD':
                print(f"✅ {var}: {'*' * len(value)} (configured)")
            elif var == 'GEMINI_API_KEY':
                print(f"✅ {var}: {value[:10]}... (configured)")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: NOT SET")
    
    print("\n🧪 TESTING INSTAGRAM CONNECTION...")
    
    try:
        from src.config import config
        print(f"Config username: {config.instagram_username}")
        print(f"Config password configured: {bool(config.instagram_password)}")
        
        from src.publishers.instagram_publisher import InstagramPublisher
        publisher = InstagramPublisher()
        
        if hasattr(publisher, 'client') and publisher.client:
            print("✅ Real Instagram client connected")
            client_type = type(publisher.client).__name__
            print(f"Client type: {client_type}")
        else:
            print("❌ No Instagram client available")
            
        # Check if it's actually the demo publisher
        publisher_type = type(publisher).__name__
        print(f"Publisher type: {publisher_type}")
        
    except Exception as e:
        print(f"❌ Error testing Instagram connection: {e}")
    
    print("\n📊 SUMMARY:")
    username = os.environ.get('INSTAGRAM_USERNAME')
    password = os.environ.get('INSTAGRAM_PASSWORD')
    
    if username and password:
        print(f"✅ Credentials configured for: {username}")
        print("✅ Ready for real Instagram posting")
    else:
        print("❌ Missing credentials - will use demo mode")

if __name__ == "__main__":
    check_environment()
