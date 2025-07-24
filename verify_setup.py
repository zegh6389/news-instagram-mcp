#!/usr/bin/env python3
"""
Quick setup verification for Canadian Instagram MCP
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    try:
        import instagrapi
        print("✅ instagrapi installed")
    except ImportError:
        print("❌ instagrapi not installed - run: pip install instagrapi")
        return False
    
    try:
        import requests
        print("✅ requests installed")
    except ImportError:
        print("❌ requests not installed")
        return False
    
    return True

def check_environment():
    """Check environment variables."""
    print("\n🔍 Checking environment variables...")
    
    required_vars = [
        'INSTAGRAM_USERNAME',
        'INSTAGRAM_PASSWORD'
    ]
    
    optional_vars = [
        'OPENAI_API_KEY',
        'ANTHROPIC_API_KEY', 
        'GEMINI_API_KEY'
    ]
    
    missing_required = []
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"❌ {var} is NOT set")
            missing_required.append(var)
    
    print("\nOptional API keys:")
    api_keys_found = 0
    for var in optional_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
            api_keys_found += 1
        else:
            print(f"⚠️  {var} is NOT set")
    
    if api_keys_found == 0:
        print("❌ No AI API keys found - you need at least one")
        missing_required.append("At least one AI API key")
    
    return len(missing_required) == 0, missing_required

def check_file_structure():
    """Check if required files exist."""
    print("\n🔍 Checking file structure...")
    
    required_files = [
        'src/auth/instagram_auth_manager.py',
        'src/auth/__init__.py',
        'setup_canadian_auth.py',
        'test_canadian_auth.py',
        'CANADIAN_AUTH_GUIDE.md',
        '.github/workflows/canadian_instagram_automation.yml'
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} missing")
            all_files_exist = False
    
    return all_files_exist

def main():
    """Main verification function."""
    print("🇨🇦 Canadian Instagram MCP Setup Verification")
    print("=" * 50)
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Check environment
    env_ok, missing_vars = check_environment()
    
    # Check files
    files_ok = check_file_structure()
    
    print("\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)
    
    if deps_ok and env_ok and files_ok:
        print("🎉 ALL CHECKS PASSED!")
        print("\n🚀 Next Steps:")
        print("1. Go to https://github.com/zegh6389/news-instagram-mcp/settings/secrets/actions")
        print("2. Add your Instagram credentials and API keys as repository secrets")
        print("3. Run: python setup_canadian_auth.py")
        print("4. Test with: python test_canadian_auth.py") 
        print("5. Trigger GitHub Actions workflow")
        
        return 0
    else:
        print("❌ Some checks failed:")
        
        if not deps_ok:
            print("  - Install missing Python dependencies")
        
        if not env_ok:
            print(f"  - Set missing environment variables: {', '.join(missing_vars)}")
        
        if not files_ok:
            print("  - Some required files are missing")
        
        print("\n📖 For detailed setup instructions, see:")
        print("  - QUICK_START_CANADIAN_AUTH.md")
        print("  - CANADIAN_AUTH_GUIDE.md")
        print("  - GITHUB_SECRETS_SETUP_CANADIAN.md")
        
        return 1

if __name__ == "__main__":
    exit(main())
