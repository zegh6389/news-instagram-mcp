# News Instagram MCP Server

A comprehensive automated news-to-Instagram posting system that scrapes Canadian news sources, processes content using AI, and publishes engaging Instagram posts through the Model Context Protocol (MCP).

## 🚀 Features

- **Multi-Source News Scraping**: Automated scraping from Canadian news sources (CBC, Global News, CTV)
- **AI-Powered Content Analysis**: Content categorization, sentiment analysis, and keyword extraction
- **Intelligent Image Processing**: Automatic image download, optimization, and template generation
- **Smart Caption Generation**: AI-generated captions with relevant hashtags
- **Automated Scheduling**: Optimal posting times based on engagement analytics
- **Instagram Publishing**: Direct posting to Instagram with rate limiting and safety features
- **MCP Integration**: Full Model Context Protocol server for seamless AI assistant integration
- **Comprehensive Analytics**: Performance tracking and engagement metrics

## 🏗️ Architecture

```
news-instagram-mcp/
├── src/
│   ├── scrapers/          # News source scrapers
│   │   ├── base_scraper.py     # Abstract base scraper
│   │   ├── cbc_scraper.py      # CBC News scraper
│   │   ├── globalnews_scraper.py # Global News scraper
│   │   └── universal_scraper.py  # Universal fallback scraper
│   ├── processors/        # Content analysis and processing
│   │   ├── content_analyzer.py  # AI content analysis
│   │   ├── image_processor.py   # Image processing and optimization
│   │   └── caption_generator.py # Caption and hashtag generation
│   ├── editors/           # Visual content creation
│   │   ├── template_engine.py   # Template-based image generation
│   │   └── visual_editor.py     # Advanced image editing
│   ├── publishers/        # Instagram publishing and scheduling
│   │   ├── instagram_publisher.py # Instagram API integration
│   │   └── scheduler.py         # Smart scheduling engine
│   ├── database/          # Database models and management
│   │   ├── models.py           # SQLAlchemy models
│   │   └── db_manager.py       # Database operations
│   ├── mcp_server.py      # MCP server implementation
│   └── config.py          # Configuration management
├── config/                # Configuration files
│   ├── news_sources.yaml      # News source configurations
│   ├── instagram_config.yaml  # Instagram settings
│   └── template_config.yaml   # Visual template settings
├── templates/             # Visual templates for posts
├── tests/                 # Test suites
├── logs/                  # Application logs
└── main.py               # Entry point
```

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- SQLite (included with Python)
- Instagram Business/Creator account
- OpenAI or Anthropic API key (optional for AI features)

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd news-instagram-mcp
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application:**
   - Copy configuration templates
   - Set up Instagram credentials
   - Configure AI API keys (optional)

## ⚙️ Configuration

### Core Configuration (`src/config.py`)

The main configuration is managed through environment variables and YAML files:

```python
# Key configuration areas:
- Database settings (SQLite by default)
- API keys (Instagram, OpenAI, Anthropic)
- Scraping parameters (delays, timeouts)
- Content processing settings
- Publishing schedules
```

### News Sources (`config/news_sources.yaml`)

Configure news sources with CSS selectors and RSS feeds:

```yaml
news_sources:
  cbc:
    name: "CBC News"
    base_url: "https://www.cbc.ca"
    rss_feeds:
      - "https://www.cbc.ca/cmlink/rss-topstories"
    selectors:
      headline: "h1.detailHeadline"
      content: ".story-content"
      image: ".lead-media img"
      author: ".byline-author"
      date: "time"
    priority: 1
    enabled: true
```

**Adding New Sources:**

1. Add configuration to `news_sources.yaml`
2. Test selectors using browser developer tools
3. Optional: Create custom scraper class for complex sources
4. Enable in configuration

### Instagram Settings (`config/instagram_config.yaml`)

Control posting behavior and content formatting:

```yaml
instagram:
  posting:
    max_posts_per_day: 5
    min_interval_hours: 3
    preferred_times: ["09:00", "12:00", "15:00", "18:00", "21:00"]
  
  content:
    max_caption_length: 2200
    hashtag_limit: 30
    
  safety:
    rate_limit_delay: 30
    max_actions_per_hour: 60
```

**Key Settings:**
- **Rate Limiting**: Prevent Instagram API violations
- **Content Limits**: Respect platform constraints
- **Scheduling**: Optimal posting times
- **Safety**: Error handling and recovery

### Visual Templates (`config/template_config.yaml`)

Define image templates for different content types:

```yaml
templates:
  breaking_news:
    dimensions: [1080, 1350]
    text_areas:
      headline:
        position: [50, 200]
        font_size: 48
        color: "#FFFFFF"
        background_color: "#FF0000"
```

## 📖 Usage

### MCP Server Mode

The primary usage is as an MCP server for integration with AI assistants:

```bash
python main.py
```

**Available MCP Tools:**

1. **scrape_news**: Scrape news from configured sources
   ```json
   {
     "source": "cbc",  // optional: specific source
     "limit": 10       // optional: max articles
   }
   ```

2. **analyze_content**: Analyze scraped articles
   ```json
   {
     "article_id": 123,  // optional: specific article
     "limit": 10         // optional: max articles to process
   }
   ```

3. **generate_post**: Create Instagram post from article
   ```json
   {
     "article_id": 123,
     "template_type": "breaking"  // breaking, analysis, feature
   }
   ```

4. **schedule_post**: Schedule post for publishing
   ```json
   {
     "post_id": 456,
     "schedule_time": "2024-01-15T15:00:00Z"  // optional
   }
   ```

5. **publish_post**: Publish post immediately
   ```json
   {
     "post_id": 456
   }
   ```

6. **get_analytics**: Get performance metrics
   ```json
   {
     "period": "daily",  // daily, weekly, monthly
     "days": 7
   }
   ```

### Programmatic Usage

```python
from src.scrapers import CBCScraper, UniversalScraper
from src.processors import ContentAnalyzer, CaptionGenerator
from src.publishers import InstagramPublisher

# Initialize components
scraper = CBCScraper('cbc', config.get_news_sources()['cbc'])
analyzer = ContentAnalyzer()
caption_gen = CaptionGenerator()
publisher = InstagramPublisher()

# Scrape news
stats = scraper.run_scraping_session()
print(f"Scraped {stats['articles_scraped']} articles")

# Analyze content
analyzer.process_articles(limit=10)

# Generate and publish posts
# (see full examples in documentation)
```

## 🔧 Component Details

### Scrapers

**Base Scraper (`base_scraper.py`)**
- Abstract base class for all scrapers
- RSS feed parsing
- Article content extraction
- Database integration
- Error handling and retries

**CBC Scraper (`cbc_scraper.py`)**
- Specialized for CBC News structure
- Custom date parsing
- Content validation
- Image extraction

**Universal Scraper (`universal_scraper.py`)**
- Fallback for any news source
- Uses newspaper3k library
- Heuristic content extraction
- Configurable CSS selectors

**Features:**
- RSS feed monitoring
- Full article content extraction
- Duplicate detection
- Content quality validation
- Automatic categorization

### Processors

**Content Analyzer (`content_analyzer.py`)**
- AI-powered content analysis
- Sentiment analysis
- Keyword extraction
- Importance scoring
- Category classification

**Image Processor (`image_processor.py`)**
- Automatic image download
- Format conversion
- Resize and optimization
- Template application
- Instagram format compliance

**Caption Generator (`caption_generator.py`)**
- AI-generated captions
- Hashtag generation
- Length optimization
- Template-based formatting
- Engagement optimization

### Publishers

**Instagram Publisher (`instagram_publisher.py`)**
- Instagram API integration
- Post publishing
- Error handling
- Rate limiting
- Engagement tracking

**Scheduler (`scheduler.py`)**
- Optimal time calculation
- Queue management
- Conflict resolution
- Performance analytics

### Database

**Models (`models.py`)**
```python
class NewsArticle:
    # Article metadata and content
    url, headline, content, summary
    author, published_date, category
    keywords, image_url, status
    
class InstagramPost:
    # Generated post data
    article_id, caption, hashtags
    image_path, scheduled_time, status
    engagement_metrics
    
class ProcessingJob:
    # Background task tracking
    job_type, status, progress
    error_messages, completion_time
```

**Database Manager (`db_manager.py`)**
- SQLAlchemy ORM integration
- CRUD operations
- Query optimization
- Migration support
- Backup functionality

## 🔄 Reconfiguration Guide

### Adding New News Sources

1. **Add to configuration:**
   ```yaml
   # config/news_sources.yaml
   new_source:
     name: "New Source"
     base_url: "https://newssite.com"
     rss_feeds: ["https://newssite.com/rss"]
     selectors:
       headline: "h1.title"
       content: ".article-body"
       # ... other selectors
   ```

2. **Test selectors:**
   - Use browser developer tools
   - Verify CSS selectors work
   - Test with multiple articles

3. **Optional custom scraper:**
   ```python
   # src/scrapers/newsource_scraper.py
   class NewSourceScraper(BaseScraper):
       def _extract_content(self, soup, url):
           # Custom extraction logic
           pass
   ```

### Modifying Content Processing

**Customize analysis:**
```python
# src/processors/content_analyzer.py
def analyze_article(self, article):
    # Add custom analysis logic
    custom_score = self._calculate_custom_score(article)
    # ... existing analysis
```

**Update templates:**
```yaml
# config/template_config.yaml
new_template:
  dimensions: [1080, 1350]
  text_areas:
    # Define text positioning and styling
```

### Instagram Configuration

**Update posting schedule:**
```yaml
# config/instagram_config.yaml
posting:
  preferred_times: ["08:00", "13:00", "17:00", "20:00"]
  max_posts_per_day: 8
  min_interval_hours: 2
```

**Modify safety settings:**
```yaml
safety:
  rate_limit_delay: 60  # Increase delay
  max_actions_per_hour: 30  # Reduce actions
```

### Environment Variables

Create `.env` file:
```env
# Instagram API
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password

# AI Services (optional)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Database
DATABASE_URL=sqlite:///news_instagram.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

## 📊 Monitoring and Analytics

### Performance Metrics

- **Scraping Success Rate**: Articles successfully processed
- **Content Quality Score**: AI-generated quality metrics
- **Publishing Success Rate**: Instagram posting success
- **Engagement Metrics**: Likes, comments, shares
- **Error Rates**: Failed operations by component

### Logging

The system provides comprehensive logging:

```
logs/
├── app.log              # General application logs
├── scraping.log         # Scraping operations
├── processing.log       # Content processing
├── publishing.log       # Instagram publishing
└── errors.log          # Error tracking
```

### Database Analytics

```python
# Get performance statistics
stats = db_manager.get_daily_stats()
print(f"Articles scraped: {stats['articles_scraped']}")
print(f"Posts published: {stats['posts_published']}")
print(f"Average engagement: {stats['avg_engagement']}")
```

## 🛠️ Development

### Testing

Run the test suite:
```bash
python -m pytest tests/
```

**Test Coverage:**
- Unit tests for all components
- Integration tests for workflows
- Mock tests for external APIs
- Performance benchmarks

### Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure code quality (pylint, black)
5. Submit pull request

### Code Style

- Follow PEP 8
- Use type hints
- Document all functions
- Include docstrings

## 🔒 Security Considerations

### API Keys
- Store in environment variables
- Never commit to version control
- Use different keys for dev/prod
- Rotate keys regularly

### Rate Limiting
- Respect Instagram API limits
- Implement exponential backoff
- Monitor API usage
- Use proxy rotation if needed

### Content Safety
- Filter inappropriate content
- Validate image content
- Check caption compliance
- Manual review process

## 🐛 Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'mcp'"**
```bash
pip install mcp lxml_html_clean
```

**Instagram login failures:**
- Check credentials
- Verify 2FA settings
- Use app-specific password
- Check rate limiting

**Scraping failures:**
- Verify CSS selectors
- Check website changes
- Update User-Agent
- Monitor rate limits

**Memory issues:**
- Increase batch sizes
- Clear cache regularly
- Monitor database size
- Optimize queries

### Debug Mode

Run with debug logging:
```bash
python main.py --debug
```

### Log Analysis

Check specific log files:
```bash
tail -f logs/scraping.log    # Monitor scraping
tail -f logs/errors.log      # Check errors
```

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Support

- **Documentation**: Full API documentation available
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions
- **Email**: Support available for enterprise users

## 📈 Roadmap

### Upcoming Features

- **Multi-Platform Support**: Twitter, Facebook, LinkedIn
- **Advanced AI**: GPT-4 integration for content generation
- **Real-time Monitoring**: Live dashboard for operations
- **A/B Testing**: Post performance optimization
- **Content Scheduling**: Editorial calendar integration
- **Team Collaboration**: Multi-user support

### Performance Improvements

- **Caching**: Redis integration for performance
- **Async Processing**: Concurrent scraping and processing
- **Database Optimization**: PostgreSQL migration
- **CDN Integration**: Image delivery optimization

---

For more detailed information, see the API documentation and component-specific guides in the `/docs` directory.
