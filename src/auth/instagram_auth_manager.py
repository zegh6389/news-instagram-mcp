"""
Enhanced Instagram Authentication Manager
Handles location-aware authentication and session management for Milton, Canada
"""

import logging
import time
import json
import hashlib
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta

try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, ChallengeRequired, TwoFactorRequired
    INSTAGRAPI_AVAILABLE = True
except ImportError:
    INSTAGRAPI_AVAILABLE = False

logger = logging.getLogger(__name__)

class InstagramAuthManager:
    """Enhanced Instagram authentication manager for Canadian location."""
    
    def __init__(self, username: str, password: str, session_dir: str = "sessions"):
        self.username = username
        self.password = password
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(exist_ok=True)
        
        # Canadian location context
        self.location_context = {
            "city": "Milton",
            "region": "Ontario",
            "country": "Canada",
            "timezone": "America/Toronto",
            "locale": "en_CA"
        }
        
        self.client = None
        self.session_file = self.session_dir / f"{username}_session.json"
        self.device_file = self.session_dir / f"{username}_device.json"
        
        if INSTAGRAPI_AVAILABLE:
            self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Instagram client with Canadian settings."""
        self.client = Client()
        
        # Set Canadian device characteristics
        device_settings = self._get_canadian_device_settings()
        self.client.set_device(device_settings)
        
        # Set Canadian user agent
        self.client.set_user_agent(self._get_canadian_user_agent())
        
        # Configure delays to appear more human-like
        self.client.delay_range = [2, 5]  # Increased delays
        
        # Set locale for Canadian context
        self.client.set_locale("en_CA")
        
        logger.info(f"🍁 Initialized Instagram client for {self.location_context['city']}, {self.location_context['country']}")
    
    def _get_canadian_device_settings(self) -> Dict[str, Any]:
        """Generate consistent Canadian device settings."""
        device_file = self.device_file
        
        if device_file.exists():
            try:
                with open(device_file, 'r') as f:
                    device_data = json.load(f)
                logger.info("📱 Loaded existing Canadian device profile")
                return device_data
            except Exception as e:
                logger.warning(f"Failed to load device profile: {e}")
        
        # Generate new Canadian device profile
        device_id = self._generate_device_id()
        
        device_settings = {
            "app_version": "278.0.0.17.119",
            "android_version": "30",
            "android_release": "11.0",
            "dpi": "420dpi",
            "resolution": "1080x2340",
            "manufacturer": "samsung",
            "device": "SM-G991W",  # Canadian Samsung Galaxy S21 model
            "model": "SM-G991W",
            "cpu": "exynos2100",
            "version_code": "427156095",
            "device_id": device_id,
            "phone_id": self._generate_phone_id(),
        }
        
        # Save device profile for consistency
        try:
            with open(device_file, 'w') as f:
                json.dump(device_settings, f, indent=2)
            logger.info("💾 Saved Canadian device profile")
        except Exception as e:
            logger.warning(f"Failed to save device profile: {e}")
        
        return device_settings
    
    def _get_canadian_user_agent(self) -> str:
        """Generate Canadian-specific user agent."""
        return (
            "Instagram 278.0.0.17.119 Android (30/11; 420dpi; 1080x2340; "
            "samsung; SM-G991W; o1s; exynos2100; en_CA; 427156095)"
        )
    
    def _generate_device_id(self) -> str:
        """Generate consistent device ID based on username."""
        # Create deterministic device ID based on username
        seed = f"{self.username}_milton_canada"
        return hashlib.md5(seed.encode()).hexdigest()[:16]
    
    def _generate_phone_id(self) -> str:
        """Generate consistent phone ID."""
        seed = f"{self.username}_phone_milton"
        return hashlib.sha256(seed.encode()).hexdigest()[:16]
    
    def _is_session_valid(self) -> bool:
        """Check if existing session is still valid."""
        if not self.session_file.exists():
            return False
        
        try:
            # Check session file age (expire after 30 days)
            session_age = datetime.now() - datetime.fromtimestamp(self.session_file.stat().st_mtime)
            if session_age > timedelta(days=30):
                logger.info("📅 Session expired (older than 30 days)")
                return False
            
            # Try to load and validate session
            self.client.load_settings(str(self.session_file))
            
            # Test session with a simple API call
            account_info = self.client.account_info()
            if account_info and account_info.username == self.username:
                logger.info(f"✅ Valid session found for @{self.username}")
                return True
            
        except Exception as e:
            logger.warning(f"Session validation failed: {e}")
        
        return False
    
    def authenticate(self) -> bool:
        """Authenticate with Instagram using Canadian location context."""
        if not INSTAGRAPI_AVAILABLE:
            logger.error("❌ instagrapi not available")
            return False
        
        if not self.client:
            logger.error("❌ Instagram client not initialized")
            return False
        
        logger.info(f"🔐 Authenticating Instagram from {self.location_context['city']}, {self.location_context['country']}")
        
        # Try to use existing session first
        if self._is_session_valid():
            logger.info("🎉 Successfully authenticated using existing session")
            return True
        
        # Perform fresh login with Canadian context
        return self._fresh_login()
    
    def _fresh_login(self) -> bool:
        """Perform fresh login with Canadian location awareness."""
        try:
            logger.info("🔄 Performing fresh Instagram login...")
            
            # Add small delay to appear more human-like
            time.sleep(2)
            
            # Attempt login
            self.client.login(self.username, self.password)
            
            # Verify login
            account_info = self.client.account_info()
            if account_info:
                logger.info(f"✅ Successfully logged in as @{account_info.username}")
                logger.info(f"👥 Followers: {account_info.follower_count}")
                
                # Save session
                self.client.dump_settings(str(self.session_file))
                logger.info("💾 Session saved for future use")
                
                return True
            
            return False
            
        except ChallengeRequired as e:
            logger.warning("🔔 Instagram challenge required")
            return self._handle_challenge(e)
            
        except TwoFactorRequired:
            logger.warning("🔐 Two-factor authentication required")
            return self._handle_2fa()
            
        except LoginRequired as e:
            logger.error(f"❌ Login failed: {e}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Authentication error: {e}")
            
            # Handle specific Instagram blocking scenarios
            error_str = str(e).lower()
            
            if "forceappupgrade" in error_str or "manual login" in error_str:
                logger.error("🔒 Instagram App Upgrade/Manual Login Required!")
                logger.info("💡 IMMEDIATE ACTION REQUIRED:")
                logger.info("   1. 📱 Open Instagram app on your phone")
                logger.info("   2. 🔑 Log in manually with your credentials")
                logger.info("   3. ✅ Complete any security prompts or app updates")
                logger.info("   4. 🌍 Ensure you're logging in from Milton, Ontario, Canada")
                logger.info("   5. ⏰ Wait 2-4 hours after manual login")
                logger.info("   6. 🔄 Then retry the automation")
                logger.warning("⚠️  Automation is BLOCKED until manual login is completed!")
                
            elif "suspicious" in error_str or "location" in error_str:
                logger.error("🌍 Location-based blocking detected!")
                logger.info("💡 Recommendations:")
                logger.info("   1. Wait 24 hours before trying again")
                logger.info("   2. Log into Instagram manually from this location first")
                logger.info("   3. Verify your account isn't restricted")
                logger.info(f"   4. Ensure you're in {self.location_context['city']}, {self.location_context['country']}")
                
            elif "blocked" in error_str or "restricted" in error_str:
                logger.error("🚫 Account may be temporarily blocked!")
                logger.info("💡 Recovery steps:")
                logger.info("   1. 📱 Check Instagram app for any notifications")
                logger.info("   2. 🔍 Review account status in app")
                logger.info("   3. ⏰ Wait 24-48 hours before retrying")
                logger.info("   4. 📧 Check email for Instagram security alerts")
                
            else:
                logger.info("💡 General troubleshooting:")
                logger.info("   1. 📱 Try manual login on Instagram app first")
                logger.info("   2. 🔍 Check for account restrictions")
                logger.info("   3. ⏰ Wait and retry later")
                
            return False
    
    def _handle_challenge(self, challenge_error) -> bool:
        """Handle Instagram security challenges."""
        logger.info("📧 Instagram security challenge detected")
        logger.info("This typically happens when logging in from a new location or device")
        logger.info(f"Challenge details: {challenge_error}")
        
        # For automated systems, we can't interactively handle challenges
        # But we can provide guidance
        logger.warning("⚠️  Challenge handling not implemented for automated systems")
        logger.info("💡 To resolve:")
        logger.info("   1. Log into Instagram manually from this device/location")
        logger.info("   2. Complete any security challenges manually")
        logger.info("   3. Then retry the automation")
        
        return False
    
    def _handle_2fa(self) -> bool:
        """Handle two-factor authentication."""
        logger.warning("🔐 Two-factor authentication detected")
        logger.info("💡 For automated systems, consider:")
        logger.info("   1. Disabling 2FA temporarily (not recommended)")
        logger.info("   2. Using app passwords if available")
        logger.info("   3. Implementing 2FA code generation")
        
        return False
    
    def get_client(self) -> Optional[Client]:
        """Get authenticated Instagram client."""
        if self.client and self._is_session_valid():
            return self.client
        
        if self.authenticate():
            return self.client
        
        return None
    
    def is_authenticated(self) -> bool:
        """Check if currently authenticated."""
        try:
            if not self.client:
                return False
            
            account_info = self.client.account_info()
            return account_info is not None
            
        except Exception:
            return False
    
    def get_auth_status(self) -> Dict[str, Any]:
        """Get detailed authentication status."""
        status = {
            "authenticated": False,
            "session_exists": self.session_file.exists(),
            "device_profile_exists": self.device_file.exists(),
            "location": f"{self.location_context['city']}, {self.location_context['country']}",
            "recommendations": []
        }
        
        if not INSTAGRAPI_AVAILABLE:
            status["error"] = "instagrapi not available"
            status["recommendations"].append("Install instagrapi: pip install instagrapi")
            return status
        
        if self.session_file.exists():
            session_age = datetime.now() - datetime.fromtimestamp(self.session_file.stat().st_mtime)
            status["session_age_days"] = session_age.days
            status["session_expired"] = session_age > timedelta(days=30)
        
        try:
            status["authenticated"] = self.is_authenticated()
        except Exception as e:
            status["error"] = str(e)
            
            # Provide specific recommendations based on error
            error_str = str(e).lower()
            if "forceappupgrade" in error_str or "manual login" in error_str:
                status["recommendations"].extend([
                    "🔒 Manual login required on Instagram app",
                    "📱 Open Instagram app and log in manually",
                    "✅ Complete any security prompts",
                    "⏰ Wait 2-4 hours after manual login"
                ])
            elif "suspicious" in error_str or "location" in error_str:
                status["recommendations"].extend([
                    "🌍 Location-based blocking detected",
                    "📱 Log into Instagram app from current location",
                    "⏰ Wait 24 hours before retrying automation"
                ])
            else:
                status["recommendations"].append("📱 Try manual login on Instagram app first")
        
        return status
    
    def logout(self):
        """Logout and clean up session."""
        try:
            if self.client:
                self.client.logout()
            
            # Remove session file
            if self.session_file.exists():
                self.session_file.unlink()
                logger.info("🚪 Logged out and cleaned up session")
                
        except Exception as e:
            logger.warning(f"Logout cleanup error: {e}")
