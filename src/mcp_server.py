"""MCP Server for news-instagram integration."""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

from mcp.server import Server
from mcp.types import Resource, Tool, TextContent, ImageContent

from .config import config
from .database import DatabaseManager, NewsArticle, InstagramPost, ArticleStatus, PostStatus
from .scrapers import CBCScraper, GlobalNewsScraper, UniversalScraper
from .processors import ContentAnalyzer, ImageProcessor, CaptionGenerator
from .publishers import InstagramPublisher, Scheduler

# Import demo publisher for fallback
try:
    from .publishers.demo_instagram_publisher import DemoInstagramPublisher
    DEMO_PUBLISHER_AVAILABLE = True
except ImportError:
    DEMO_PUBLISHER_AVAILABLE = False

logger = logging.getLogger(__name__)

class NewsInstagramMCPServer:
    """MCP Server for news-instagram automation."""
    
    def __init__(self):
        logger.info("Initializing NewsInstagramMCPServer...")
        self.server = Server("news-instagram-mcp")
        logger.info(f"Created MCP server with name: {self.server.name}")
        
        self.db_manager = DatabaseManager()
        
        # Initialize components
        self.scrapers = self._initialize_scrapers()
        self.content_analyzer = ContentAnalyzer()
        self.image_processor = ImageProcessor()
        self.caption_generator = CaptionGenerator()
        
        # Initialize Instagram publisher with fallback to demo mode
        self.instagram_publisher = self._initialize_instagram_publisher()
        self.scheduler = Scheduler()
        
        # Register MCP handlers
        logger.info("Registering MCP resources...")
        self._register_resources()
        logger.info("Registering MCP tools...")
        self._register_tools()
        logger.info("NewsInstagramMCPServer initialization complete")
    
    def _initialize_scrapers(self) -> Dict[str, Any]:
        """Initialize news scrapers."""
        scrapers = {}
        news_sources = config.get_news_sources()
        
        for source_id, source_config in news_sources.items():
            if source_id == 'cbc':
                scrapers[source_id] = CBCScraper(source_id, source_config)
            elif source_id == 'globalnews':
                scrapers[source_id] = GlobalNewsScraper(source_id, source_config)
            else:
                scrapers[source_id] = UniversalScraper(source_id, source_config)
        
        return scrapers
    
    def _initialize_instagram_publisher(self):
        """Initialize Instagram publisher with demo fallback."""
        # For demo purposes, always use demo publisher
        # In production, check credentials and try real publisher first
        
        # Uncomment this section for production with real Instagram credentials:
        # if config.instagram_username and config.instagram_password:
        #     try:
        #         publisher = InstagramPublisher()
        #         if hasattr(publisher, 'client') and publisher.client:
        #             logger.info("✅ Instagram publisher initialized with real credentials")
        #             return publisher
        #         else:
        #             logger.warning("⚠️ Instagram credentials available but client failed to initialize")
        #     except Exception as e:
        #         logger.warning(f"⚠️ Failed to initialize Instagram publisher: {e}")
        
        # Always use demo publisher for this demo environment
        if DEMO_PUBLISHER_AVAILABLE:
            logger.info("📱 Using demo Instagram publisher (simulation mode)")
            return DemoInstagramPublisher()
        else:
            logger.error("❌ No Instagram publisher available")
            return None
    
    def _register_resources(self):
        """Register MCP resources."""
        
        @self.server.list_resources()
        async def list_resources() -> List[Resource]:
            """List available resources."""
            return [
                Resource(
                    uri="news://articles/recent",
                    name="Recent News Articles",
                    description="Recently scraped news articles",
                    mimeType="application/json"
                ),
                Resource(
                    uri="news://posts/scheduled",
                    name="Scheduled Instagram Posts",
                    description="Scheduled Instagram posts",
                    mimeType="application/json"
                ),
                Resource(
                    uri="news://analytics/daily",
                    name="Daily Analytics",
                    description="Daily statistics and analytics",
                    mimeType="application/json"
                ),
                Resource(
                    uri="news://config/sources",
                    name="News Sources Configuration",
                    description="Configuration for news sources",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read a specific resource."""
            try:
                if uri == "news://articles/recent":
                    articles = self.db_manager.get_recent_articles(hours=24, limit=20)
                    return json.dumps([{
                        'id': article.id,
                        'headline': article.headline,
                        'source': article.source,
                        'category': article.category,
                        'status': article.status,
                        'published_date': article.published_date.isoformat() if article.published_date else None,
                        'scraped_date': article.scraped_date.isoformat(),
                        'url': article.url
                    } for article in articles], indent=2)
                
                elif uri == "news://posts/scheduled":
                    posts = self.db_manager.get_posts_by_status(PostStatus.SCHEDULED, limit=20)
                    return json.dumps([{
                        'id': post.id,
                        'article_id': post.article_id,
                        'scheduled_time': post.scheduled_time.isoformat() if post.scheduled_time else None,
                        'template_used': post.template_used,
                        'status': post.status
                    } for post in posts], indent=2)
                
                elif uri == "news://analytics/daily":
                    stats = self.db_manager.get_daily_stats()
                    return json.dumps(stats, indent=2)
                
                elif uri == "news://config/sources":
                    return json.dumps(config.get_news_sources(), indent=2)
                
                else:
                    return json.dumps({"error": "Resource not found"})
                    
            except Exception as e:
                logger.error(f"Error reading resource {uri}: {e}")
                return json.dumps({"error": str(e)})
    
    def _register_tools(self):
        """Register MCP tools."""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="scrape_news",
                    description="Scrape news from configured sources",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "source": {
                                "type": "string",
                                "description": "Specific news source to scrape (optional)"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of articles to scrape"
                            }
                        }
                    }
                ),
                Tool(
                    name="analyze_content",
                    description="Analyze scraped articles for content and categorization",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "article_id": {
                                "type": "integer",
                                "description": "Specific article ID to analyze (optional)"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of articles to analyze"
                            }
                        }
                    }
                ),
                Tool(
                    name="generate_post",
                    description="Generate Instagram post from news article",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "article_id": {
                                "type": "integer",
                                "description": "Article ID to create post from"
                            },
                            "template_type": {
                                "type": "string",
                                "description": "Template type (breaking, analysis, feature)"
                            }
                        },
                        "required": ["article_id"]
                    }
                ),
                Tool(
                    name="schedule_post",
                    description="Schedule Instagram post for publishing",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "post_id": {
                                "type": "integer",
                                "description": "Post ID to schedule"
                            },
                            "schedule_time": {
                                "type": "string",
                                "description": "ISO timestamp for scheduling (optional)"
                            }
                        },
                        "required": ["post_id"]
                    }
                ),
                Tool(
                    name="publish_post",
                    description="Publish Instagram post immediately",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "post_id": {
                                "type": "integer",
                                "description": "Post ID to publish"
                            }
                        },
                        "required": ["post_id"]
                    }
                ),
                Tool(
                    name="get_analytics",
                    description="Get analytics and statistics",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "period": {
                                "type": "string",
                                "description": "Time period (daily, weekly, monthly)"
                            },
                            "days": {
                                "type": "integer",
                                "description": "Number of days to include"
                            }
                        }
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Call a specific tool."""
            try:
                if name == "scrape_news":
                    return await self._scrape_news_tool(arguments)
                elif name == "analyze_content":
                    return await self._analyze_content_tool(arguments)
                elif name == "generate_post":
                    return await self._generate_post_tool(arguments)
                elif name == "schedule_post":
                    return await self._schedule_post_tool(arguments)
                elif name == "publish_post":
                    return await self._publish_post_tool(arguments)
                elif name == "get_analytics":
                    return await self._get_analytics_tool(arguments)
                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]
                    
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def _scrape_news_tool(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Scrape news tool implementation."""
        source = arguments.get('source')
        limit = arguments.get('limit')
        
        results = []
        total_stats = {'articles_found': 0, 'articles_scraped': 0, 'articles_failed': 0}
        
        if source and source in self.scrapers:
            # Scrape specific source
            scraper = self.scrapers[source]
            stats = scraper.run_scraping_session()
            results.append(f"Scraped {source}: {stats}")
            
            for key in total_stats:
                total_stats[key] += stats.get(key, 0)
        else:
            # Scrape all sources
            for source_id, scraper in self.scrapers.items():
                try:
                    stats = scraper.run_scraping_session()
                    results.append(f"Scraped {source_id}: {stats}")
                    
                    for key in total_stats:
                        total_stats[key] += stats.get(key, 0)
                        
                except Exception as e:
                    results.append(f"Error scraping {source_id}: {str(e)}")
        
        summary = f"""
News Scraping Complete:
- Total articles found: {total_stats['articles_found']}
- Successfully scraped: {total_stats['articles_scraped']}
- Failed: {total_stats['articles_failed']}

Details:
{chr(10).join(results)}
"""
        
        return [TextContent(type="text", text=summary)]
    
    async def _analyze_content_tool(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Analyze content tool implementation."""
        article_id = arguments.get('article_id')
        limit = arguments.get('limit', 10)
        
        if article_id:
            # Analyze specific article
            article = self.db_manager.get_session().query(NewsArticle).filter_by(id=article_id).first()
            if not article:
                return [TextContent(type="text", text=f"Article {article_id} not found")]
            
            analysis = self.content_analyzer.analyze_article(article)
            
            if 'error' in analysis:
                return [TextContent(type="text", text=f"Analysis failed: {analysis['error']}")]
            
            result = f"""
Article Analysis Complete:
- Article ID: {article.id}
- Headline: {article.headline}
- Category: {analysis['category']}
- Importance Score: {analysis['importance_score']:.2f}
- Sentiment: {analysis['sentiment']['classification']}
- Keywords: {', '.join(analysis['keywords'][:10])}
- Summary: {analysis['summary']}
"""
            
            return [TextContent(type="text", text=result)]
        else:
            # Analyze multiple articles
            stats = self.content_analyzer.process_articles(limit)
            
            result = f"""
Content Analysis Complete:
- Articles processed: {stats.get('processed', 0)}
- Articles failed: {stats.get('failed', 0)}
- Articles skipped: {stats.get('skipped', 0)}
"""
            
            return [TextContent(type="text", text=result)]
    
    async def _generate_post_tool(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Generate post tool implementation."""
        # Validate required parameters
        if 'article_id' not in arguments:
            return [TextContent(type="text", text="Error: article_id parameter is required")]
        
        article_id = arguments['article_id']
        template_type = arguments.get('template_type', 'feature')
        
        # Get article
        session = self.db_manager.get_session()
        article = session.query(NewsArticle).filter_by(id=article_id).first()
        session.close()
        
        if not article:
            return [TextContent(type="text", text=f"Article {article_id} not found")]
        
        try:
            # Download and process image
            image_path = None
            if article.image_url:
                downloaded_path = self.image_processor.download_image(article.image_url, article.id)
                if downloaded_path:
                    image_path = self.image_processor.process_image(downloaded_path, article.id)
            
            # Generate caption
            caption_data = self.caption_generator.generate_caption_data(article, template_type)
            
            if 'error' in caption_data:
                return [TextContent(type="text", text=f"Caption generation failed: {caption_data['error']}")]
            
            # Create Instagram post record
            post_data = {
                'article_id': article.id,
                'caption': caption_data['caption'],
                'hashtags': caption_data['hashtags'],
                'image_path': image_path,
                'template_used': template_type,
                'status': PostStatus.DRAFT.value
            }
            
            post = self.db_manager.save_instagram_post(post_data)
            
            if not post:
                return [TextContent(type="text", text="Failed to save Instagram post")]
            
            result = f"""
Instagram Post Generated:
- Post ID: {post.id}
- Article: {article.headline}
- Template: {template_type}
- Caption Length: {len(caption_data['caption'])} characters
- Hashtags: {len(caption_data['hashtags'])}
- Image: {'Yes' if image_path else 'No'}
- Status: {post.status}

Caption Preview:
{caption_data['caption'][:200]}...
"""
            
            return [TextContent(type="text", text=result)]
            
        except Exception as e:
            return [TextContent(type="text", text=f"Error generating post: {str(e)}")]
    
    async def _schedule_post_tool(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Schedule post tool implementation."""
        post_id = arguments['post_id']
        schedule_time = arguments.get('schedule_time')
        
        try:
            if schedule_time:
                schedule_dt = datetime.fromisoformat(schedule_time.replace('Z', '+00:00'))
            else:
                # Use scheduler to determine optimal time
                schedule_dt = self.scheduler.get_next_posting_time()
            
            # Update post status and schedule time
            success = self.db_manager.update_post_status(
                post_id,
                PostStatus.SCHEDULED,
                scheduled_time=schedule_dt
            )
            
            if success:
                result = f"""
Post Scheduled Successfully:
- Post ID: {post_id}
- Scheduled Time: {schedule_dt.isoformat()}
- Status: Scheduled
"""
            else:
                result = f"Failed to schedule post {post_id}"
            
            return [TextContent(type="text", text=result)]
            
        except Exception as e:
            return [TextContent(type="text", text=f"Error scheduling post: {str(e)}")]
    
    async def _publish_post_tool(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Publish post tool implementation."""
        post_id = arguments.get('post_id')
        caption_override = arguments.get('caption_override')
        
        try:
            # Check if publisher is available
            if not self.instagram_publisher:
                return [TextContent(type="text", text="Instagram publisher not available")]
            
            # If no post_id provided, get the latest draft post
            if not post_id:
                session = self.db_manager.get_session()
                latest_post = session.query(InstagramPost).filter_by(status=PostStatus.DRAFT.value).order_by(InstagramPost.created_date.desc()).first()
                session.close()
                
                if not latest_post:
                    return [TextContent(type="text", text="No draft posts available to publish")]
                
                post_id = latest_post.id
            
            # Get post
            session = self.db_manager.get_session()
            post = session.query(InstagramPost).filter_by(id=post_id).first()
            session.close()
            
            if not post:
                return [TextContent(type="text", text=f"Post {post_id} not found")]
            
            # Publish post
            result = self.instagram_publisher.publish_post(post_id, caption_override)
            
            if result.get('success'):
                publisher_type = "Demo" if hasattr(self.instagram_publisher, 'is_demo') else "Instagram"
                result_text = f"""
Post Published Successfully ({publisher_type}):
- Post ID: {post_id}
- Instagram ID: {result.get('instagram_id', 'N/A')}
- URL: {result.get('url', 'N/A')}
- Published Time: {datetime.utcnow().isoformat()}
- Status: Published
- Caption Length: {result.get('caption_length', 'N/A')} characters
"""
                if caption_override:
                    result_text += f"- Caption Override: Used"
            else:
                result_text = f"Failed to publish post {post_id}: {result.get('error')}"
            
            return [TextContent(type="text", text=result_text)]
            
        except Exception as e:
            return [TextContent(type="text", text=f"Error publishing post: {str(e)}")]
    
    async def _get_analytics_tool(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Get analytics tool implementation."""
        period = arguments.get('period', 'daily')
        days = arguments.get('days', 7)
        
        try:
            analytics_data = []
            
            for i in range(days):
                date = datetime.utcnow().date() - timedelta(days=i)
                stats = self.db_manager.get_daily_stats(date)
                analytics_data.append(stats)
            
            # Calculate totals
            total_articles = sum(day['articles_scraped'] for day in analytics_data)
            total_posts = sum(day['posts_published'] for day in analytics_data)
            
            result = f"""
Analytics Report ({period} - {days} days):

Summary:
- Total articles scraped: {total_articles}
- Total posts published: {total_posts}
- Average articles per day: {total_articles / days:.1f}
- Average posts per day: {total_posts / days:.1f}

Daily Breakdown:
"""
            
            for day_data in analytics_data:
                result += f"- {day_data['date']}: {day_data['articles_scraped']} articles, {day_data['posts_published']} posts\n"
            
            return [TextContent(type="text", text=result)]
            
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting analytics: {str(e)}")]
    
    async def run(self, read_stream, write_stream, initialization_options):
        """Run the MCP server with streams."""
        logger.info("Starting News Instagram MCP Server")
        
        # Start background scheduler
        asyncio.create_task(self._run_scheduler())
        
        # Run server with provided streams
        await self.server.run(read_stream, write_stream, initialization_options)
    
    async def _run_scheduler(self):
        """Run background scheduler for automated tasks."""
        while True:
            try:
                # Check for scheduled posts
                scheduled_posts = self.db_manager.get_scheduled_posts(datetime.utcnow())
                
                for post in scheduled_posts:
                    try:
                        result = self.instagram_publisher.publish_post(post)
                        if result.get('success'):
                            logger.info(f"Published scheduled post {post.id}")
                        else:
                            logger.error(f"Failed to publish scheduled post {post.id}: {result.get('error')}")
                    except Exception as e:
                        logger.error(f"Error publishing scheduled post {post.id}: {e}")
                
                # Wait before next check
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                logger.error(f"Error in scheduler: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error

# Main entry point
async def main():
    """Main entry point for the MCP server."""
    server = NewsInstagramMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
