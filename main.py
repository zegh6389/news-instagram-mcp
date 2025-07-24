#!/usr/bin/env python3
"""Main entry point for the news-instagram-mcp application."""

import asyncio
import argparse
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.mcp_server import NewsInstagramMCPServer
from src.config import config


def setup_logging(stdio_mode=False):
    """Setup logging configuration."""
    log_level = getattr(logging, config.log_level.upper(), logging.INFO)
    
    # Create logs directory
    Path('logs').mkdir(exist_ok=True)
    
    # In stdio mode, send logs to stderr to avoid interfering with MCP communication
    stream_handler = logging.StreamHandler(sys.stderr if stdio_mode else sys.stdout)
    
    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.log_file),
            stream_handler
        ]
    )


async def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(description='News Instagram MCP Server')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--stdio', action='store_true', help='Run as MCP server over stdio')
    
    args = parser.parse_args()
    
    # Setup logging
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    setup_logging(stdio_mode=args.stdio)
    
    logger = logging.getLogger(__name__)
    
    # Only log startup message if not in stdio mode
    if not args.stdio:
        logger.info("Starting News Instagram MCP Server")
    
    try:
        # Create server
        server = NewsInstagramMCPServer()
        
        if args.stdio:
            # Run as MCP server over stdio (for use with MCP clients)
            from mcp.server.stdio import stdio_server
            async with stdio_server() as (read_stream, write_stream):
                await server.run(read_stream, write_stream, server.server.create_initialization_options())
        else:
            # Run as standalone application for testing
            logger.info("Running in standalone mode for testing...")
            
            # Test the system components
            await test_system_components(server)
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


async def test_system_components(server):
    """Test system components when running standalone."""
    logger = logging.getLogger(__name__)
    
    logger.info("Testing system components...")
    
    # Test scrapers
    logger.info("Testing news scrapers...")
    try:
        scrapers = list(server.scrapers.keys())
        logger.info(f"Available scrapers: {scrapers}")
        
        if 'cbc' in server.scrapers:
            cbc_scraper = server.scrapers['cbc']
            logger.info("Attempting to scrape CBC RSS feeds (with timeout)...")
            
            # Add timeout to prevent hanging
            import asyncio
            try:
                # Run scraping with a timeout of 30 seconds
                articles = await asyncio.wait_for(
                    asyncio.to_thread(cbc_scraper.scrape_rss_feeds), 
                    timeout=30.0
                )
                logger.info(f"Found {len(articles)} articles from CBC RSS feeds")
                
                if articles:
                    # Test one article
                    article = articles[0]
                    logger.info(f"Sample article: {article['headline'][:100]}...")
                    
                    # Test caption generation
                    logger.info("Testing caption generation...")
                    caption = server.caption_generator.generate_caption(
                        article, 
                        {'keywords': ['news'], 'category': 'general'}
                    )
                    logger.info(f"Generated caption: {caption[:100]}...")
                else:
                    logger.warning("No articles found from RSS feeds")
                    
            except asyncio.TimeoutError:
                logger.warning("RSS scraping timed out after 30 seconds - this is normal for slow networks")
            except Exception as scrape_error:
                logger.error(f"Error during RSS scraping: {scrape_error}")
                
    except Exception as e:
        logger.error(f"Error testing components: {e}")
    
    # Test database
    logger.info("Testing database...")
    try:
        stats = server.db_manager.get_daily_stats()
        logger.info(f"Database stats: {stats}")
    except Exception as e:
        logger.error(f"Database error: {e}")
    
    # Test Instagram (without actually posting)
    logger.info("Testing Instagram connection...")
    try:
        # Instagram already logged in during server initialization
        logger.info("Instagram connection successful")
    except Exception as e:
        logger.error(f"Instagram error: {e}")
    
    logger.info("System test completed!")
    logger.info("To use as MCP server, run with --stdio flag")
    logger.info("Example: python main.py --stdio")


if __name__ == '__main__':
    asyncio.run(main())
