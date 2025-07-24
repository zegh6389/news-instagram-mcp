# Canadian Instagram Authentication Setup Script for Windows PowerShell
# Run this script from your project directory

param(
    [string]$Username = "",
    [string]$Password = ""
)

Write-Host "🍁 Canadian Instagram Authentication Setup" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Location: Milton, Ontario, Canada" -ForegroundColor Cyan
Write-Host "🕐 Timezone: America/Toronto (Eastern Time)" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python detected: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python first." -ForegroundColor Red
    exit 1
}

# Check if we're in the right directory
if (-not (Test-Path "requirements.txt")) {
    Write-Host "❌ requirements.txt not found. Please run this script from the project root directory." -ForegroundColor Red
    exit 1
}

Write-Host "📦 Installing required Python packages..." -ForegroundColor Yellow
try {
    python -m pip install -r requirements.txt
    Write-Host "✅ Packages installed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install packages. Please check your Python/pip installation." -ForegroundColor Red
    exit 1
}

# Create sessions directory
if (-not (Test-Path "sessions")) {
    New-Item -ItemType Directory -Name "sessions" | Out-Null
    Write-Host "📁 Created sessions directory" -ForegroundColor Green
}

# Get Instagram credentials
if ($Username -eq "") {
    $Username = Read-Host "Enter your Instagram username"
}

if ($Password -eq "") {
    $securePassword = Read-Host "Enter your Instagram password" -AsSecureString
    $Password = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword))
}

# Create .env file
$envContent = @"
# Instagram Credentials for Canadian Authentication
INSTAGRAM_USERNAME=$Username
INSTAGRAM_PASSWORD=$Password

# Canadian Location Context
LOCATION_CITY=Milton
LOCATION_PROVINCE=Ontario
LOCATION_COUNTRY=Canada
LOCATION_TIMEZONE=America/Toronto

# Instagram Session Settings
INSTAGRAM_SESSION_FILE=sessions/${Username}_session.json

# Rate Limiting (Conservative for new accounts)
MAX_POSTS_PER_DAY=3
POST_SCHEDULE_INTERVAL=14400
REQUEST_DELAY=5
MAX_RETRIES=3

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/canadian_instagram.log
"@

$envContent | Out-File -FilePath ".env" -Encoding UTF8
Write-Host "📝 Created .env file with Canadian settings" -ForegroundColor Green

# Create logs directory
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Name "logs" | Out-Null
    Write-Host "📁 Created logs directory" -ForegroundColor Green
}

Write-Host ""
Write-Host "🔐 Starting Canadian Instagram authentication..." -ForegroundColor Yellow
Write-Host ""

# Run the Canadian authentication script
try {
    python setup_canadian_auth.py
    $authResult = $LASTEXITCODE
    
    if ($authResult -eq 0) {
        Write-Host ""
        Write-Host "🎉 SUCCESS! Canadian Instagram authentication completed!" -ForegroundColor Green
        Write-Host ""
        Write-Host "🚀 Next Steps:" -ForegroundColor Cyan
        Write-Host "1. Test your authentication: python test_canadian_auth.py" -ForegroundColor White
        Write-Host "2. Run a test post: python deploy/manual_automation.py" -ForegroundColor White
        Write-Host "3. Set up automated posting with GitHub Actions" -ForegroundColor White
        Write-Host ""
        Write-Host "📋 Important Notes:" -ForegroundColor Yellow
        Write-Host "• Your session is saved for Milton, Ontario, Canada" -ForegroundColor White
        Write-Host "• Instagram now recognizes this location as trusted" -ForegroundColor White
        Write-Host "• Run from the same network/device for best results" -ForegroundColor White
        Write-Host "• Monitor logs for any authentication issues" -ForegroundColor White
        
    } else {
        Write-Host ""
        Write-Host "❌ Authentication failed. Please check the troubleshooting guide." -ForegroundColor Red
        Write-Host ""
        Write-Host "📋 Common Solutions:" -ForegroundColor Yellow
        Write-Host "1. Log into Instagram manually from this browser/device first" -ForegroundColor White
        Write-Host "2. Check your email for Instagram security notifications" -ForegroundColor White
        Write-Host "3. Ensure your account isn't restricted or suspended" -ForegroundColor White
        Write-Host "4. Wait 24 hours and try again if recently blocked" -ForegroundColor White
        Write-Host "5. Read CANADIAN_AUTH_GUIDE.md for detailed instructions" -ForegroundColor White
    }
    
} catch {
    Write-Host "❌ Error running authentication script: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📖 For detailed troubleshooting, see CANADIAN_AUTH_GUIDE.md" -ForegroundColor Cyan
Write-Host ""
