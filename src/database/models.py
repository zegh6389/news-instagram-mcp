"""Database models for the news-instagram-mcp project."""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum

Base = declarative_base()

class ArticleStatus(Enum):
    """Status of news articles."""
    SCRAPED = "scraped"
    PROCESSED = "processed"
    PUBLISHED = "published"
    FAILED = "failed"
    SKIPPED = "skipped"

class PostStatus(Enum):
    """Status of Instagram posts."""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"

class NewsArticle(Base):
    """Model for news articles."""
    __tablename__ = 'news_articles'
    
    id = Column(Integer, primary_key=True)
    url = Column(String(500), unique=True, nullable=False, index=True)
    source = Column(String(100), nullable=False, index=True)
    headline = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    author = Column(String(200))
    published_date = Column(DateTime, index=True)
    scraped_date = Column(DateTime, default=datetime.utcnow, index=True)
    category = Column(String(50), index=True)
    keywords = Column(JSON)  # List of extracted keywords
    image_url = Column(String(500))
    image_path = Column(String(500))  # Local path to downloaded image
    status = Column(String(20), default=ArticleStatus.SCRAPED.value, index=True)
    processing_notes = Column(Text)
    
    # Relationships
    instagram_posts = relationship("InstagramPost", back_populates="article")
    processing_jobs = relationship("ProcessingJob", back_populates="article")
    
    def __repr__(self):
        return f"<NewsArticle(id={self.id}, headline='{self.headline[:50]}...', source='{self.source}')>"

class InstagramPost(Base):
    """Model for Instagram posts."""
    __tablename__ = 'instagram_posts'
    
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('news_articles.id'), nullable=False)
    caption = Column(Text, nullable=False)
    hashtags = Column(JSON)  # List of hashtags
    image_path = Column(String(500), nullable=False)
    template_used = Column(String(100))
    scheduled_time = Column(DateTime, index=True)
    published_time = Column(DateTime, index=True)
    instagram_id = Column(String(100))  # Instagram post ID
    instagram_url = Column(String(500))  # Instagram post URL
    status = Column(String(20), default=PostStatus.DRAFT.value, index=True)
    engagement_stats = Column(JSON)  # Likes, comments, shares, etc.
    created_date = Column(DateTime, default=datetime.utcnow)
    error_message = Column(Text)
    
    # Relationships
    article = relationship("NewsArticle", back_populates="instagram_posts")
    
    def __repr__(self):
        return f"<InstagramPost(id={self.id}, article_id={self.article_id}, status='{self.status}')>"

class ProcessingJob(Base):
    """Model for tracking processing jobs."""
    __tablename__ = 'processing_jobs'
    
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('news_articles.id'), nullable=False)
    job_type = Column(String(50), nullable=False)  # scraping, processing, publishing
    status = Column(String(20), nullable=False, index=True)  # pending, running, completed, failed
    started_at = Column(DateTime, index=True)
    completed_at = Column(DateTime, index=True)
    error_message = Column(Text)
    job_data = Column(JSON)  # Additional job-specific data
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    
    # Relationships
    article = relationship("NewsArticle", back_populates="processing_jobs")
    
    def __repr__(self):
        return f"<ProcessingJob(id={self.id}, type='{self.job_type}', status='{self.status}')>"

class ScrapingSession(Base):
    """Model for tracking scraping sessions."""
    __tablename__ = 'scraping_sessions'
    
    id = Column(Integer, primary_key=True)
    source = Column(String(100), nullable=False, index=True)
    started_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, index=True)
    articles_found = Column(Integer, default=0)
    articles_scraped = Column(Integer, default=0)
    articles_failed = Column(Integer, default=0)
    status = Column(String(20), nullable=False, index=True)
    error_message = Column(Text)
    
    def __repr__(self):
        return f"<ScrapingSession(id={self.id}, source='{self.source}', status='{self.status}')>"
