# Documentation Scraper

A powerful and configurable web scraper designed to extract documentation from various documentation frameworks and websites. The scraper is optimized for RAG (Retrieval-Augmented Generation) applications and supports multiple documentation frameworks including Docusaurus, Sphinx, MkDocs, GitBook, and more.

## Features

- 🚀 Framework-aware scraping for popular documentation systems
- ⚡ Configurable selectors and extraction rules
- 🔄 Automatic retry mechanism with exponential backoff
- 🛡️ Respects robots.txt and rate limiting
- 📝 Smart content chunking for RAG applications
- 🎯 Customizable exclusion patterns
- 📊 Detailed logging and progress tracking
- 💾 JSON output with metadata

## Requirements

```bash
pip install selenium beautifulsoup4 requests backoff
```

You'll also need Chrome/Chromium browser installed on your system.

## Usage

Basic usage:
```bash
python doc_scraper.py https://docs.example.com
```

With custom configuration:
```bash
python doc_scraper.py https://docs.example.com doc_config.json
```

## Configuration

The scraper can be customized using a JSON configuration file. Here's what you can configure:

- `max_pages`: Maximum number of pages to scrape
- `max_retries`: Maximum number of retry attempts for failed requests
- `chunk_size`: Maximum size of content chunks
- `rate_limit`: Rate limiting settings
- `selectors`: CSS selectors for content extraction
- `exclude_patterns`: URL patterns to exclude
- `framework_specific`: Framework-specific selectors and settings

Example configuration for different frameworks is provided in `doc_config.json`.

## Output

The scraper creates a `scraped_docs` directory and saves the extracted content in JSON files with the following structure:

```json
{
    "metadata": {
        "source_url": "https://docs.example.com",
        "scrape_date": "2024-03-21 10:30:00",
        "total_chunks": 42,
        "config_used": { ... }
    },
    "chunks": [
        "chunk1 content with metadata...",
        "chunk2 content with metadata...",
        ...
    ]
}
```

## Supported Documentation Frameworks

- Docusaurus
- Sphinx
- MkDocs
- GitBook
- ReadMe.io
- Generic documentation sites

## Best Practices

1. Start with the default configuration and adjust as needed
2. Use framework-specific configurations when available
3. Respect website's rate limiting and robots.txt
4. Monitor the logs for any issues
5. Test with a small number of pages first

## Error Handling

The scraper includes robust error handling:

- Automatic retry for transient failures
- Exponential backoff
- Detailed error logging
- Graceful degradation

## Contributing

Feel free to submit issues and enhancement requests! 