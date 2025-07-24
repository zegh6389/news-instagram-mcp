# GitHub Actions Deployment Guide

## 🚀 Quick Setup Steps

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Add GitHub Actions automation"
git remote add origin https://github.com/YOUR_USERNAME/news-instagram-mcp.git
git push -u origin main
```

### 2. Set GitHub Repository Secrets
Go to: **Repository → Settings → Secrets and variables → Actions**

Add these secrets:
- `INSTAGRAM_USERNAME` = your_instagram_username  
- `INSTAGRAM_PASSWORD` = your_instagram_password
- `GEMINI_API_KEY` = your_gemini_api_key (optional)
- `DATABASE_URL` = sqlite:///tmp/news_instagram.db

### 3. Enable GitHub Actions
- Go to **Actions** tab in your repository
- Enable workflows if prompted
- Your automation will start running daily at 6:00 AM UTC

## 📅 Automation Features

### Daily Automation (Automatic)
- **Runs**: Every day at 6:00 AM UTC
- **Does**: Scrapes news → Generates 3 posts → Publishes 1 immediately
- **Logs**: Available in Actions tab for 30 days

### Manual Automation (On-Demand)  
- **Trigger**: Actions → Manual News Automation → Run workflow
- **Options**: Choose post count, template type, immediate publish
- **Use Case**: Test or create content outside daily schedule

## 🎯 What Happens Daily

1. **6:00 AM UTC**: GitHub Actions triggers
2. **Scrape News**: Gets latest articles from CBC & Global News  
3. **Analyze Content**: Categorizes and processes articles
4. **Generate Posts**: Creates 3 Instagram posts with different templates
5. **Publish**: Posts 1 immediately with daily news caption
6. **Logs**: Detailed results saved and viewable in GitHub

## 📊 Monitoring

### View Results
- **GitHub Actions Tab**: See all runs and logs
- **Artifacts**: Download detailed logs for each run
- **Commit Comments**: Quick status updates on repository

### Success Metrics
- Articles scraped per day
- Posts generated successfully  
- Publishing success rate
- Error tracking and alerts

## 🔧 Customization

### Change Schedule
Edit `.github/workflows/daily-automation.yml`:
```yaml
schedule:
  - cron: '0 14 * * *'  # 2 PM UTC instead
```

### Adjust Post Count
Edit `deploy/github_automation.py`:
```python
templates = ['breaking', 'analysis', 'feature', 'general']  # Add more
```

### Timezone Considerations
- GitHub Actions uses UTC time
- 6:00 AM UTC = 2:00 AM ET / 11:00 PM PT (previous day)
- Adjust cron schedule based on your target audience

## 🎉 You're All Set!

Once you push to GitHub and add the secrets, your news automation will:
- ✅ Run automatically every day
- ✅ Handle errors gracefully  
- ✅ Provide detailed logging
- ✅ Cost $0 (within GitHub free tier)
- ✅ Require zero maintenance

Your Instagram account will start getting fresh news content daily! 🚀
