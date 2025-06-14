#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title scrapeDocs
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 🌐
# @raycast.argument1 { "type": "text", "placeholder": "Base URL (e.g. https://firebase.google.com)" }

# Documentation:
# @raycast.description scrape and format website documentation as txt file
# @raycast.author jos_
# @raycast.authorURL https://raycast.com/jos_

# Extract domain name from URL for file name
DOMAIN=$(echo "$1" | sed -E 's#https?://([^/]+).*#\1#' | tr '.' '_')
OUTPUT_DIR=~/Documents/documentation

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "Scraping documentation from: $1"
echo "Saving to: $OUTPUT_DIR/${DOMAIN}.txt"

# Run the scraper with the provided arguments
cd ~/code/scripts
python3 doc_scraper.py "$1" "$OUTPUT_DIR/${DOMAIN}"

# Open the output file in the default text editor
open "$OUTPUT_DIR/${DOMAIN}.txt"

# Open the folder in Finder
open "$OUTPUT_DIR" 
