#!/bin/bash

################################################################################
# Sentiment Analysis Triage - Project Export Script
#
# Description:
#   Creates a timestamped ZIP archive of the entire sentiment-analysis-triage
#   project, excluding unnecessary files like .git, __pycache__, venv, etc.
#
# Usage:
#   ./export-project.sh [output_directory]
#
# Arguments:
#   output_directory - Optional. Directory where ZIP will be created.
#                      Defaults to parent directory (..)
#
# Examples:
#   ./export-project.sh
#   ./export-project.sh ~/exports
#   ./export-project.sh /tmp
#
# Author: Sentiment Analysis Triage Team
# Date: 2026-05-17
################################################################################

set -e  # Exit on error
set -u  # Exit on undefined variable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

# Get script directory (project root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="$(basename "$SCRIPT_DIR")"

# Output directory (default to parent directory)
OUTPUT_DIR="${1:-..}"

# Generate timestamp for filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ZIP_FILENAME="${PROJECT_NAME}_export_${TIMESTAMP}.zip"
ZIP_FILEPATH="${OUTPUT_DIR}/${ZIP_FILENAME}"

# Files and directories to exclude (for find command)
EXCLUDE_PATTERNS=(
    ".git"
    "__pycache__"
    "*.pyc"
    "*.pyo"
    "*.pyd"
    ".Python"
    "venv"
    "env"
    "ENV"
    "node_modules"
    ".vscode"
    ".idea"
    "*.log"
    ".DS_Store"
    "Thumbs.db"
    ".env"
    "*.swp"
    "*.swo"
    "*~"
    ".pytest_cache"
    ".coverage"
    "htmlcov"
    "dist"
    "build"
    "*.egg-info"
)

################################################################################
# Functions
################################################################################

print_header() {
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}Sentiment Analysis Triage - Project Export${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
}

print_info() {
    echo -e "${YELLOW}$1${NC}"
}

print_success() {
    echo -e "${GREEN}$1${NC}"
}

print_error() {
    echo -e "${RED}$1${NC}"
}

print_gray() {
    echo -e "${GRAY}$1${NC}"
}

# Build find exclude arguments
build_exclude_args() {
    local args=""
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        if [[ "$pattern" == *"*"* ]]; then
            # Pattern with wildcard
            args="$args -name '$pattern' -o"
        else
            # Directory or exact name
            args="$args -path '*/$pattern' -o -name '$pattern' -o"
        fi
    done
    # Remove trailing " -o"
    echo "${args% -o}"
}

# Format bytes to human readable
format_bytes() {
    local bytes=$1
    if [ $bytes -lt 1024 ]; then
        echo "${bytes}B"
    elif [ $bytes -lt 1048576 ]; then
        echo "$(awk "BEGIN {printf \"%.2f\", $bytes/1024}")KB"
    else
        echo "$(awk "BEGIN {printf \"%.2f\", $bytes/1048576}")MB"
    fi
}

################################################################################
# Main Script
################################################################################

print_header

# Check if zip command is available
if ! command -v zip &> /dev/null; then
    print_error "Error: 'zip' command not found. Please install zip utility."
    echo "  Ubuntu/Debian: sudo apt-get install zip"
    echo "  macOS: zip is pre-installed"
    echo "  CentOS/RHEL: sudo yum install zip"
    exit 1
fi

print_info "Project Root: $SCRIPT_DIR"
print_info "Output File: $ZIP_FILEPATH"
echo ""

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Create temporary directory for staging
TEMP_DIR=$(mktemp -d)
STAGING_DIR="${TEMP_DIR}/${PROJECT_NAME}"

print_success "Creating staging directory..."
mkdir -p "$STAGING_DIR"

# Build exclude arguments for find
EXCLUDE_ARGS=$(build_exclude_args)

print_success "Copying project files..."
FILE_COUNT=0
TOTAL_SIZE=0

# Copy files while excluding patterns
cd "$SCRIPT_DIR"
while IFS= read -r -d '' file; do
    # Get relative path
    rel_path="${file#./}"
    
    # Skip if matches exclude pattern
    skip=false
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        if [[ "$rel_path" == *"$pattern"* ]]; then
            skip=true
            break
        fi
    done
    
    if [ "$skip" = false ]; then
        # Create directory structure in staging
        dest_file="${STAGING_DIR}/${rel_path}"
        dest_dir=$(dirname "$dest_file")
        mkdir -p "$dest_dir"
        
        # Copy file
        cp "$file" "$dest_file"
        
        # Update counters
        FILE_COUNT=$((FILE_COUNT + 1))
        file_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
        TOTAL_SIZE=$((TOTAL_SIZE + file_size))
        
        # Progress indicator
        if [ $((FILE_COUNT % 10)) -eq 0 ]; then
            print_gray "  Copied $FILE_COUNT files..."
        fi
    fi
done < <(find . -type f -print0)

print_success "  Total files copied: $FILE_COUNT"
print_success "  Total size: $(format_bytes $TOTAL_SIZE)"
echo ""

# Create ZIP archive
print_success "Creating ZIP archive..."
cd "$TEMP_DIR"

# Remove existing ZIP if it exists
[ -f "$ZIP_FILEPATH" ] && rm -f "$ZIP_FILEPATH"

# Create ZIP with optimal compression
zip -r -q -9 "$ZIP_FILEPATH" "$PROJECT_NAME"

# Clean up staging directory
print_success "Cleaning up temporary files..."
rm -rf "$TEMP_DIR"

# Get final ZIP file info
ZIP_SIZE=$(stat -f%z "$ZIP_FILEPATH" 2>/dev/null || stat -c%s "$ZIP_FILEPATH" 2>/dev/null)
COMPRESSION_RATIO=$(awk "BEGIN {printf \"%.1f\", (1 - ($ZIP_SIZE / $TOTAL_SIZE)) * 100}")

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${GREEN}Export Complete!${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
print_info "Export Summary:"
echo "  Files exported: $FILE_COUNT"
echo "  Original size: $(format_bytes $TOTAL_SIZE)"
echo "  ZIP file size: $(format_bytes $ZIP_SIZE)"
echo "  Compression ratio: ${COMPRESSION_RATIO}%"
echo ""
print_info "ZIP file location:"
echo "  $ZIP_FILEPATH"
echo ""
print_info "Excluded patterns:"
for pattern in "${EXCLUDE_PATTERNS[@]}"; do
    print_gray "  - $pattern"
done
echo ""

# Make the ZIP file readable
chmod 644 "$ZIP_FILEPATH"

print_success "Export completed successfully! ✓"
echo ""

# Offer to open file location (macOS only)
if [[ "$OSTYPE" == "darwin"* ]]; then
    read -p "Open file location in Finder? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open -R "$ZIP_FILEPATH"
    fi
fi

exit 0

# Made with Bob
