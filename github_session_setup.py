#!/usr/bin/env python3
"""
GitHub Actions Instagram Session Handler
Creates session file from GitHub Secrets for cloud deployment
"""

import json
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def setup_instagram_session_from_secret():
    """Setup Instagram session from GitHub Secret."""
    
    # Get session data from environment (GitHub Secret)
    session_data = os.getenv('INSTAGRAM_SESSION_DATA')
    
    if not session_data:
        logger.error("❌ INSTAGRAM_SESSION_DATA secret not found!")
        logger.info("💡 Please add INSTAGRAM_SESSION_DATA to GitHub repository secrets")
        return False
    
    try:
        # Parse the JSON session data
        session_json = json.loads(session_data)
        
        # Write to session file
        session_file = Path('instagram_session.json')
        with open(session_file, 'w') as f:
            json.dump(session_json, f, indent=2)
        
        logger.info("✅ Instagram session file created from GitHub Secret")
        logger.info(f"📄 Session file size: {session_file.stat().st_size} bytes")
        
        # Validate session structure
        required_keys = ['sessionid', 'csrftoken', 'ds_user_id', 'cookies']
        missing_keys = [key for key in required_keys if key not in session_json]
        
        if missing_keys:
            logger.warning(f"⚠️ Session missing keys: {missing_keys}")
            return False
        
        logger.info("✅ Session structure validated")
        return True
        
    except json.JSONDecodeError as e:
        logger.error(f"❌ Invalid JSON in INSTAGRAM_SESSION_DATA: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Failed to setup session: {e}")
        return False

def verify_session_file():
    """Verify the session file exists and is valid."""
    session_file = Path('instagram_session.json')
    
    if not session_file.exists():
        logger.error("❌ instagram_session.json not found")
        return False
    
    try:
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        
        # Check for essential session components
        sessionid = session_data.get('sessionid')
        if not sessionid:
            logger.error("❌ No sessionid in session file")
            return False
        
        logger.info(f"✅ Session file verified, sessionid: {sessionid[:20]}...")
        return True
        
    except Exception as e:
        logger.error(f"❌ Session file verification failed: {e}")
        return False

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    logger.info("🔐 Setting up Instagram session for GitHub Actions...")
    
    if setup_instagram_session_from_secret():
        if verify_session_file():
            logger.info("🎯 Instagram session ready for automation!")
        else:
            logger.error("❌ Session verification failed")
            exit(1)
    else:
        logger.error("❌ Failed to setup Instagram session")
        exit(1)
