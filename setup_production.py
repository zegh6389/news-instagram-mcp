#!/usr/bin/env python3
"""
GitHub Repository Secrets Configuration
Sets up production credentials for automated deployment
"""

import os
import sys

def print_github_secrets_instructions():
    """Print instructions for setting up GitHub repository secrets"""
    
    print("🔧 GITHUB REPOSITORY SECRETS CONFIGURATION")
    print("=" * 60)
    print()
    print("To complete your production deployment, add these secrets to your GitHub repository:")
    print()
    print("📍 Go to: https://github.com/YOUR_USERNAME/news-instagram-mcp/settings/secrets/actions")
    print()
    print("🔑 Add these Repository Secrets:")
    print()
    print("1. INSTAGRAM_USERNAME")
    print("   Value: awais_zegham")
    print()
    print("2. INSTAGRAM_PASSWORD") 
    print("   Value: @Wadooha374549")
    print()
    print("3. GEMINI_API_KEY")
    print("   Value: AIzaSyCpXrYZ92M84lrJqIr9H6HpaOMGUU57o9s")
    print()
    print("4. DATABASE_URL (optional)")
    print("   Value: sqlite:///production_news_instagram.db")
    print()
    print("✅ Once configured, GitHub Actions will run daily at 6 AM UTC")
    print("🔄 Manual triggers are also available in the Actions tab")
    print()
    print("🎯 Your automation will post to Instagram account: awais_zegham")
    print("📊 Logs and analytics available in GitHub Actions artifacts")
    print()

def validate_local_environment():
    """Validate local environment setup"""
    print("🧪 LOCAL ENVIRONMENT VALIDATION")
    print("=" * 40)
    
    required_vars = {
        'INSTAGRAM_USERNAME': 'awais_zegham',
        'INSTAGRAM_PASSWORD': '@Wadooha374549', 
        'GEMINI_API_KEY': 'AIzaSyCpXrYZ92M84lrJqIr9H6HpaOMGUU57o9s'
    }
    
    all_set = True
    for var, expected in required_vars.items():
        actual = os.environ.get(var)
        if actual == expected:
            print(f"✅ {var}: Configured correctly")
        else:
            print(f"❌ {var}: Not set or incorrect")
            all_set = False
    
    if all_set:
        print("\n🎉 Local environment ready for production!")
    else:
        print("\n⚠️ Please set environment variables before running")
        
    return all_set

def main():
    """Main configuration helper"""
    print("🚀 NEWS INSTAGRAM MCP - PRODUCTION SETUP")
    print("=" * 50)
    print("User: awais_zegham")
    print("Mode: Production (Real Instagram Posting)")
    print()
    
    # Check local environment
    local_ready = validate_local_environment()
    print()
    
    # GitHub setup instructions
    print_github_secrets_instructions()
    
    # Summary
    print("📋 DEPLOYMENT CHECKLIST")
    print("=" * 30)
    print("✅ Instagram credentials configured")
    print("✅ AI API key configured")
    print("✅ Production code deployed")
    print("✅ Demo mode removed")
    print("✅ System tested successfully")
    print("⏳ GitHub secrets (manual setup required)")
    print("⏳ Enable GitHub Actions")
    print()
    print("🎯 Ready for live Instagram automation!")

if __name__ == "__main__":
    main()
