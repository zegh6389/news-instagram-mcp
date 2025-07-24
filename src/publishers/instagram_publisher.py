"""Instagram publisher for posting content to Instagram."""

import logging
import time
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

try:
    from instagrapi import Client
    INSTAGRAPI_AVAILABLE = True
except ImportError:
    INSTAGRAPI_AVAILABLE = False

from ..config import config
from ..database import DatabaseManager, InstagramPost, PostStatus
from ..auth import InstagramAuthManager

logger = logging.getLogger(__name__)

class InstagramPublisher:
    """Publishes content to Instagram."""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.auth_manager = None
        self.client = None
        
        if INSTAGRAPI_AVAILABLE and config.instagram_username and config.instagram_password:
            self.auth_manager = InstagramAuthManager(
                username=config.instagram_username,
                password=config.instagram_password,
                session_dir="sessions"
            )
    
    def connect(self) -> bool:
        """Connect to Instagram using enhanced authentication."""
        try:
            if not self.auth_manager:
                logger.error("Instagram authentication manager not initialized")
                return False
            
            # Authenticate and get client
            self.client = self.auth_manager.get_client()
            
            if self.client and self.auth_manager.is_authenticated():
                account_info = self.client.account_info()
                logger.info(f"✅ Connected to Instagram as @{account_info.username}")
                logger.info(f"🍁 Location context: Milton, Ontario, Canada")
                logger.info(f"👥 Followers: {account_info.follower_count}")
                return True
            else:
                logger.error("❌ Failed to authenticate with Instagram")
                return False
            
        except Exception as e:
            logger.error(f"Error connecting to Instagram: {e}")
            return False
    
    def publish_post(self, post_id: int, caption_override: Optional[str] = None) -> Dict[str, Any]:
        """Publish an Instagram post."""
        try:
            if not self.client:
                return {'success': False, 'error': 'Instagram client not available'}
            
            # Get post from database
            session = self.db_manager.get_session()
            post = session.query(InstagramPost).filter_by(id=post_id).first()
            
            if not post:
                session.close()
                return {'success': False, 'error': f'Post {post_id} not found'}
            
            # Use override caption if provided
            original_caption = post.caption
            if caption_override:
                post.caption = caption_override
            
            # Validate post
            validation = self._validate_post(post)
            if not validation['is_valid']:
                session.close()
                return {'success': False, 'error': f"Post validation failed: {validation['errors']}"}
            
            # Prepare media
            media_path = self._prepare_media(post)
            if not media_path:
                # Restore original caption
                if caption_override:
                    post.caption = original_caption
                session.close()
                return {'success': False, 'error': 'Failed to prepare media'}
            
            # Upload post
            result = self._upload_post(post, media_path)
            
            if result['success']:
                # Update post status
                post.status = PostStatus.PUBLISHED.value
                post.published_time = datetime.utcnow()
                post.instagram_id = result.get('instagram_id')
                post.instagram_url = result.get('url')
                
                # Save caption override if used
                if caption_override:
                    post.caption = caption_override
                
                session.commit()
            else:
                # Restore original caption on failure
                if caption_override:
                    post.caption = original_caption
            
            session.close()
            return result
            
        except Exception as e:
            logger.error(f"Error publishing post {post_id}: {e}")
            return {'success': False, 'error': str(e)}
            
            # Update post status with error
            self.db_manager.update_post_status(
                post.id,
                PostStatus.FAILED,
                error_message=str(e)
            )
            
            return {'success': False, 'error': str(e)}
    
    def _validate_post(self, post: InstagramPost) -> Dict[str, Any]:
        """Validate post before publishing."""
        validation = {
            'is_valid': True,
            'errors': []
        }
        
        # Check caption
        if not post.caption or len(post.caption.strip()) == 0:
            validation['is_valid'] = False
            validation['errors'].append('Caption is empty')
        
        if len(post.caption) > config.max_caption_length:
            validation['is_valid'] = False
            validation['errors'].append(f'Caption too long ({len(post.caption)} > {config.max_caption_length})')
        
        # Check image
        if not post.image_path:
            validation['is_valid'] = False
            validation['errors'].append('No image provided')
        elif not Path(post.image_path).exists():
            validation['is_valid'] = False
            validation['errors'].append('Image file not found')
        
        # Check Instagram limits
        hashtag_count = len([tag for tag in post.hashtags or [] if tag.startswith('#')])
        if hashtag_count > 30:
            validation['is_valid'] = False
            validation['errors'].append(f'Too many hashtags ({hashtag_count} > 30)')
        
        return validation
    
    def _prepare_media(self, post: InstagramPost) -> Optional[str]:
        """Prepare media for Instagram upload."""
        try:
            if not post.image_path or not Path(post.image_path).exists():
                logger.error(f"Image not found: {post.image_path}")
                return None
            
            # Image should already be processed and optimized
            # Just verify it meets Instagram requirements
            from PIL import Image
            
            with Image.open(post.image_path) as img:
                width, height = img.size
                
                # Check dimensions
                if width < 320 or height < 320:
                    logger.error(f"Image too small: {width}x{height}")
                    return None
                
                if width > 1080 or height > 1350:
                    logger.warning(f"Image may be too large: {width}x{height}")
                
                # Check file size
                file_size = Path(post.image_path).stat().st_size
                if file_size > 8 * 1024 * 1024:  # 8MB
                    logger.error(f"Image file too large: {file_size} bytes")
                    return None
            
            return post.image_path
            
        except Exception as e:
            logger.error(f"Error preparing media: {e}")
            return None
    
    def _upload_post(self, post: InstagramPost, media_path: str) -> Dict[str, Any]:
        """Upload post to Instagram."""
        try:
            # Rate limiting
            time.sleep(config.instagram_config.get('instagram', {}).get('safety', {}).get('rate_limit_delay', 30))
            
            # Upload photo
            media = self.client.photo_upload(
                path=media_path,
                caption=post.caption
            )
            
            if media:
                instagram_url = f"https://www.instagram.com/p/{media.code}/"
                
                return {
                    'success': True,
                    'instagram_id': media.id,
                    'instagram_url': instagram_url,
                    'media_code': media.code
                }
            else:
                return {'success': False, 'error': 'Upload failed - no media returned'}
                
        except Exception as e:
            logger.error(f"Error uploading to Instagram: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_post_engagement(self, instagram_id: str) -> Dict[str, Any]:
        """Get engagement stats for a published post."""
        try:
            if not self.client:
                return {'error': 'Instagram client not available'}
            
            # Get media info
            media_info = self.client.media_info(instagram_id)
            
            if media_info:
                return {
                    'likes': media_info.like_count,
                    'comments': media_info.comment_count,
                    'views': getattr(media_info, 'view_count', 0),
                    'shares': getattr(media_info, 'share_count', 0),
                    'saves': getattr(media_info, 'save_count', 0),
                    'reach': getattr(media_info, 'reach', 0),
                    'impressions': getattr(media_info, 'impressions', 0)
                }
            else:
                return {'error': 'Media not found'}
                
        except Exception as e:
            logger.error(f"Error getting engagement for {instagram_id}: {e}")
            return {'error': str(e)}
    
    def update_engagement_stats(self, post_id: int) -> bool:
        """Update engagement stats for a published post."""
        try:
            # Get post
            session = self.db_manager.get_session()
            post = session.query(InstagramPost).filter_by(id=post_id).first()
            session.close()
            
            if not post or not post.instagram_id:
                return False
            
            # Get engagement stats
            engagement = self.get_post_engagement(post.instagram_id)
            
            if 'error' not in engagement:
                # Update post with engagement stats
                self.db_manager.update_post_status(
                    post_id,
                    PostStatus.PUBLISHED,  # Keep current status
                    engagement_stats=engagement
                )
                
                logger.info(f"Updated engagement stats for post {post_id}")
                return True
            else:
                logger.error(f"Failed to get engagement for post {post_id}: {engagement['error']}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating engagement stats: {e}")
            return False
    
    def delete_post(self, instagram_id: str) -> bool:
        """Delete a post from Instagram."""
        try:
            if not self.client:
                logger.error("Instagram client not available")
                return False
            
            success = self.client.media_delete(instagram_id)
            
            if success:
                logger.info(f"Deleted Instagram post {instagram_id}")
            else:
                logger.error(f"Failed to delete Instagram post {instagram_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error deleting post {instagram_id}: {e}")
            return False
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get Instagram account information."""
        try:
            if not self.client:
                return {'error': 'Instagram client not available'}
            
            user_info = self.client.account_info()
            
            return {
                'username': user_info.username,
                'full_name': user_info.full_name,
                'biography': user_info.biography,
                'followers_count': user_info.follower_count,
                'following_count': user_info.following_count,
                'media_count': user_info.media_count,
                'is_verified': user_info.is_verified,
                'is_business': user_info.is_business
            }
            
        except Exception as e:
            logger.error(f"Error getting account info: {e}")
            return {'error': str(e)}
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Instagram connection."""
        try:
            if not INSTAGRAPI_AVAILABLE:
                return {
                    'success': False,
                    'error': 'instagrapi not installed'
                }
            
            if not self.client:
                return {
                    'success': False,
                    'error': 'Instagram client not initialized'
                }
            
            # Try to get account info
            account_info = self.get_account_info()
            
            if 'error' not in account_info:
                return {
                    'success': True,
                    'username': account_info['username'],
                    'followers': account_info['followers_count'],
                    'following': account_info['following_count']
                }
            else:
                return {
                    'success': False,
                    'error': account_info['error']
                }
                
        except Exception as e:
            logger.error(f"Error testing connection: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_posting_guidelines(self) -> Dict[str, Any]:
        """Get Instagram posting guidelines and limits."""
        return {
            'image_requirements': {
                'min_width': 320,
                'min_height': 320,
                'max_width': 1080,
                'max_height': 1350,
                'max_file_size_mb': 8,
                'supported_formats': ['jpg', 'jpeg', 'png']
            },
            'caption_requirements': {
                'max_length': 2200,
                'max_hashtags': 30,
                'max_mentions': 20
            },
            'posting_limits': {
                'max_posts_per_day': 25,
                'max_posts_per_hour': 5,
                'recommended_interval_minutes': 30
            },
            'best_practices': [
                'Post during peak engagement hours',
                'Use relevant hashtags',
                'Include call-to-action',
                'Maintain consistent posting schedule',
                'Engage with followers'
            ]
        }
