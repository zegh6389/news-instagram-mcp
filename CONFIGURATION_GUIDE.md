# News Instagram MCP - Configuration Guide

## 📋 Quick Setup Checklist

1. ✅ Install Python 3.9+
2. ✅ Create virtual environment
3. ✅ Install dependencies: `pip install -r requirements.txt`
4. ✅ Configure news sources
5. ✅ Set up Instagram credentials
6. ✅ Configure AI API keys (optional)
7. ✅ Test the system

## 🔧 Component Configuration

### 1. News Scrapers Configuration

**File**: `config/news_sources.yaml`

```yaml
news_sources:
  # Add new sources here
  custom_news:
    name: "Custom News Site"
    base_url: "https://example-news.com"
    rss_feeds:
      - "https://example-news.com/rss"
    selectors:
      headline: "h1.title"        # CSS selector for headline
      content: ".article-body"    # CSS selector for content
      image: ".featured-image img" # CSS selector for image
      author: ".author-name"      # CSS selector for author
      date: "time"               # CSS selector for date
    priority: 2                  # Lower number = higher priority
    enabled: true               # Enable/disable this source
```

**How to find CSS selectors:**
1. Open news article in browser
2. Right-click on headline → "Inspect Element"
3. Right-click on highlighted HTML → "Copy" → "Copy selector"
4. Test selector in browser console: `document.querySelector("your-selector")`

### 2. Instagram Configuration

**File**: `config/instagram_config.yaml`

```yaml
instagram:
  posting:
    max_posts_per_day: 5          # Daily posting limit
    min_interval_hours: 3         # Minimum hours between posts
    preferred_times:              # Optimal posting times
      - "09:00"
      - "12:00" 
      - "15:00"
      - "18:00"
      - "21:00"
  
  content:
    max_caption_length: 2200      # Instagram caption limit
    hashtag_limit: 30            # Maximum hashtags per post
    mention_limit: 20            # Maximum mentions per post
  
  safety:
    rate_limit_delay: 30         # Seconds between API calls
    max_actions_per_hour: 60     # Maximum API actions per hour
```

**Instagram Credentials Setup:**
1. Create Instagram Business account
2. Get username/password or API tokens
3. Set environment variables:
   ```env
   INSTAGRAM_USERNAME=your_username
   INSTAGRAM_PASSWORD=your_password
   ```

### 3. Visual Templates Configuration

**File**: `config/template_config.yaml`

```yaml
templates:
  breaking_news:
    file: "breaking_news.png"        # Template image file
    dimensions: [1080, 1350]         # Instagram post dimensions
    text_areas:
      headline:
        position: [50, 200]          # X, Y coordinates
        max_width: 980               # Maximum text width
        font_size: 48                # Text size
        color: "#FFFFFF"             # Text color
        background_color: "#FF0000"   # Background color (optional)
        
  feature_story:
    file: "feature_story.png"
    dimensions: [1080, 1350]
    text_areas:
      headline:
        position: [50, 150]
        font_size: 42
        color: "#1A1A1A"
```

**Creating Templates:**
1. Design template in image editor (1080x1350px)
2. Save as PNG in `templates/` folder
3. Configure text areas in YAML
4. Test with sample content

## 🔄 Server Reconfiguration

### Adding New News Sources

1. **Research the news site:**
   - Find RSS feed URL
   - Identify CSS selectors for content
   - Test article pages

2. **Add configuration:**
   ```yaml
   # config/news_sources.yaml
   new_source:
     name: "New Source Name"
     base_url: "https://newssite.com"
     rss_feeds: ["https://newssite.com/feed.xml"]
     selectors:
       headline: "h1.article-title"
       content: ".article-content"
       image: ".hero-image img"
       author: ".byline"
       date: ".publish-date"
     enabled: true
   ```

3. **Test the scraper:**
   ```python
   from src.scrapers import UniversalScraper
   
   config = {
       'name': 'New Source',
       'base_url': 'https://newssite.com',
       # ... your configuration
   }
   
   scraper = UniversalScraper('new_source', config)
   stats = scraper.run_scraping_session()
   print(stats)
   ```

### Customizing Content Processing

**Modify Analysis Rules:**

```python
# src/processors/content_analyzer.py

def _custom_category_detection(self, content):
    """Add custom categorization logic"""
    if 'cryptocurrency' in content.lower():
        return 'technology'
    elif 'climate change' in content.lower():
        return 'environment'
    # ... add more rules
    
def _custom_importance_scoring(self, article):
    """Add custom importance scoring"""
    score = 0.5  # Base score
    
    # Boost breaking news
    if 'breaking' in article.headline.lower():
        score += 0.3
        
    # Boost local news
    if any(city in article.content.lower() for city in ['toronto', 'vancouver', 'montreal']):
        score += 0.2
        
    return min(score, 1.0)
```

**Customize Caption Generation:**

```python
# src/processors/caption_generator.py

def _custom_hashtag_rules(self, content, category):
    """Add custom hashtag generation"""
    hashtags = set()
    
    # Category-specific hashtags
    if category == 'politics':
        hashtags.update(['#CanadianPolitics', '#Parliament'])
    elif category == 'technology':
        hashtags.update(['#TechNews', '#Innovation'])
        
    # Content-based hashtags
    if 'election' in content.lower():
        hashtags.add('#Election2024')
        
    return list(hashtags)
```

### Modifying Publishing Behavior

**Custom Scheduling:**

```python
# src/publishers/scheduler.py

def _custom_optimal_times(self, day_of_week, category):
    """Define custom optimal posting times"""
    
    # Weekend schedules
    if day_of_week in [5, 6]:  # Saturday, Sunday
        return ['10:00', '14:00', '19:00']
    
    # Weekday schedules by category
    if category == 'breaking':
        return ['08:00', '12:00', '17:00', '20:00']
    elif category == 'business':
        return ['09:00', '12:00', '15:00']
    
    # Default schedule
    return ['09:00', '12:00', '15:00', '18:00', '21:00']
```

**Custom Content Filtering:**

```python
# src/publishers/instagram_publisher.py

def _custom_content_filter(self, post):
    """Add custom content filtering"""
    
    # Skip posts with certain keywords
    blocked_keywords = ['controversial_topic', 'sensitive_subject']
    if any(keyword in post.caption.lower() for keyword in blocked_keywords):
        return False
        
    # Require minimum engagement potential
    if post.importance_score < 0.6:
        return False
        
    return True
```

## 🔄 Runtime Reconfiguration

### Hot-Reload Configuration

```python
# Reload configuration without restarting
from src.config import config
config.reload()

# Reload specific scrapers
server.scrapers = server._initialize_scrapers()
```

### Dynamic Source Management

```python
# Add source at runtime
new_source_config = {
    'name': 'Breaking News Source',
    'base_url': 'https://breakingnews.com',
    'rss_feeds': ['https://breakingnews.com/rss'],
    'selectors': {'headline': 'h1', 'content': '.content'},
    'enabled': True
}

# Add to server
server.scrapers['breaking_news'] = UniversalScraper('breaking_news', new_source_config)
```

### Environment-Specific Configuration

**Development (`config/dev.yaml`):**
```yaml
instagram:
  posting:
    max_posts_per_day: 1
    min_interval_hours: 8
  safety:
    rate_limit_delay: 60
    
logging:
  level: DEBUG
  console: true
```

**Production (`config/prod.yaml`):**
```yaml
instagram:
  posting:
    max_posts_per_day: 5
    min_interval_hours: 3
  safety:
    rate_limit_delay: 30
    
logging:
  level: INFO
  console: false
```

## 🔧 Advanced Configuration

### Database Configuration

```python
# config/database.py
DATABASE_CONFIGS = {
    'development': {
        'url': 'sqlite:///dev_news.db',
        'echo': True
    },
    'production': {
        'url': 'postgresql://user:pass@localhost/news_instagram',
        'pool_size': 10,
        'max_overflow': 20
    }
}
```

### AI Service Configuration

```yaml
# config/ai_services.yaml
ai:
  content_analysis:
    primary: 'openai'      # or 'anthropic'
    fallback: 'anthropic'  # fallback service
    
  openai:
    model: 'gpt-3.5-turbo'
    max_tokens: 500
    temperature: 0.7
    
  anthropic:
    model: 'claude-3-sonnet'
    max_tokens: 500
```

### Monitoring Configuration

```yaml
# config/monitoring.yaml
monitoring:
  metrics:
    enabled: true
    collection_interval: 300  # seconds
    retention_days: 30
    
  alerts:
    email: admin@company.com
    thresholds:
      scraping_failure_rate: 0.3
      publishing_failure_rate: 0.1
      processing_delay_minutes: 60
```

## 🚀 Performance Tuning

### Scraping Performance

```yaml
# config/performance.yaml
scraping:
  concurrent_sources: 3      # Parallel source processing
  articles_per_batch: 50     # Batch size for processing
  request_delay: 2           # Delay between requests
  timeout: 30               # Request timeout
  retries: 3                # Number of retries
```

### Processing Performance

```yaml
processing:
  worker_threads: 4          # Concurrent processing threads
  batch_size: 20            # Articles per processing batch
  cache_ttl: 3600           # Cache time-to-live
  ai_request_limit: 100     # AI API requests per hour
```

This configuration guide provides comprehensive instructions for setting up and customizing every aspect of the News Instagram MCP server.
