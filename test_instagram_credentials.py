#!/usr/bin/env python3
"""
Quick test to verify Instagram credentials
Run this to check if your Instagram credentials are working
"""

import os
import sys
from pathlib import Path

# Add src to path
src_path = str(Path(__file__).parent / 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Change to the script directory to ensure relative imports work
os.chdir(Path(__file__).parent)

from config import config

def test_credentials():
    """Test Instagram credentials configuration."""
    print("🔍 Instagram Credentials Test")
    print("=" * 40)
    
    # Check environment variables
    print(f"📧 INSTAGRAM_USERNAME env: {os.getenv('INSTAGRAM_USERNAME', 'Not set')}")
    print(f"🔐 INSTAGRAM_PASSWORD env: {'Set' if os.getenv('INSTAGRAM_PASSWORD') else 'Not set'}")
    print()
    
    # Check config values
    print(f"📧 Config username: {config.instagram_username}")
    print(f"🔐 Config password: {'Set' if config.instagram_password else 'Not set'}")
    print()
    
    # Check for placeholder values
    if config.instagram_username == 'your_instagram_username':
        print("⚠️  WARNING: Username is still placeholder value!")
        print("   You need to update your GitHub secrets with real Instagram credentials")
    elif not config.instagram_username:
        print("❌ ERROR: No Instagram username configured")
    else:
        print("✅ Instagram username looks valid")
    
    if config.instagram_password == 'your_instagram_password':
        print("⚠️  WARNING: Password is still placeholder value!")
        print("   You need to update your GitHub secrets with real Instagram credentials")
    elif not config.instagram_password:
        print("❌ ERROR: No Instagram password configured")
    else:
        print("✅ Instagram password is configured")
    
    print()
    print("🎯 SOLUTION:")
    print("1. Go to: https://github.com/zegh6389/news-instagram-mcp/settings/secrets/actions")
    print("2. Update INSTAGRAM_USERNAME with your real Instagram username")
    print("3. Update INSTAGRAM_PASSWORD with your real Instagram password")
    print("4. Run the manual automation again")

if __name__ == "__main__":
    test_credentials()
