#!/usr/bin/env python3
"""
Manual automation script for GitHub Actions
Allows custom parameters via workflow dispatch
"""

import asyncio
import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
src_dir = project_root / 'src'
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_dir))

from src.mcp_server import NewsInstagramMCPServer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/manual_automation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class ManualAutomation:
    def __init__(self):
        self.server = None
        self.stats = {
            'posts_generated': 0,
            'posts_published': 0,
            'errors': []
        }
    
    async def initialize(self):
        """Initialize the MCP server"""
        try:
            logging.info("🚀 Initializing News Instagram MCP Server...")
            self.server = NewsInstagramMCPServer()
            logging.info("✅ MCP Server initialized successfully")
            return True
        except Exception as e:
            logging.error(f"❌ Failed to initialize server: {e}")
            self.stats['errors'].append(str(e))
            return False
    
    async def quick_scrape(self):
        """Quick news scrape for fresh content"""
        try:
            logging.info("📰 Quick news scrape...")
            result = await self.server._scrape_news_tool({'limit': 20})
            logging.info("✅ Quick scrape completed")
            return True
        except Exception as e:
            logging.warning(f"⚠️ Quick scrape failed: {e}")
            return False
    
    async def run_manual_automation(self, posts_count, template_type, immediate_publish):
        """Run manual automation with custom parameters"""
        
        logging.info(f"🎯 Manual automation starting...")
        logging.info(f"📋 Parameters: {posts_count} posts, {template_type} template, publish={immediate_publish}")
        
        start_time = datetime.now()
        
        # Initialize
        if not await self.initialize():
            return False
        
        # Quick scrape for fresh content
        await self.quick_scrape()
        
        # Determine templates to use
        if template_type == 'mixed':
            templates = ['breaking', 'analysis', 'feature']
        else:
            templates = [template_type]
        
        # Generate posts
        logging.info(f"🎨 Generating {posts_count} posts...")
        
        for i in range(posts_count):
            try:
                template = templates[i % len(templates)]
                
                result = await self.server._generate_post_tool({
                    'article_id': i + 1,
                    'template_type': template
                })
                
                if result:
                    self.stats['posts_generated'] += 1
                    logging.info(f"✅ Generated post {i+1} with {template} template")
                    
                    # Publish immediately if requested
                    if immediate_publish:
                        try:
                            publish_result = await self.server._publish_post_tool({
                                'post_id': i + 1,
                                'caption_override': f'🎯 Manual Post {i+1} - {datetime.now().strftime("%B %d, %Y")} | {template.title()} Template #ManualPost #NewsAutomation'
                            })
                            
                            if publish_result:
                                self.stats['posts_published'] += 1
                                logging.info(f"📱 Published post {i+1}")
                            else:
                                logging.warning(f"⚠️ Failed to publish post {i+1}")
                                
                        except Exception as e:
                            logging.error(f"❌ Error publishing post {i+1}: {e}")
                            self.stats['errors'].append(f"Publish post {i+1}: {e}")
                else:
                    logging.warning(f"⚠️ Failed to generate post {i+1}")
                    
            except Exception as e:
                logging.error(f"❌ Error generating post {i+1}: {e}")
                self.stats['errors'].append(f"Generate post {i+1}: {e}")
                continue
        
        # Log final results
        end_time = datetime.now()
        duration = end_time - start_time
        
        logging.info(f"⏱️ Manual automation completed in {duration}")
        logging.info(f"📊 Results: {self.stats['posts_generated']} generated, {self.stats['posts_published']} published")
        
        if self.stats['errors']:
            logging.info(f"❌ {len(self.stats['errors'])} errors encountered:")
            for error in self.stats['errors']:
                logging.info(f"  - {error}")
        
        # Create GitHub Actions summary
        summary_file = os.environ.get('GITHUB_STEP_SUMMARY', 'manual_summary.md')
        try:
            with open(summary_file, 'w') as f:
                f.write(f"""# Manual Automation Results - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 📋 Parameters
- **Posts Count**: {posts_count}
- **Template Type**: {template_type}
- **Immediate Publish**: {immediate_publish}

## 📊 Results
- 🎨 **Posts Generated**: {self.stats['posts_generated']}
- 📱 **Posts Published**: {self.stats['posts_published']}
- ⏱️ **Duration**: {duration}

## 🎯 Status
{'✅ **SUCCESS**: All operations completed!' if len(self.stats['errors']) == 0 else f'⚠️ **PARTIAL SUCCESS**: {len(self.stats["errors"])} errors encountered'}

## 📝 Error Details
{chr(10).join([f'- {error}' for error in self.stats['errors']]) if self.stats['errors'] else 'No errors encountered!'}
""")
        except Exception as e:
            logging.warning(f"Failed to create GitHub summary: {e}")
        
        return self.stats['posts_generated'] > 0

async def main():
    """Main manual automation function"""
    
    # Get parameters from environment (set by GitHub Actions)
    posts_count = int(os.getenv('POSTS_COUNT', '3'))
    template_type = os.getenv('TEMPLATE_TYPE', 'mixed')
    immediate_publish = os.getenv('IMMEDIATE_PUBLISH', 'false').lower() == 'true'
    
    automation = ManualAutomation()
    
    try:
        success = await automation.run_manual_automation(posts_count, template_type, immediate_publish)
        
        if success:
            logging.info("🎉 Manual automation completed successfully!")
            sys.exit(0)
        else:
            logging.error("❌ Manual automation failed!")
            sys.exit(1)
            
    except Exception as e:
        logging.error(f"💥 Fatal error in manual automation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
