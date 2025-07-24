#!/usr/bin/env python3
"""
Extract Instagram session data for GitHub Secrets
This script reads the local session file and outputs the JSON content
that should be copied to GitHub repository secrets.
"""

import json
from pathlib import Path

def extract_session_data():
    """Extract session data from local file for GitHub Secrets."""
    
    session_file = Path("instagram_session.json")
    
    if not session_file.exists():
        print("❌ instagram_session.json not found!")
        print("💡 Make sure you're in the project root directory")
        return None
    
    try:
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        
        # Compact JSON for GitHub Secrets (no extra whitespace)
        compact_json = json.dumps(session_data, separators=(',', ':'))
        
        print("✅ Session data extracted successfully!")
        print("\n" + "="*60)
        print("📋 COPY THIS TO GITHUB SECRETS:")
        print("="*60)
        print("Secret Name: INSTAGRAM_SESSION_DATA")
        print("Secret Value:")
        print(compact_json)
        print("="*60)
        print("\n📝 Instructions:")
        print("1. Go to your GitHub repository: https://github.com/zegh6389/news-instagram-mcp")
        print("2. Click Settings > Secrets and variables > Actions")
        print("3. Click 'New repository secret'")
        print("4. Name: INSTAGRAM_SESSION_DATA")
        print("5. Value: Copy the JSON above")
        print("6. Click 'Add secret'")
        print("\n🔒 After adding the secret, the session file will be removed from the repository")
        print("   for better security - it will be recreated from secrets during GitHub Actions")
        
        return compact_json
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in session file: {e}")
        return None
    except Exception as e:
        print(f"❌ Error reading session file: {e}")
        return None

if __name__ == "__main__":
    print("🔐 Instagram Session Data Extractor for GitHub Secrets")
    print("="*60)
    
    session_data = extract_session_data()
    
    if session_data:
        print(f"\n✨ Session data is {len(session_data)} characters long")
        print("🎯 Ready to add to GitHub repository secrets!")
    else:
        print("\n❌ Failed to extract session data")
        exit(1)
