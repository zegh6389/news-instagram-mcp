# 🚀 First Post Setup & Testing Guide

## 📋 Prerequisites Checklist

Before we can post your first Instagram post, you need to provide these items:

### 1. ✅ Instagram Account Setup
- **Instagram Business or Creator Account** (required for API access)
- **Username and Password**
- **Two-Factor Authentication** (2FA) - you may need to disable temporarily or use app-specific password

### 2. ⚠️ AI Services (Optional but Recommended)
- **OpenAI API Key** (for content analysis and caption generation)
- **Anthropic API Key** (alternative to OpenAI)

Note: The system can work without AI services but will use basic content processing.

### 3. 📁 File Setup
- Create `.env` file with your credentials
- Ensure configuration files are properly set

## 🛠️ Step-by-Step Setup

### Step 1: Create Environment File

```bash
# Copy the example file
cp .env.example .env
```

Then edit `.env` with your actual credentials:

```env
# REQUIRED: Instagram credentials
INSTAGRAM_USERNAME=your_actual_username
INSTAGRAM_PASSWORD=your_actual_password

# OPTIONAL: AI services (for better content processing)
OPENAI_API_KEY=sk-your-openai-key-here
# OR
ANTHROPIC_API_KEY=your-anthropic-key-here

# Keep these defaults for testing
DATABASE_URL=sqlite:///news_instagram.db
LOG_LEVEL=DEBUG
MAX_POSTS_PER_DAY=1
```

### Step 2: Test System Components

Let's test each component to ensure everything works:

#### Test 1: Database Setup
```bash
python -c "from src.database import DatabaseManager; db = DatabaseManager(); print('Database OK')"
```

#### Test 2: News Scraping
```bash
python -c "
from src.scrapers import CBCScraper
from src.config import config
scraper = CBCScraper('cbc', config.get_news_sources()['cbc'])
articles = scraper.scrape_rss_feeds()
print(f'Found {len(articles)} articles')
"
```

#### Test 3: Full Article Scraping
```bash
python -c "
from src.scrapers import CBCScraper
from src.config import config
scraper = CBCScraper('cbc', config.get_news_sources()['cbc'])
stats = scraper.run_scraping_session()
print(f'Scraping stats: {stats}')
"
```

#### Test 4: Content Analysis
```bash
python -c "
from src.processors import ContentAnalyzer
analyzer = ContentAnalyzer()
stats = analyzer.process_articles(limit=1)
print(f'Analysis stats: {stats}')
"
```

#### Test 5: Instagram Connection Test
```bash
python -c "
from src.publishers import InstagramPublisher
publisher = InstagramPublisher()
print('Instagram publisher initialized successfully')
"
```

### Step 3: Generate Your First Post

#### Option A: Using MCP Tools (Recommended)
```bash
python main.py
```

Then use these MCP commands in sequence:
1. `scrape_news` - Get latest articles
2. `analyze_content` - Process the articles  
3. `generate_post` - Create an Instagram post
4. `publish_post` - Post to Instagram

#### Option B: Manual Testing Script
```python
# test_first_post.py
from src.scrapers import CBCScraper
from src.processors import ContentAnalyzer, CaptionGenerator
from src.publishers import InstagramPublisher
from src.config import config
from src.database import DatabaseManager

def test_first_post():
    print("🔍 Step 1: Scraping news...")
    scraper = CBCScraper('cbc', config.get_news_sources()['cbc'])
    stats = scraper.run_scraping_session()
    print(f"✅ Scraped {stats['articles_scraped']} articles")
    
    print("\\n🧠 Step 2: Analyzing content...")
    analyzer = ContentAnalyzer()
    analysis_stats = analyzer.process_articles(limit=1)
    print(f"✅ Analyzed {analysis_stats.get('processed', 0)} articles")
    
    print("\\n📝 Step 3: Generating caption...")
    db = DatabaseManager()
    articles = db.get_recent_articles(hours=24, limit=1)
    
    if not articles:
        print("❌ No articles found!")
        return
        
    article = articles[0]
    caption_gen = CaptionGenerator()
    
    # Create a simple article dict for caption generation
    article_data = {
        'headline': article.headline,
        'summary': article.summary or article.content[:200]
    }
    
    analysis_data = {
        'keywords': article.keywords or ['news'],
        'category': article.category or 'general'
    }
    
    caption = caption_gen.generate_caption(article_data, analysis_data)
    print(f"✅ Generated caption: {caption[:100]}...")
    
    print("\\n📱 Step 4: Creating Instagram post...")
    # Here we would normally publish to Instagram
    # For testing, we'll just create the database record
    
    post_data = {
        'article_id': article.id,
        'caption': caption,
        'hashtags': '#news #canada #breaking',
        'template_used': 'feature',
        'status': 'draft'
    }
    
    post = db.save_instagram_post(post_data)
    print(f"✅ Created post {post.id}")
    
    print("\\n🎉 First post ready! To publish to Instagram:")
    print(f"   - Post ID: {post.id}")
    print(f"   - Article: {article.headline}")
    print(f"   - Caption length: {len(caption)} characters")
    
    return post

if __name__ == "__main__":
    test_first_post()
```

## 🔧 What You Need to Provide

### Minimum Required (for basic functionality):
1. **Instagram Username & Password**
2. **Instagram Business/Creator account**

### Recommended (for full functionality):
3. **OpenAI API Key** ($5-20/month depending on usage)
   - Get from: https://platform.openai.com/api-keys
   - Needed for: Smart content analysis, caption generation

### Optional Enhancements:
4. **Custom news sources** (if you want sources beyond CBC/Global News)
5. **Custom visual templates** (for branded post graphics)
6. **Custom hashtag strategies**

## 🎯 Expected First Post Workflow

1. **Scrape**: System finds latest news articles from CBC
2. **Analyze**: AI analyzes content for category, keywords, importance
3. **Generate**: Creates Instagram-optimized caption with hashtags
4. **Publish**: Posts to your Instagram account

## ⚠️ Safety Notes

- Start with `MAX_POSTS_PER_DAY=1` for testing
- Use `LOG_LEVEL=DEBUG` to see detailed operations
- Test posting will use your actual Instagram account
- Consider using a test Instagram account first

## 🐛 Common Issues & Solutions

### Instagram Login Issues:
- Ensure you have a Business/Creator account
- Try disabling 2FA temporarily
- Use app-specific password if available
- Check for suspicious login blocks

### No Articles Found:
- Check internet connection
- Verify news source URLs are accessible
- Check if RSS feeds are working

### AI API Issues:
- Verify API key is correct
- Check API quota/billing
- System will fallback to basic processing without AI

## 📞 Ready to Test?

Once you've provided:
1. ✅ Instagram credentials in `.env` file
2. ✅ (Optional) OpenAI API key
3. ✅ Confirmed Instagram account is Business/Creator type

We can run the test script and generate your first automated news post!

Let me know when you're ready, and I'll help you run the tests step by step.
