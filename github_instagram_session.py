#!/usr/bin/env python3
"""
Enhanced Instagram Session Manager for GitHub Actions
Handles session validation, recreation, and fallback authentication
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from instagrapi import Client
    INSTAGRAPI_AVAILABLE = True
except ImportError:
    INSTAGRAPI_AVAILABLE = False

logger = logging.getLogger(__name__)

class GitHubInstagramSession:
    """Enhanced Instagram session manager for GitHub Actions environment."""
    
    def __init__(self, username: str, password: str, session_file: str = "instagram_session.json"):
        self.username = username
        self.password = password
        self.session_file = session_file
        self.client = None
        
        if INSTAGRAPI_AVAILABLE:
            self.client = Client()
            
    def setup_client_settings(self):
        """Configure client with consistent settings for GitHub Actions."""
        if not self.client:
            return
            
        try:
            # Configure for consistent behavior
            self.client.set_proxy("")
            self.client.delay_range = [2, 4]  # Slightly longer delays for cloud environment
            
            # Set user agent for consistency
            self.client.set_user_agent(
                "Instagram 85.0.0.21.100 Android (24/7.0; 640dpi; 1440x2560; samsung; SM-G930F; herolte; samsungexynos8890; en_US)"
            )
            
            logger.info("✅ Instagram client configured for GitHub Actions")
            
        except Exception as e:
            logger.warning(f"⚠️ Could not apply all client settings: {e}")
    
    def validate_session(self) -> bool:
        """Validate if the current session is still active."""
        try:
            if not self.client:
                return False
                
            # Try to get account info to test session
            account_info = self.client.account_info()
            
            if account_info and account_info.username:
                logger.info(f"✅ Session valid for @{account_info.username}")
                return True
            else:
                logger.warning("⚠️ Session validation failed - no account info")
                return False
                
        except Exception as e:
            logger.warning(f"⚠️ Session validation error: {e}")
            return False
    
    def load_session_file(self) -> bool:
        """Load session from file if it exists and is valid."""
        session_path = Path(self.session_file)
        
        if not session_path.exists():
            logger.info("📄 No session file found")
            return False
            
        try:
            logger.info("📂 Loading Instagram session file...")
            self.client.load_settings(str(session_path))
            
            # Validate the loaded session
            if self.validate_session():
                logger.info("✅ Successfully loaded and validated session file")
                return True
            else:
                logger.warning("⚠️ Loaded session is invalid, will recreate")
                return False
                
        except Exception as e:
            logger.warning(f"⚠️ Failed to load session file: {e}")
            # Delete corrupted session file
            try:
                session_path.unlink()
                logger.info("🗑️ Deleted corrupted session file")
            except:
                pass
            return False
    
    def create_fresh_session(self) -> bool:
        """Create a fresh Instagram session with login."""
        try:
            logger.info("🔐 Creating fresh Instagram session...")
            
            # Configure client settings first
            self.setup_client_settings()
            
            # Attempt login
            self.client.login(self.username, self.password)
            
            # Validate the new session
            if self.validate_session():
                # Save the session
                self.client.dump_settings(self.session_file)
                logger.info("✅ Fresh session created and saved")
                return True
            else:
                logger.error("❌ Fresh session creation failed validation")
                return False
                
        except Exception as e:
            error_msg = str(e).lower()
            
            if "challenge" in error_msg or "verification" in error_msg:
                logger.error("❌ Instagram requires challenge verification")
                logger.info("💡 This usually happens in cloud environments")
                logger.info("💡 Consider using a pre-authenticated session file")
            elif "login" in error_msg:
                logger.error("❌ Login failed - check credentials")
            else:
                logger.error(f"❌ Unexpected login error: {e}")
                
            return False
    
    def attempt_relogin(self) -> bool:
        """Attempt to relogin with existing session data."""
        try:
            logger.info("🔄 Attempting relogin with existing session...")
            
            self.client.relogin()
            
            if self.validate_session():
                # Update session file
                self.client.dump_settings(self.session_file)
                logger.info("✅ Relogin successful")
                return True
            else:
                logger.warning("⚠️ Relogin failed validation")
                return False
                
        except Exception as e:
            logger.warning(f"⚠️ Relogin failed: {e}")
            return False
    
    def ensure_authenticated(self) -> bool:
        """Ensure Instagram client is authenticated, trying multiple methods."""
        if not self.client:
            logger.error("❌ Instagram client not available")
            return False
            
        logger.info("🔍 Ensuring Instagram authentication...")
        
        # Method 1: Try existing session validation
        if self.validate_session():
            logger.info("✅ Already authenticated")
            return True
        
        # Method 2: Try loading session file
        if self.load_session_file():
            return True
            
        # Method 3: Try relogin if session data exists
        session_path = Path(self.session_file)
        if session_path.exists():
            if self.attempt_relogin():
                return True
                
        # Method 4: Create fresh session (last resort)
        logger.info("💡 Trying fresh login as last resort...")
        if self.create_fresh_session():
            return True
            
        logger.error("❌ All authentication methods failed")
        return False
    
    def get_authenticated_client(self) -> Optional[Client]:
        """Get an authenticated Instagram client."""
        if self.ensure_authenticated():
            return self.client
        else:
            return None
    
    def get_account_summary(self) -> Dict[str, Any]:
        """Get a summary of the authenticated account."""
        try:
            if not self.validate_session():
                return {'error': 'Not authenticated'}
                
            account_info = self.client.account_info()
            
            return {
                'success': True,
                'username': account_info.username,
                'full_name': account_info.full_name,
                'followers': account_info.follower_count,
                'following': account_info.following_count,
                'posts': account_info.media_count,
                'is_verified': account_info.is_verified,
                'is_business': account_info.is_business
            }
            
        except Exception as e:
            return {'error': str(e)}

# Convenience function for GitHub Actions
def get_github_instagram_client(username: str, password: str, session_file: str = "instagram_session.json") -> Optional[Client]:
    """Get an authenticated Instagram client for GitHub Actions."""
    session_manager = GitHubInstagramSession(username, password, session_file)
    return session_manager.get_authenticated_client()

if __name__ == "__main__":
    # Test script
    import os
    
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')
    
    if not username or not password:
        print("❌ Please set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD environment variables")
        exit(1)
        
    session_manager = GitHubInstagramSession(username, password)
    client = session_manager.get_authenticated_client()
    
    if client:
        summary = session_manager.get_account_summary()
        print(f"✅ Authentication successful!")
        print(f"📱 Account: @{summary.get('username', 'unknown')}")
        print(f"👥 Followers: {summary.get('followers', 0)}")
    else:
        print("❌ Authentication failed")
        exit(1)
