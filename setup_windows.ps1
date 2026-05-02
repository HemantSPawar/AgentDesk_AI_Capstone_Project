$ErrorActionPreference = "Stop"

Write-Host "AgentDesk AI - Windows setup" -ForegroundColor Cyan
Write-Host "This script prepares Python, virtual environment, dependencies, and .env." -ForegroundColor Cyan

$pythonCommand = Get-Command python -ErrorAction SilentlyContinue

if (-not $pythonCommand) {
    Write-Host "Python was not found. Installing Python 3.14 with winget..." -ForegroundColor Yellow
    winget install --id Python.Python.3.14 -e
    Write-Host "Python installed. Close and reopen this terminal, then run this script again." -ForegroundColor Yellow
    exit 0
}

Write-Host "Python found:" -ForegroundColor Green
python --version

if (-not (Test-Path ".venv")) {
    Write-Host "Creating root virtual environment..." -ForegroundColor Cyan
    python -m venv .venv
} else {
    Write-Host "Root virtual environment already exists. Reusing .venv." -ForegroundColor Green
}

$venvPython = ".\.venv\Scripts\python.exe"

Write-Host "Upgrading pip..." -ForegroundColor Cyan
& $venvPython -m pip install --upgrade pip

Write-Host "Installing course dependencies from root requirements.txt..." -ForegroundColor Cyan
& $venvPython -m pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    Write-Host "Creating root .env from .env.example..." -ForegroundColor Cyan
    Copy-Item ".env.example" ".env"
} else {
    Write-Host "Root .env already exists. Keeping existing file." -ForegroundColor Green
}

Write-Host ""
Write-Host "Setup complete." -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Open .env and add your OPENAI_API_KEY."
Write-Host "2. Activate the environment:"
Write-Host "   .\.venv\Scripts\Activate.ps1"
Write-Host "3. Run Chapter 2:"
Write-Host "   cd chapter_02_project_setup"
Write-Host "   python app.py"
