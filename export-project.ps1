<#
.SYNOPSIS
    Export Sentiment Analysis Triage Project to ZIP Archive

.DESCRIPTION
    Creates a timestamped ZIP archive of the entire sentiment-analysis-triage project,
    excluding unnecessary files like .git, __pycache__, venv, node_modules, etc.

.PARAMETER OutputDir
    Directory where the ZIP file will be created. Defaults to parent directory.

.EXAMPLE
    .\export-project.ps1
    Creates a ZIP file in the parent directory with timestamp

.EXAMPLE
    .\export-project.ps1 -OutputDir "C:\Exports"
    Creates a ZIP file in the specified directory

.NOTES
    Author: Sentiment Analysis Triage Team
    Date: 2026-05-17
#>

param(
    [string]$OutputDir = ".."
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Get script directory (project root)
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectName = Split-Path -Leaf $ProjectRoot

# Generate timestamp for filename
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$ZipFileName = "${ProjectName}_export_${Timestamp}.zip"
$ZipFilePath = Join-Path $OutputDir $ZipFileName

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Sentiment Analysis Triage - Project Export" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Files and directories to exclude
$ExcludePatterns = @(
    ".git",
    ".gitignore",
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".Python",
    "venv",
    "env",
    "ENV",
    "node_modules",
    ".vscode",
    ".idea",
    "*.log",
    ".DS_Store",
    "Thumbs.db",
    ".env",
    "*.swp",
    "*.swo",
    "*~",
    ".pytest_cache",
    ".coverage",
    "htmlcov",
    "dist",
    "build",
    "*.egg-info"
)

Write-Host "Project Root: $ProjectRoot" -ForegroundColor Yellow
Write-Host "Output File: $ZipFilePath" -ForegroundColor Yellow
Write-Host ""

# Create temporary directory for staging
$TempDir = Join-Path $env:TEMP "sentiment_export_$Timestamp"
$StagingDir = Join-Path $TempDir $ProjectName

Write-Host "Creating staging directory..." -ForegroundColor Green
New-Item -ItemType Directory -Path $StagingDir -Force | Out-Null

# Function to check if path should be excluded
function Should-Exclude {
    param([string]$Path)
    
    foreach ($Pattern in $ExcludePatterns) {
        if ($Path -like "*$Pattern*") {
            return $true
        }
    }
    return $false
}

# Copy files to staging directory
Write-Host "Copying project files..." -ForegroundColor Green
$FileCount = 0
$TotalSize = 0

Get-ChildItem -Path $ProjectRoot -Recurse -File | ForEach-Object {
    $RelativePath = $_.FullName.Substring($ProjectRoot.Length + 1)
    
    if (-not (Should-Exclude $RelativePath)) {
        $DestPath = Join-Path $StagingDir $RelativePath
        $DestDir = Split-Path -Parent $DestPath
        
        if (-not (Test-Path $DestDir)) {
            New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
        }
        
        Copy-Item -Path $_.FullName -Destination $DestPath -Force
        $FileCount++
        $TotalSize += $_.Length
        
        if ($FileCount % 10 -eq 0) {
            Write-Host "  Copied $FileCount files..." -ForegroundColor Gray
        }
    }
}

Write-Host "  Total files copied: $FileCount" -ForegroundColor Green
Write-Host "  Total size: $([math]::Round($TotalSize / 1MB, 2)) MB" -ForegroundColor Green
Write-Host ""

# Create ZIP archive
Write-Host "Creating ZIP archive..." -ForegroundColor Green

# Ensure output directory exists
$OutputDirPath = Resolve-Path $OutputDir -ErrorAction SilentlyContinue
if (-not $OutputDirPath) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
    $OutputDirPath = Resolve-Path $OutputDir
}

# Remove existing ZIP if it exists
if (Test-Path $ZipFilePath) {
    Remove-Item $ZipFilePath -Force
}

# Create ZIP using .NET compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($TempDir, $ZipFilePath, 'Optimal', $false)

# Clean up staging directory
Write-Host "Cleaning up temporary files..." -ForegroundColor Green
Remove-Item -Path $TempDir -Recurse -Force

# Get final ZIP file info
$ZipInfo = Get-Item $ZipFilePath
$ZipSizeMB = [math]::Round($ZipInfo.Length / 1MB, 2)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Export Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Export Summary:" -ForegroundColor Yellow
Write-Host "  Files exported: $FileCount" -ForegroundColor White
Write-Host "  Original size: $([math]::Round($TotalSize / 1MB, 2)) MB" -ForegroundColor White
Write-Host "  ZIP file size: $ZipSizeMB MB" -ForegroundColor White
Write-Host "  Compression ratio: $([math]::Round((1 - ($ZipInfo.Length / $TotalSize)) * 100, 1))%" -ForegroundColor White
Write-Host ""
Write-Host "ZIP file location:" -ForegroundColor Yellow
Write-Host "  $ZipFilePath" -ForegroundColor White
Write-Host ""
Write-Host "Excluded patterns:" -ForegroundColor Yellow
$ExcludePatterns | ForEach-Object { Write-Host "  - $_" -ForegroundColor Gray }
Write-Host ""

# Open file explorer to show the ZIP file
Write-Host "Opening file location..." -ForegroundColor Green
explorer.exe "/select,$ZipFilePath"

Write-Host ""
Write-Host "Export completed successfully! ✓" -ForegroundColor Green

# Made with Bob
