# PowerShell Script to Download and Install Prerequisites for brat

# Ensure PowerShell is running with administrative privileges
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script must be run as Administrator!" -ForegroundColor Red
    exit
}

# Check if Python is installed
Write-Host "Checking for Python installation..." -ForegroundColor Cyan
$pythonVersion = python --version 2>$null
if (-not $?) {
    Write-Host "Python is not installed. Downloading and installing Python..." -ForegroundColor Yellow
    $pythonInstallerUrl = "https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe"
    $installerPath = "$env:TEMP\python-installer.exe"
    Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $installerPath -UseBasicParsing
    Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    Remove-Item -Path $installerPath

    # Verify Python installation
    $pythonVersion = python --version 2>$null
    if (-not $?) {
        Write-Host "Python installation failed. Please install Python manually." -ForegroundColor Red
        exit
    } else {
        Write-Host "Python installed successfully: $pythonVersion" -ForegroundColor Green
    }
} else {
    Write-Host "Python is already installed: $pythonVersion" -ForegroundColor Green
}

# Update pip to the latest version
Write-Host "Updating pip to the latest version..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# Check if requirements.txt exists in the current directory
if (-Not (Test-Path "requirements.txt")) {
    Write-Host "Error: requirements.txt not found in the current directory." -ForegroundColor Red
    exit
}

# Install required Python libraries
Write-Host "Installing Python libraries from requirements.txt..." -ForegroundColor Cyan
try {
    python -m pip install -r requirements.txt
    Write-Host "All Python libraries installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Failed to install Python libraries." -ForegroundColor Red
    exit
}

# Install NLTK tokenizer data
Write-Host "Downloading NLTK tokenizer data..." -ForegroundColor Cyan
try {
    python -c "import nltk; nltk.download('punkt')"
    Write-Host "NLTK data installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Failed to download NLTK data." -ForegroundColor Red
}

# Check and install necessary system dependencies (optional for TTS)
Write-Host "Checking for TTS system dependencies..." -ForegroundColor Cyan
if ($IsWindows) {
    Write-Host "No additional dependencies required for Windows." -ForegroundColor Green
} else {
    Write-Host "Note: Additional dependencies may be required for text-to-speech on Linux or macOS." -ForegroundColor Yellow
}

Write-Host "All prerequisites are installed! You can now run brat." -ForegroundColor Green
