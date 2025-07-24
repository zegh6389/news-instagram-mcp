"""Scheduler for managing Instagram post timing and automation."""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta, time
import schedule
import threading
import time as time_module

from ..config import config
from ..database import DatabaseManager, InstagramPost, PostStatus, NewsArticle, ArticleStatus

logger = logging.getLogger(__name__)

class Scheduler:
    """Manages scheduling and automation of Instagram posts."""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.posting_config = config.get_instagram_posting_config()
        self.is_running = False
        self.scheduler_thread = None
        
        # Setup schedule
        self._setup_schedule()
    
    def _setup_schedule(self):
        """Setup recurring scheduled tasks."""
        # Schedule content processing
        schedule.every(30).minutes.do(self._process_pending_content)
        
        # Schedule post publishing
        schedule.every(5).minutes.do(self._publish_scheduled_posts)
        
        # Schedule engagement updates
        schedule.every(2).hours.do(self._update_engagement_stats)
        
        # Schedule cleanup tasks
        schedule.every().day.at("02:00").do(self._cleanup_old_data)
        
        # Schedule analytics updates
        schedule.every().day.at("23:30").do(self._update_daily_analytics)
    
    def start(self):
        """Start the scheduler in a background thread."""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return
        
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        logger.info("Scheduler started")
    
    def stop(self):
        """Stop the scheduler."""
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        logger.info("Scheduler stopped")
    
    def _run_scheduler(self):
        """Run the scheduler loop."""
        while self.is_running:
            try:
                schedule.run_pending()
                time_module.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                time_module.sleep(60)
    
    def get_next_posting_time(self, category: Optional[str] = None) -> datetime:
        """Get the next optimal posting time."""
        try:
            now = datetime.utcnow()
            
            # Get preferred posting times
            preferred_times = self.posting_config.get('preferred_times', ['09:00', '12:00', '15:00', '18:00', '21:00'])
            min_interval_hours = self.posting_config.get('min_interval_hours', 3)
            
            # Get last post time
            last_post = self._get_last_post_time()
            
            # Find next available time slot
            for time_str in preferred_times:
                hour, minute = map(int, time_str.split(':'))
                next_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                # If time has passed today, try tomorrow
                if next_time <= now:
                    next_time += timedelta(days=1)
                
                # Check minimum interval
                if last_post:
                    time_diff = (next_time - last_post).total_seconds() / 3600
                    if time_diff < min_interval_hours:
                        continue
                
                # Check daily post limit
                if not self._exceeds_daily_limit(next_time.date()):
                    return next_time
            
            # If no preferred time works, find next available slot
            return self._find_next_available_slot(now)
            
        except Exception as e:
            logger.error(f"Error getting next posting time: {e}")
            # Fallback: next hour
            return datetime.utcnow() + timedelta(hours=1)
    
    def _get_last_post_time(self) -> Optional[datetime]:
        """Get the timestamp of the last published post."""
        try:
            session = self.db_manager.get_session()
            last_post = session.query(InstagramPost).filter_by(
                status=PostStatus.PUBLISHED.value
            ).order_by(InstagramPost.published_time.desc()).first()
            session.close()
            
            return last_post.published_time if last_post else None
            
        except Exception as e:
            logger.error(f"Error getting last post time: {e}")
            return None
    
    def _exceeds_daily_limit(self, date: datetime.date) -> bool:
        """Check if posting on this date would exceed daily limit."""
        try:
            max_posts_per_day = self.posting_config.get('max_posts_per_day', 5)
            
            # Count posts for this date
            start_date = datetime.combine(date, time.min)
            end_date = start_date + timedelta(days=1)
            
            session = self.db_manager.get_session()
            post_count = session.query(InstagramPost).filter(
                InstagramPost.published_time >= start_date,
                InstagramPost.published_time < end_date,
                InstagramPost.status == PostStatus.PUBLISHED.value
            ).count()
            session.close()
            
            return post_count >= max_posts_per_day
            
        except Exception as e:
            logger.error(f"Error checking daily limit: {e}")
            return False
    
    def _find_next_available_slot(self, start_time: datetime) -> datetime:
        """Find the next available posting slot."""
        try:
            min_interval_hours = self.posting_config.get('min_interval_hours', 3)
            max_posts_per_day = self.posting_config.get('max_posts_per_day', 5)
            
            current_time = start_time
            
            # Look up to 7 days ahead
            for _ in range(7 * 24):  # 7 days * 24 hours
                # Check if this time slot is available
                if not self._exceeds_daily_limit(current_time.date()):
                    last_post = self._get_last_post_time()
                    
                    if not last_post or (current_time - last_post).total_seconds() >= min_interval_hours * 3600:
                        return current_time
                
                current_time += timedelta(hours=1)
            
            # Fallback: 24 hours from now
            return start_time + timedelta(days=1)
            
        except Exception as e:
            logger.error(f"Error finding next available slot: {e}")
            return start_time + timedelta(hours=3)
    
    def schedule_post(self, post_id: int, schedule_time: Optional[datetime] = None) -> bool:
        """Schedule a post for publishing."""
        try:
            if not schedule_time:
                schedule_time = self.get_next_posting_time()
            
            # Update post with schedule time
            success = self.db_manager.update_post_status(
                post_id,
                PostStatus.SCHEDULED,
                scheduled_time=schedule_time
            )
            
            if success:
                logger.info(f"Scheduled post {post_id} for {schedule_time}")
            else:
                logger.error(f"Failed to schedule post {post_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error scheduling post {post_id}: {e}")
            return False
    
    def _process_pending_content(self):
        """Process pending content (scheduled task)."""
        try:
            from ..processors import ContentAnalyzer, ImageProcessor, CaptionGenerator
            
            # Process scraped articles
            content_analyzer = ContentAnalyzer()
            stats = content_analyzer.process_articles(limit=10)
            
            if stats.get('processed', 0) > 0:
                logger.info(f"Processed {stats['processed']} articles")
            
            # Generate posts for high-priority articles
            self._auto_generate_posts()
            
        except Exception as e:
            logger.error(f"Error in process_pending_content: {e}")
    
    def _auto_generate_posts(self):
        """Automatically generate posts for high-priority articles."""
        try:
            from ..processors import ImageProcessor, CaptionGenerator
            
            # Get processed articles that don't have posts yet
            session = self.db_manager.get_session()
            articles = session.query(NewsArticle).filter(
                NewsArticle.status == ArticleStatus.PROCESSED.value,
                ~NewsArticle.instagram_posts.any()  # No existing posts
            ).order_by(NewsArticle.scraped_date.desc()).limit(5).all()
            session.close()
            
            if not articles:
                return
            
            image_processor = ImageProcessor()
            caption_generator = CaptionGenerator()
            
            for article in articles:
                try:
                    # Skip if article is too old
                    if article.scraped_date < datetime.utcnow() - timedelta(hours=24):
                        continue
                    
                    # Check if article meets criteria for auto-posting
                    if not self._should_auto_post(article):
                        continue
                    
                    # Process image
                    image_path = None
                    if article.image_url:
                        downloaded_path = image_processor.download_image(article.image_url, article.id)
                        if downloaded_path:
                            image_path = image_processor.process_image(downloaded_path, article.id)
                    
                    # Generate caption
                    template_type = self._determine_template_type(article)
                    caption_data = caption_generator.generate_caption(article, template_type)
                    
                    if 'error' in caption_data:
                        logger.warning(f"Failed to generate caption for article {article.id}")
                        continue
                    
                    # Create post
                    post_data = {
                        'article_id': article.id,
                        'caption': caption_data['caption'],
                        'hashtags': caption_data['hashtags'],
                        'image_path': image_path,
                        'template_used': template_type,
                        'status': PostStatus.DRAFT.value
                    }
                    
                    post = self.db_manager.save_instagram_post(post_data)
                    
                    if post:
                        # Schedule the post
                        schedule_time = self.get_next_posting_time(article.category)
                        self.schedule_post(post.id, schedule_time)
                        
                        logger.info(f"Auto-generated and scheduled post for article {article.id}")
                    
                except Exception as e:
                    logger.error(f"Error auto-generating post for article {article.id}: {e}")
            
        except Exception as e:
            logger.error(f"Error in auto_generate_posts: {e}")
    
    def _should_auto_post(self, article: NewsArticle) -> bool:
        """Determine if article should be auto-posted."""
        try:
            # Check article category and keywords
            auto_post_categories = ['breaking', 'politics', 'economy']
            
            if article.category in auto_post_categories:
                return True
            
            # Check for breaking news keywords
            breaking_keywords = ['breaking', 'urgent', 'alert', 'developing']
            content_text = (article.headline + " " + article.content).lower()
            
            if any(keyword in content_text for keyword in breaking_keywords):
                return True
            
            # Check article quality and importance
            if len(article.content.split()) > 200 and article.image_url:
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking auto-post criteria: {e}")
            return False
    
    def _determine_template_type(self, article: NewsArticle) -> str:
        """Determine template type for article."""
        content_text = (article.headline + " " + article.content).lower()
        
        # Breaking news
        if any(keyword in content_text for keyword in ['breaking', 'urgent', 'alert']):
            return 'breaking'
        
        # Analysis
        if article.category in ['politics', 'economy'] or 'analysis' in content_text:
            return 'analysis'
        
        return 'feature'
    
    def _publish_scheduled_posts(self):
        """Publish posts that are scheduled for now (scheduled task)."""
        try:
            from ..publishers import InstagramPublisher
            
            # Get posts scheduled for now
            now = datetime.utcnow()
            scheduled_posts = self.db_manager.get_scheduled_posts(now)
            
            if not scheduled_posts:
                return
            
            publisher = InstagramPublisher()
            
            for post in scheduled_posts:
                try:
                    result = publisher.publish_post(post)
                    
                    if result.get('success'):
                        logger.info(f"Published scheduled post {post.id}")
                    else:
                        logger.error(f"Failed to publish scheduled post {post.id}: {result.get('error')}")
                        
                        # Reschedule for later
                        new_schedule_time = now + timedelta(hours=1)
                        self.schedule_post(post.id, new_schedule_time)
                        
                except Exception as e:
                    logger.error(f"Error publishing scheduled post {post.id}: {e}")
            
        except Exception as e:
            logger.error(f"Error in publish_scheduled_posts: {e}")
    
    def _update_engagement_stats(self):
        """Update engagement stats for recent posts (scheduled task)."""
        try:
            from ..publishers import InstagramPublisher
            
            # Get recently published posts
            cutoff_time = datetime.utcnow() - timedelta(days=7)
            
            session = self.db_manager.get_session()
            recent_posts = session.query(InstagramPost).filter(
                InstagramPost.status == PostStatus.PUBLISHED.value,
                InstagramPost.published_time >= cutoff_time,
                InstagramPost.instagram_id.isnot(None)
            ).all()
            session.close()
            
            if not recent_posts:
                return
            
            publisher = InstagramPublisher()
            
            for post in recent_posts:
                try:
                    publisher.update_engagement_stats(post.id)
                    time_module.sleep(2)  # Rate limiting
                except Exception as e:
                    logger.error(f"Error updating engagement for post {post.id}: {e}")
            
            logger.info(f"Updated engagement stats for {len(recent_posts)} posts")
            
        except Exception as e:
            logger.error(f"Error in update_engagement_stats: {e}")
    
    def _cleanup_old_data(self):
        """Clean up old data (scheduled task)."""
        try:
            # Clean up old articles and posts
            cleanup_stats = self.db_manager.cleanup_old_data(days_to_keep=30)
            
            if cleanup_stats.get('deleted_articles', 0) > 0:
                logger.info(f"Cleaned up old data: {cleanup_stats}")
            
            # Clean up old images
            from ..processors import ImageProcessor
            image_processor = ImageProcessor()
            image_stats = image_processor.cleanup_old_images(days_old=7)
            
            if image_stats.get('deleted_downloads', 0) > 0:
                logger.info(f"Cleaned up old images: {image_stats}")
            
        except Exception as e:
            logger.error(f"Error in cleanup_old_data: {e}")
    
    def _update_daily_analytics(self):
        """Update daily analytics (scheduled task)."""
        try:
            # This could be expanded to send reports, update dashboards, etc.
            stats = self.db_manager.get_daily_stats()
            logger.info(f"Daily stats: {stats}")
            
        except Exception as e:
            logger.error(f"Error in update_daily_analytics: {e}")
    
    def get_schedule_status(self) -> Dict[str, Any]:
        """Get current scheduler status."""
        try:
            # Get upcoming scheduled posts
            session = self.db_manager.get_session()
            upcoming_posts = session.query(InstagramPost).filter(
                InstagramPost.status == PostStatus.SCHEDULED.value,
                InstagramPost.scheduled_time >= datetime.utcnow()
            ).order_by(InstagramPost.scheduled_time).limit(10).all()
            session.close()
            
            return {
                'is_running': self.is_running,
                'upcoming_posts': len(upcoming_posts),
                'next_post_time': upcoming_posts[0].scheduled_time.isoformat() if upcoming_posts else None,
                'last_check': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting schedule status: {e}")
            return {'error': str(e)}
    
    def manual_trigger(self, task_name: str) -> Dict[str, Any]:
        """Manually trigger a scheduled task."""
        try:
            if task_name == 'process_content':
                self._process_pending_content()
                return {'success': True, 'message': 'Content processing triggered'}
            
            elif task_name == 'publish_scheduled':
                self._publish_scheduled_posts()
                return {'success': True, 'message': 'Scheduled posts publishing triggered'}
            
            elif task_name == 'update_engagement':
                self._update_engagement_stats()
                return {'success': True, 'message': 'Engagement stats update triggered'}
            
            elif task_name == 'cleanup':
                self._cleanup_old_data()
                return {'success': True, 'message': 'Data cleanup triggered'}
            
            else:
                return {'success': False, 'error': f'Unknown task: {task_name}'}
                
        except Exception as e:
            logger.error(f"Error manually triggering {task_name}: {e}")
            return {'success': False, 'error': str(e)}
