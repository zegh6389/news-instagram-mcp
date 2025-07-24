#!/usr/bin/env python3
"""
Quick API checker - shows what you have and what you need for first post.
This won't get stuck on network calls.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def check_environment_file():
    """Check if .env file exists and what's in it."""
    print("🔍 Checking Environment Setup...")
    
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found!")
        print("\n📝 You need to create .env file:")
        print("1. Copy: cp .env.example .env")
        print("2. Edit .env with your credentials")
        return False
    
    print("✅ .env file exists")
    return True

def check_required_apis():
    """Check what APIs you have configured."""
    print("\n🔑 Checking API Credentials...")
    
    # Load environment without causing errors
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        print("❌ Could not load .env file")
        return False
    
    # Check Instagram (REQUIRED)
    instagram_username = os.getenv('INSTAGRAM_USERNAME')
    instagram_password = os.getenv('INSTAGRAM_PASSWORD')
    
    print("\n📱 Instagram API (REQUIRED for posting):")
    if instagram_username and instagram_password:
        print(f"✅ Username: {instagram_username}")
        print("✅ Password: *** (configured)")
        instagram_ok = True
    else:
        print("❌ Instagram credentials missing!")
        print("   Add to .env: INSTAGRAM_USERNAME=your_username")
        print("   Add to .env: INSTAGRAM_PASSWORD=your_password")
        instagram_ok = False
    
    # Check AI APIs (OPTIONAL)
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    print("\n🧠 AI APIs (Optional - for smart content processing):")
    if openai_key:
        print(f"✅ OpenAI API: {openai_key[:8]}...")
        ai_ok = True
    elif anthropic_key:
        print(f"✅ Anthropic API: {anthropic_key[:8]}...")
        ai_ok = True
    else:
        print("⚠️  No AI API keys found")
        print("   For better content: Add OPENAI_API_KEY=sk-your-key")
        print("   Or: Add ANTHROPIC_API_KEY=your-key")
        ai_ok = False
    
    return instagram_ok, ai_ok

def check_dependencies():
    """Check if required Python packages are installed."""
    print("\n📦 Checking Dependencies...")
    
    required_packages = [
        ('requests', 'Web scraping'),
        ('beautifulsoup4', 'HTML parsing'),
        ('feedparser', 'RSS parsing'),
        ('sqlalchemy', 'Database'),
        ('pydantic', 'Data validation'),
        ('pillow', 'Image processing'),
        ('instagrapi', 'Instagram API'),
        ('mcp', 'MCP Protocol'),
        ('newspaper3k', 'News extraction'),
        ('python-dotenv', 'Environment variables')
    ]
    
    missing = []
    
    for package, description in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} - {description}")
        except ImportError:
            print(f"❌ {package} - {description}")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    
    print("✅ All dependencies installed!")
    return True

def check_instagram_account_type():
    """Provide guidance on Instagram account requirements."""
    print("\n📋 Instagram Account Requirements:")
    print("✅ Must be Business or Creator account (not personal)")
    print("✅ Must have username/password (not just tokens)")
    print("⚠️  2FA might need to be disabled temporarily")
    print("⚠️  Account must not be restricted/banned")
    
    print("\nTo convert to Business account:")
    print("1. Go to Instagram Settings > Account")
    print("2. Switch to Professional Account")
    print("3. Choose Business or Creator")

def show_what_you_need():
    """Show clear summary of what's needed."""
    print("\n" + "="*60)
    print("🎯 WHAT YOU NEED FOR YOUR FIRST POST")
    print("="*60)
    
    print("\n🚨 REQUIRED (System won't work without these):")
    print("1. Instagram Business/Creator account")
    print("2. Instagram username and password")
    print("3. .env file with credentials")
    
    print("\n⭐ RECOMMENDED (for better results):")
    print("4. OpenAI API key ($5-20/month)")
    print("   - Get from: https://platform.openai.com/api-keys")
    print("   - Needed for: Smart captions, content analysis")
    
    print("\n✅ OPTIONAL (system has defaults):")
    print("5. Custom news sources")
    print("6. Custom visual templates")
    print("7. Custom posting schedules")

def create_sample_env():
    """Create a sample .env file if none exists."""
    env_file = Path('.env')
    if not env_file.exists():
        print("\n📝 Creating sample .env file...")
        
        sample_content = """# Instagram API (REQUIRED)
INSTAGRAM_USERNAME=your_instagram_username_here
INSTAGRAM_PASSWORD=your_instagram_password_here

# OpenAI API (OPTIONAL - for smart features)
OPENAI_API_KEY=sk-your-openai-key-here

# System defaults (can keep as-is)
DATABASE_URL=sqlite:///news_instagram.db
LOG_LEVEL=DEBUG
MAX_POSTS_PER_DAY=1
REQUEST_DELAY=2
"""
        
        with open('.env', 'w') as f:
            f.write(sample_content)
        
        print("✅ Created .env file with template")
        print("📝 Edit .env file and add your actual credentials")
        return True
    
    return False

def main():
    """Check everything and provide clear guidance."""
    print("🔍 News Instagram MCP - API & Requirements Check")
    print("="*60)
    
    # Check basic setup
    env_exists = check_environment_file()
    
    if not env_exists:
        create_sample_env()
        print("\n❌ Setup .env file first, then run this script again")
        return
    
    # Check APIs
    instagram_ok, ai_ok = check_required_apis()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Show account guidance
    check_instagram_account_type()
    
    # Show summary
    show_what_you_need()
    
    print("\n" + "="*60)
    print("📊 STATUS SUMMARY")
    print("="*60)
    
    print(f"{'✅' if instagram_ok else '❌'} Instagram credentials")
    print(f"{'✅' if ai_ok else '⚠️ '} AI API (optional)")
    print(f"{'✅' if deps_ok else '❌'} Dependencies")
    
    if instagram_ok and deps_ok:
        print("\n🎉 READY! You can create your first post!")
        print("\nNext steps:")
        print("1. Ensure Instagram account is Business/Creator type")
        print("2. Run: python main.py")
        print("3. Use MCP tools or manual scripts")
        
        if not ai_ok:
            print("\n💡 For better results, add OpenAI API key to .env")
    else:
        print("\n🔧 SETUP NEEDED:")
        if not instagram_ok:
            print("- Add Instagram credentials to .env file")
        if not deps_ok:
            print("- Install missing Python packages")
        
        print("\nThen run this script again to verify!")

if __name__ == "__main__":
    main()
