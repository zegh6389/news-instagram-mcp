# 📰📱 News Instagram MCP Server

> **An intelligent, fully-automated news-to-Instagram posting system** that scrapes Canadian news sources, processes content with AI, and publishes engaging Instagram posts using the Model Context Protocol (MCP).

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![Instagram API](https://img.shields.io/badge/Instagram-API-purple.svg)](https://developers.facebook.com/docs/instagram-api/)
[![AI Powered](https://img.shields.io/badge/AI-Powered-orange.svg)](https://openai.com/)

## 🚀 **What This System Does**

Transform Canadian news into engaging Instagram content **automatically**:

1. **🔍 Scrapes** latest news from CBC, Global News, CTV
2. **🧠 Analyzes** content with AI (categorization, sentiment, keywords)
3. **🎨 Creates** Instagram-ready visuals with templates
4. **✍️ Generates** compelling captions and hashtags
5. **⏰ Schedules** posts at optimal times
6. **📤 Publishes** directly to Instagram
7. **📊 Tracks** engagement and performance

## ✨ **Key Features**

### 🔥 **Intelligent News Processing**
- **Multi-Source Scraping**: CBC, Global News, CTV + Universal scraper for any site
- **AI Content Analysis**: Automatic categorization, sentiment analysis, importance scoring
- **Smart Filtering**: Duplicate detection, quality assessment, content validation
- **Real-time RSS Monitoring**: Continuous news feed monitoring with timeout handling

### 📱 **Instagram Automation**
- **Visual Content Creation**: Branded templates with automatic text overlay
- **AI Caption Generation**: Context-aware captions with relevant hashtags
- **Smart Scheduling**: Optimal posting times based on engagement analytics
- **Rate Limiting**: Respects Instagram API limits with intelligent delays
- **Engagement Tracking**: Monitors likes, comments, shares, reach

### 🤖 **MCP Integration**
- **Full MCP Server**: Complete Model Context Protocol implementation
- **6 Powerful Tools**: Scrape, analyze, generate, schedule, publish, analytics
- **Real-time Resources**: Live access to articles, posts, analytics, configuration
- **Claude Desktop Ready**: Seamless integration with AI assistants

### 🔒 **Enterprise-Grade Safety**
- **Content Moderation**: AI-powered content filtering and validation
- **Error Recovery**: Robust error handling with automatic retries
- **Database Integrity**: SQLite with migration support and backup
- **Comprehensive Logging**: Multi-level logging with rotation

## 🏗️ **Architecture**

```
news-instagram-mcp/
├── 🎯 main.py                 # Entry point (Standalone + MCP server modes)
├── 📁 src/
│   ├── 🕷️ scrapers/          # News source scrapers
│   │   ├── 📄 base_scraper.py     # Abstract base with RSS + timeout handling
│   │   ├── 🇨🇦 cbc_scraper.py      # CBC News specialized scraper
│   │   ├── 🌍 globalnews_scraper.py # Global News scraper
│   │   └── 🔄 universal_scraper.py  # Universal fallback for any site
│   ├── 🧠 processors/        # AI-powered content processing
│   │   ├── 📊 content_analyzer.py   # AI analysis, categorization, sentiment
│   │   ├── 🖼️ image_processor.py    # Download, resize, optimize images
│   │   └── ✍️ caption_generator.py  # AI caption + hashtag generation
│   ├── 🎨 editors/           # Visual content creation
│   │   ├── 🖌️ template_engine.py    # Template-based image generation
│   │   └── 🎭 visual_editor.py      # Advanced image editing capabilities
│   ├── 📤 publishers/        # Instagram publishing system
│   │   ├── 📱 instagram_publisher.py # Instagram API integration
│   │   └── ⏰ scheduler.py           # Smart scheduling engine
│   ├── 💾 database/          # Data management
│   │   ├── 📋 models.py             # SQLAlchemy models (Articles, Posts, Jobs)
│   │   └── 🔧 db_manager.py         # Database operations + analytics
│   ├── 🌐 mcp_server.py      # MCP server implementation (6 tools + 4 resources)
│   └── ⚙️ config.py          # Configuration management
├── 📁 config/                # Configuration files
│   ├── 📰 news_sources.yaml       # News source configurations
│   ├── 📱 instagram_config.yaml   # Instagram settings + safety limits
│   └── 🎨 template_config.yaml    # Visual template configurations
├── 📁 templates/             # Instagram post templates (PNG files)
│   ├── 🚨 breaking_news.png       # Breaking news template
│   ├── 📊 analysis_post.png       # Analysis template  
│   └── 📖 feature_story.png       # Feature story template
├── 📁 tests/                 # Comprehensive test suite
├── 📁 logs/                  # Application logs
└── 📄 .env                   # Environment variables (credentials)
```

## 🚀 **Quick Start - Get Running in 5 Minutes**

### **1. 📦 Installation**

```bash
# Clone the repository
git clone https://github.com/your-username/news-instagram-mcp.git
cd news-instagram-mcp

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### **2. ⚙️ Configuration**

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
notepad .env  # Windows
# nano .env   # Linux/Mac
```

**Required credentials:**
```env
# Instagram (REQUIRED)
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password

# AI API (OPTIONAL - Gemini included)
GEMINI_API_KEY=your_gemini_api_key

# System Settings (pre-configured)
DATABASE_URL=sqlite:///news_instagram.db
LOG_LEVEL=INFO
MAX_POSTS_PER_DAY=5
```

### **3. 🧪 Test the System**

```bash
# Test all components
python main.py

# Expected output:
# ✅ Instagram connection successful
# ✅ Database tables created
# ✅ News scrapers initialized (CBC, GlobalNews, CTV)
# ✅ MCP handlers registered
# ✅ System test completed!
```

### **4. 🚀 Launch MCP Server**

```bash
# Start MCP server for Claude Desktop
python main.py --stdio
```

## 🎯 **Usage Examples**

### **🤖 Via Claude Desktop (Recommended)**

Once configured in Claude Desktop, you can:

```
"Scrape the latest Canadian news and create 3 Instagram posts"

"Analyze recent articles and publish the most important breaking news"

"Generate a weekly analytics report for our Instagram performance"

"Schedule posts for optimal engagement times this week"
```

### **🔧 Via MCP Tools (Direct)**

```python
# Available MCP Tools:

1. scrape_news - Get latest articles from news sources
2. analyze_content - AI analysis of scraped content  
3. generate_post - Create Instagram post from article
4. schedule_post - Schedule post for optimal time
5. publish_post - Publish post immediately
6. get_analytics - Performance metrics and insights
```

### **💻 Programmatic Usage**

```python
from src.scrapers import CBCScraper
from src.processors import ContentAnalyzer, CaptionGenerator  
from src.publishers import InstagramPublisher

# Initialize components
scraper = CBCScraper('cbc', config.get_news_sources()['cbc'])
analyzer = ContentAnalyzer()
publisher = InstagramPublisher()

# Scrape and process
stats = scraper.run_scraping_session()
analyzer.process_articles(limit=10)

# Generate and publish
# (Full examples in documentation)
```

## 🛠️ **Advanced Configuration**

### **📰 Adding News Sources**

Add any news website to `config/news_sources.yaml`:

```yaml
your_news_site:
  name: "Your News Site"
  base_url: "https://yournews.com"
  rss_feeds:
    - "https://yournews.com/rss"
  selectors:
    headline: "h1.title"        # CSS selector for headlines
    content: ".article-body"    # CSS selector for content
    image: ".featured-image img" # CSS selector for images
  priority: 1                  # 1 = highest priority
  enabled: true               # Enable/disable source
```

### **🎨 Custom Templates**

Create custom Instagram templates:

1. Design 1080x1350px image in Photoshop/GIMP
2. Save as PNG in `templates/` folder
3. Configure in `config/template_config.yaml`
4. System automatically applies text overlays

### **⏰ Posting Schedule**

Customize posting times in `config/instagram_config.yaml`:

```yaml
instagram:
  posting:
    max_posts_per_day: 8
    min_interval_hours: 2
    preferred_times:
      - "08:00"  # Morning news
      - "12:00"  # Lunch break
      - "17:00"  # Evening commute
      - "20:00"  # Prime time
```

### **🔒 Safety & Rate Limiting**

```yaml
safety:
  rate_limit_delay: 30         # Seconds between API calls
  max_actions_per_hour: 60     # Maximum Instagram actions
  content_filters:             # Block inappropriate content
    - "inappropriate_keyword"
  manual_approval: false       # Require manual approval
```

## 📊 **Monitoring & Analytics**

### **📈 Performance Metrics**

Track comprehensive metrics:
- **Articles scraped** per day/week/month
- **Posts published** with success rates
- **Engagement metrics** (likes, comments, shares)
- **Error rates** by component
- **Processing times** and performance

### **📋 Available Analytics**

```python
# Daily statistics
stats = db_manager.get_daily_stats()
{
    'articles_scraped': 45,
    'posts_published': 8,
    'avg_engagement': 156.2,
    'error_rate': 0.02
}

# Weekly trends
trends = analytics.get_weekly_trends()
# Engagement optimization suggestions
suggestions = analytics.get_optimization_suggestions()
```

### **📊 Real-time Dashboard**

Access via MCP resources:
- `news://articles/recent` - Latest scraped articles
- `news://posts/scheduled` - Upcoming scheduled posts  
- `news://analytics/daily` - Performance dashboard
- `news://config/sources` - Current source configuration

## 🔌 **MCP Integration Setup**

### **For Claude Desktop:**

1. **Install Claude Desktop** (if not already installed)

2. **Add MCP configuration** to `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "news-instagram-mcp": {
      "command": "G:/cursor/news-instagram-mcp/.venv/Scripts/python.exe",
      "args": ["G:/cursor/news-instagram-mcp/main.py", "--stdio"],
      "env": {
        "PYTHONPATH": "G:/cursor/news-instagram-mcp"
      }
    }
  }
}
```

3. **Restart Claude Desktop**

4. **Test integration**: Ask Claude to "scrape news and create an Instagram post"

### **For Other MCP Clients:**

The server implements the full MCP specification and works with any MCP-compatible client.

## 🚨 **Troubleshooting**

### **Common Issues & Solutions**

| Issue | Solution |
|-------|----------|
| **Instagram login fails** | ✅ Check credentials, enable 2FA, use app password |
| **RSS feeds timeout** | ✅ Normal behavior - system handles gracefully |
| **"Module not found"** | ✅ Run `pip install -r requirements.txt` |
| **Database errors** | ✅ Delete `news_instagram.db` to reset database |
| **Unicode errors** | ✅ Fixed in v2.0 - restart if persists |
| **Memory issues** | ✅ Reduce batch sizes in configuration |

### **Debug Mode**

Enable detailed logging:

```bash
# Debug mode
python main.py --debug

# Check logs
tail -f logs/app.log        # Main application
tail -f logs/errors.log     # Error tracking
tail -f logs/instagram.log  # Publishing logs
```

### **System Health Check**

```bash
# Test all components
python main.py

# Expected output:
# ✅ Database tables created successfully
# ✅ Instagram session loaded
# ✅ MCP handlers registered  
# ✅ News scrapers available: ['cbc', 'globalnews', 'ctv']
# ✅ System test completed!
```

## 💡 **Pro Tips**

### **🚀 Optimization**

- **Peak Performance**: Run during off-peak hours for faster scraping
- **Engagement**: Schedule posts at 8AM, 12PM, 5PM, 8PM for best engagement
- **Content Quality**: Enable manual approval for critical accounts
- **Rate Limits**: Increase delays if hitting Instagram rate limits

### **🔧 Customization**

- **Custom Scrapers**: Create specialized scrapers for specific news sites
- **AI Models**: Switch between OpenAI, Anthropic, or Gemini for different styles
- **Templates**: Create branded templates matching your Instagram aesthetic
- **Hashtags**: Customize hashtag strategies in caption generator

### **📊 Analytics**

- **A/B Testing**: Test different posting times and templates
- **Content Performance**: Track which news categories perform best
- **Engagement Optimization**: Adjust posting schedule based on analytics
- **Quality Metrics**: Monitor content quality scores and engagement rates

## 🤝 **Contributing**

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes
4. **Add** tests for new functionality
5. **Ensure** code quality (`pylint`, `black`)
6. **Submit** a pull request

### **Development Setup**

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black src/
pylint src/

# Type checking
mypy src/
```

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 **Support**

- 📖 **Documentation**: Full API docs and guides available
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-username/news-instagram-mcp/issues) for bug reports
- 💬 **Discussions**: [GitHub Discussions](https://github.com/your-username/news-instagram-mcp/discussions) for questions
- 📧 **Email**: Enterprise support available

## 🚀 **Roadmap**

### **🔮 Upcoming Features**

- **Multi-Platform**: Twitter, Facebook, LinkedIn support
- **Advanced AI**: GPT-4 integration for enhanced content
- **Real-time Dashboard**: Live web interface for monitoring
- **A/B Testing**: Automated post optimization
- **Team Collaboration**: Multi-user support with roles
- **Content Calendar**: Editorial calendar integration

### **⚡ Performance Improvements**

- **Redis Caching**: Enhanced performance with Redis
- **Async Processing**: Concurrent scraping and processing  
- **PostgreSQL**: Enterprise database support
- **CDN Integration**: Optimized image delivery
- **Kubernetes**: Container orchestration support

---

## 🎉 **Ready to Transform Your News Coverage?**

Get started now and automate your news-to-Instagram workflow!

```bash
git clone https://github.com/your-username/news-instagram-mcp.git
cd news-instagram-mcp
python main.py --stdio
```

**Follow us for updates**: [@newsmcp](https://instagram.com/newsmcp) | **Star on GitHub** ⭐

---

*Made with ❤️ for the news and social media community*

## 🚀 Quick Start - Your First Post

### What You Need:
1. **Instagram Business/Creator Account** (required)
2. **Instagram Username & Password**
3. **OpenAI API Key** (optional but recommended)

### Setup Steps:
1. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your credentials
```

2. Add your credentials to `.env`:
```env
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
OPENAI_API_KEY=sk-your-key-here  # optional
```

3. Run system test:
```bash
python test_system.py
```

4. If all tests pass, generate your first post:
```bash
python main.py
# Then use MCP tools: scrape_news -> analyze_content -> generate_post -> publish_post
```

See `FIRST_POST_GUIDE.md` for detailed setup instructions.

## Configuration

### Environment Variables

- `INSTAGRAM_USERNAME`: Your Instagram username
- `INSTAGRAM_PASSWORD`: Your Instagram password
- `OPENAI_API_KEY`: OpenAI API key for content analysis
- `ANTHROPIC_API_KEY`: Anthropic API key (alternative to OpenAI)
- `DATABASE_URL`: Database connection string

### News Sources

Configure news sources in `config/news_sources.yaml`:
- Add RSS feeds
- Set CSS selectors for content extraction
- Define categories and keywords
- Configure content filters

### Instagram Settings

Configure Instagram posting in `config/instagram_config.yaml`:
- Set posting schedule and limits
- Define hashtag strategies
- Configure caption templates
- Set safety and rate limiting options

## Usage

### MCP Server

Start the MCP server:
```bash
python src/mcp_server.py
```

The server provides the following tools:
- `scrape_news`: Scrape news from configured sources
- `analyze_content`: Analyze scraped articles
- `generate_post`: Create Instagram posts from articles
- `schedule_post`: Schedule posts for publishing
- `publish_post`: Publish posts immediately
- `get_analytics`: Get performance analytics

### Manual Operations

```python
from src.scrapers import CBCScraper
from src.processors import ContentAnalyzer, CaptionGenerator
from src.publishers import InstagramPublisher

# Scrape news
scraper = CBCScraper('cbc', config.get_news_sources()['cbc'])
stats = scraper.run_scraping_session()

# Analyze content
analyzer = ContentAnalyzer()
analyzer.process_articles(limit=10)

# Generate and publish posts
caption_gen = CaptionGenerator()
publisher = InstagramPublisher()
# ... (see documentation for full examples)
```

## News Sources

### Supported Sources

- **CBC News**: Canada's national broadcaster
- **Global News**: Major Canadian news network
- **CTV News**: Canadian television network
- **Universal Scraper**: For additional news sources

### Adding New Sources

1. Add source configuration to `config/news_sources.yaml`
2. Create a custom scraper class (optional)
3. Update the MCP server to include the new source

## Content Processing

### Analysis Features

- **Categorization**: Automatic categorization (breaking, politics, economy, etc.)
- **Sentiment Analysis**: Emotional tone detection
- **Keyword Extraction**: Important terms and entities
- **Importance Scoring**: Priority ranking for content
- **Quality Assessment**: Content quality evaluation

### Image Processing

- **Download**: Automatic image retrieval from articles
- **Optimization**: Resize and optimize for Instagram
- **Template Creation**: Generate branded news graphics
- **Format Conversion**: Ensure Instagram compatibility

## Instagram Publishing

### Features

- **Smart Scheduling**: Optimal posting times based on engagement
- **Rate Limiting**: Respect Instagram's API limits
- **Engagement Tracking**: Monitor likes, comments, shares
- **Error Handling**: Robust error recovery and retry logic
- **Content Validation**: Ensure posts meet Instagram requirements

### Safety Features

- **Rate Limiting**: Prevent API violations
- **Content Filtering**: Remove inappropriate content
- **Duplicate Detection**: Avoid posting duplicate content
- **Manual Approval**: Optional manual review process

## Database Schema

### Tables

- `news_articles`: Scraped news articles
- `instagram_posts`: Generated Instagram posts
- `processing_jobs`: Background task tracking
- `scraping_sessions`: Scraping session logs

## API Reference

### MCP Resources

- `news://articles/recent`: Recent news articles
- `news://posts/scheduled`: Scheduled Instagram posts
- `news://analytics/daily`: Daily statistics
- `news://config/sources`: News source configuration

### MCP Tools

Each tool accepts specific parameters and returns structured results. See the MCP server implementation for detailed schemas.

## Monitoring and Analytics

### Metrics Tracked

- Articles scraped per day
- Posts published per day
- Engagement rates
- Error rates
- Processing times

### Logs

Comprehensive logging is available at multiple levels:
- INFO: General operations
- WARNING: Non-critical issues
- ERROR: Critical failures
- DEBUG: Detailed debugging information

## Development

### Testing

Run the test suite:
```bash
python -m pytest tests/
```

### Adding Features

1. Follow the existing architecture patterns
2. Add appropriate tests
3. Update configuration files
4. Document new features

## Troubleshooting

### Common Issues

1. **Instagram Login Issues**: Check credentials and 2FA settings
2. **Scraping Failures**: Verify news source URLs and selectors
3. **Image Processing Errors**: Ensure PIL/Pillow is properly installed
4. **Database Errors**: Check database connection and permissions

### Debug Mode

Enable debug logging in `.env`:
```
LOG_LEVEL=DEBUG
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[License information]

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the troubleshooting guide

## Changelog

See CHANGELOG.md for version history and updates.
