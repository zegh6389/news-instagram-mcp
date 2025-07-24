# 🔐 GitHub Secrets Setup for Canadian Instagram MCP

This guide helps you set up the required GitHub repository secrets for the Canadian Instagram automation.

## 🚨 Required Secrets

You need to configure these secrets in your GitHub repository settings:

### Instagram Credentials
- `INSTAGRAM_USERNAME` - Your Instagram username
- `INSTAGRAM_PASSWORD` - Your Instagram password

### AI API Keys (at least one required)
- `OPENAI_API_KEY` - OpenAI API key for GPT models
- `ANTHROPIC_API_KEY` - Anthropic API key for Claude models  
- `GEMINI_API_KEY` - Google Gemini API key

## 📝 How to Add Secrets

### Step 1: Go to Repository Settings
1. Navigate to your GitHub repository: https://github.com/zegh6389/news-instagram-mcp
2. Click on **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**

### Step 2: Add Each Secret
For each secret listed above:

1. Click **New repository secret**
2. Enter the **Name** (exactly as shown above)
3. Enter the **Secret value**
4. Click **Add secret**

## 🔧 Detailed Setup Instructions

### Instagram Credentials

#### INSTAGRAM_USERNAME
```
Name: INSTAGRAM_USERNAME
Secret: your_instagram_username
```
⚠️ **Important**: Use just the username, not the full email or @username

#### INSTAGRAM_PASSWORD  
```
Name: INSTAGRAM_PASSWORD
Secret: your_instagram_password
```
⚠️ **Security Note**: This is stored securely by GitHub and never exposed in logs

### AI API Keys

#### OpenAI API Key (Recommended)
```
Name: OPENAI_API_KEY  
Secret: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**How to get OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Log in to your OpenAI account
3. Click **Create new secret key**
4. Copy the key and add it as a secret

#### Anthropic API Key (Alternative)
```
Name: ANTHROPIC_API_KEY
Secret: sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**How to get Anthropic API Key:**
1. Go to https://console.anthropic.com/
2. Create an account or log in
3. Navigate to API Keys section
4. Generate a new API key

#### Google Gemini API Key (Alternative)
```
Name: GEMINI_API_KEY
Secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**How to get Gemini API Key:**
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click **Create API Key**
4. Copy the generated key

## ✅ Verification

After adding all secrets, you should see them listed in your repository secrets:

```
INSTAGRAM_USERNAME     ••••••••••••••••
INSTAGRAM_PASSWORD     ••••••••••••••••
OPENAI_API_KEY        ••••••••••••••••
ANTHROPIC_API_KEY     ••••••••••••••••
GEMINI_API_KEY        ••••••••••••••••
```

## 🧪 Test Your Setup

### Method 1: Manual Workflow
1. Go to **Actions** tab in your repository
2. Click **Manual Canadian Instagram Test**
3. Click **Run workflow**
4. Select "authentication" test type
5. Click **Run workflow**

### Method 2: Check Secrets in Code
The workflows will fail with clear error messages if secrets are missing or incorrect.

## 🔒 Security Best Practices

### Instagram Account Security
1. **Enable Two-Factor Authentication** (but disable for automation)
2. **Use a dedicated automation account** (recommended)
3. **Monitor login notifications** from Instagram
4. **Check security emails** regularly

### API Key Security
1. **Limit API key permissions** where possible
2. **Monitor API usage** for unexpected activity
3. **Rotate keys regularly** (every 3-6 months)
4. **Never share keys** outside of GitHub secrets

### GitHub Repository Security
1. **Keep repository private** if containing sensitive automation
2. **Limit repository access** to trusted collaborators
3. **Review workflow runs** regularly
4. **Monitor secret access** in audit logs

## 🚨 Troubleshooting

### Common Issues

#### "Secret not found" Error
- **Solution**: Check secret name spelling (case-sensitive)
- **Solution**: Ensure secret is added to correct repository

#### Instagram Authentication Failure
- **Solution**: Verify username/password are correct
- **Solution**: Check if account has 2FA enabled
- **Solution**: Ensure account isn't restricted

#### API Key Invalid
- **Solution**: Regenerate API key from provider
- **Solution**: Check API key format (should start with expected prefix)
- **Solution**: Verify API account has sufficient credits/quota

#### GitHub Actions Access
- **Solution**: Ensure repository has Actions enabled
- **Solution**: Check if organization has restrictions on secrets

### Debug Steps

1. **Check Workflow Logs**:
   - Go to Actions tab
   - Click on failed workflow run
   - Expand failed steps to see error messages

2. **Test Individual Components**:
   - Run authentication test first
   - Test content generation separately
   - Verify Instagram connection works

3. **Manual Verification**:
   - Try logging into Instagram manually
   - Test API keys with simple requests
   - Verify all services are accessible

## 📞 Getting Help

If you continue having issues:

1. **Check Repository Issues**: Look for similar problems
2. **Review Documentation**: Read CANADIAN_AUTH_GUIDE.md
3. **Test Locally**: Run scripts on your local machine first
4. **Monitor Instagram**: Watch for security notifications

## 🔄 Regular Maintenance

### Monthly Tasks:
- [ ] Verify all secrets are still valid
- [ ] Check API key usage and limits
- [ ] Review Instagram account security
- [ ] Test authentication manually

### When Instagram Updates:
- [ ] Check if authentication method changed
- [ ] Update user agent strings if needed
- [ ] Verify device profiles still work
- [ ] Test automation after major Instagram updates

---

**Remember**: Keep your secrets secure and never commit them to your repository code!
