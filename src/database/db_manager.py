"""Database manager for the news-instagram-mcp project."""

from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from .models import Base, NewsArticle, InstagramPost, ProcessingJob, ScrapingSession, ArticleStatus, PostStatus
from ..config import config

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database operations."""
    
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or config.database_url
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.create_tables()
    
    def create_tables(self):
        """Create all database tables."""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Error creating database tables: {e}")
            raise
    
    def get_session(self) -> Session:
        """Get a database session."""
        return self.SessionLocal()
    
    # News Article operations
    def save_article(self, article_data: Dict[str, Any]) -> Optional[NewsArticle]:
        """Save a news article to the database."""
        session = self.get_session()
        try:
            # Check if article already exists
            existing = session.query(NewsArticle).filter_by(url=article_data['url']).first()
            if existing:
                logger.info(f"Article already exists: {article_data['url']}")
                return existing
            
            article = NewsArticle(**article_data)
            session.add(article)
            session.commit()
            session.refresh(article)
            logger.info(f"Saved new article: {article.headline}")
            return article
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error saving article: {e}")
            return None
        finally:
            session.close()
    
    def get_articles_by_status(self, status: ArticleStatus, limit: Optional[int] = None) -> List[NewsArticle]:
        """Get articles by status."""
        session = self.get_session()
        try:
            query = session.query(NewsArticle).filter_by(status=status.value)
            if limit:
                query = query.limit(limit)
            return query.all()
        finally:
            session.close()
    
    def get_recent_articles(self, hours: int = 24, limit: Optional[int] = None) -> List[NewsArticle]:
        """Get articles from the last N hours."""
        session = self.get_session()
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            query = session.query(NewsArticle).filter(
                NewsArticle.scraped_date >= cutoff_time
            ).order_by(NewsArticle.scraped_date.desc())
            if limit:
                query = query.limit(limit)
            return query.all()
        finally:
            session.close()
    
    def update_article_status(self, article_id: int, status: ArticleStatus, notes: Optional[str] = None) -> bool:
        """Update article status."""
        session = self.get_session()
        try:
            article = session.query(NewsArticle).filter_by(id=article_id).first()
            if not article:
                return False
            
            article.status = status.value
            if notes:
                article.processing_notes = notes
            
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error updating article status: {e}")
            return False
        finally:
            session.close()
    
    # Instagram Post operations
    def save_instagram_post(self, post_data: Dict[str, Any]) -> Optional[InstagramPost]:
        """Save an Instagram post to the database."""
        session = self.get_session()
        try:
            post = InstagramPost(**post_data)
            session.add(post)
            session.commit()
            session.refresh(post)
            logger.info(f"Saved new Instagram post for article {post.article_id}")
            return post
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error saving Instagram post: {e}")
            return None
        finally:
            session.close()
    
    def get_posts_by_status(self, status: PostStatus, limit: Optional[int] = None) -> List[InstagramPost]:
        """Get Instagram posts by status."""
        session = self.get_session()
        try:
            query = session.query(InstagramPost).filter_by(status=status.value)
            if limit:
                query = query.limit(limit)
            return query.all()
        finally:
            session.close()
    
    def get_scheduled_posts(self, before_time: Optional[datetime] = None) -> List[InstagramPost]:
        """Get scheduled posts that are ready to publish."""
        session = self.get_session()
        try:
            query = session.query(InstagramPost).filter_by(status=PostStatus.SCHEDULED.value)
            if before_time:
                query = query.filter(InstagramPost.scheduled_time <= before_time)
            return query.order_by(InstagramPost.scheduled_time).all()
        finally:
            session.close()
    
    def update_post_status(self, post_id: int, status: PostStatus, **kwargs) -> bool:
        """Update Instagram post status and other fields."""
        session = self.get_session()
        try:
            post = session.query(InstagramPost).filter_by(id=post_id).first()
            if not post:
                return False
            
            post.status = status.value
            
            # Update additional fields
            for key, value in kwargs.items():
                if hasattr(post, key):
                    setattr(post, key, value)
            
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error updating post status: {e}")
            return False
        finally:
            session.close()
    
    # Processing Job operations
    def create_processing_job(self, article_id: int, job_type: str, job_data: Optional[Dict] = None) -> Optional[ProcessingJob]:
        """Create a new processing job."""
        session = self.get_session()
        try:
            job = ProcessingJob(
                article_id=article_id,
                job_type=job_type,
                status='pending',
                job_data=job_data or {}
            )
            session.add(job)
            session.commit()
            session.refresh(job)
            return job
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error creating processing job: {e}")
            return None
        finally:
            session.close()
    
    def get_pending_jobs(self, job_type: Optional[str] = None) -> List[ProcessingJob]:
        """Get pending processing jobs."""
        session = self.get_session()
        try:
            query = session.query(ProcessingJob).filter_by(status='pending')
            if job_type:
                query = query.filter_by(job_type=job_type)
            return query.order_by(ProcessingJob.id).all()
        finally:
            session.close()
    
    def update_job_status(self, job_id: int, status: str, error_message: Optional[str] = None) -> bool:
        """Update processing job status."""
        session = self.get_session()
        try:
            job = session.query(ProcessingJob).filter_by(id=job_id).first()
            if not job:
                return False
            
            job.status = status
            if status == 'running' and not job.started_at:
                job.started_at = datetime.utcnow()
            elif status in ['completed', 'failed']:
                job.completed_at = datetime.utcnow()
            
            if error_message:
                job.error_message = error_message
                job.retry_count += 1
            
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error updating job status: {e}")
            return False
        finally:
            session.close()
    
    # Analytics and reporting
    def get_daily_stats(self, date: Optional[datetime] = None) -> Dict[str, int]:
        """Get daily statistics."""
        if not date:
            date = datetime.utcnow().date()
        
        session = self.get_session()
        try:
            start_date = datetime.combine(date, datetime.min.time())
            end_date = start_date + timedelta(days=1)
            
            articles_scraped = session.query(NewsArticle).filter(
                and_(NewsArticle.scraped_date >= start_date,
                     NewsArticle.scraped_date < end_date)
            ).count()
            
            posts_published = session.query(InstagramPost).filter(
                and_(InstagramPost.published_time >= start_date,
                     InstagramPost.published_time < end_date,
                     InstagramPost.status == PostStatus.PUBLISHED.value)
            ).count()
            
            return {
                'articles_scraped': articles_scraped,
                'posts_published': posts_published,
                'date': date.isoformat()
            }
        finally:
            session.close()
    
    def cleanup_old_data(self, days_to_keep: int = 30) -> Dict[str, int]:
        """Clean up old data from the database."""
        cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
        session = self.get_session()
        
        try:
            # Delete old articles and related data
            old_articles = session.query(NewsArticle).filter(
                NewsArticle.scraped_date < cutoff_date
            ).all()
            
            deleted_articles = 0
            deleted_posts = 0
            deleted_jobs = 0
            
            for article in old_articles:
                # Delete related posts
                posts = session.query(InstagramPost).filter_by(article_id=article.id).all()
                for post in posts:
                    session.delete(post)
                    deleted_posts += 1
                
                # Delete related jobs
                jobs = session.query(ProcessingJob).filter_by(article_id=article.id).all()
                for job in jobs:
                    session.delete(job)
                    deleted_jobs += 1
                
                # Delete article
                session.delete(article)
                deleted_articles += 1
            
            session.commit()
            
            return {
                'deleted_articles': deleted_articles,
                'deleted_posts': deleted_posts,
                'deleted_jobs': deleted_jobs
            }
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error cleaning up old data: {e}")
            return {'error': str(e)}
        finally:
            session.close()
