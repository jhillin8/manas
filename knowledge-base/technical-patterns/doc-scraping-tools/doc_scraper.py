#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import sys
import os
from urllib.parse import urljoin, urlparse
import time
import random
import logging
from selenium.common.exceptions import TimeoutException, WebDriverException, StaleElementReferenceException
from typing import List, Set, Tuple, Dict, Optional
import requests
from urllib.robotparser import RobotFileParser
import json
from pathlib import Path
import backoff

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RetryableError(Exception):
    """Custom exception for errors that should trigger a retry"""
    pass

class DocumentationScraper:
    def __init__(self, start_url: str, config: Optional[Dict] = None):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.visited_urls: Set[str] = set()
        self.config = self._load_config(config)
        self.robots_parser = self._setup_robots_parser()
        self.browser = self.init_browser()
        self.output_dir = self._setup_output_dir()
        self.rate_limiter = RateLimiter(
            requests_per_second=self.config['rate_limit']['requests_per_second']
        )

    def _load_config(self, config: Optional[Dict] = None) -> Dict:
        """Load and merge configuration with defaults"""
        default_config = {
            'max_pages': 100,
            'max_retries': 3,
            'chunk_size': 1500,
            'rate_limit': {
                'requests_per_second': 1
            },
            'selectors': {
                'content': [
                    'article', 'main', '[role="main"]', '.content',
                    '.documentation', '.markdown-body', '#content',
                    '.docs-content', '.post-content'
                ],
                'title': [
                    'h1', 'article h1', '.article-title', '.doc-title',
                    '[role="heading"]'
                ],
                'description': [
                    '.lead', '.introduction', '.summary', '.description',
                    'article p:first-of-type'
                ]
            },
            'exclude_patterns': [
                '/search', '/login', '/signup', '/download',
                '.pdf', '.zip', '.exe', '.dmg',
                'javascript:', 'mailto:', 'tel:',
                '/blog/', '/pricing/', '/enterprise/'
            ]
        }
        
        if config:
            # Deep merge the provided config with defaults
            return self._deep_merge(default_config, config)
        return default_config

    def _deep_merge(self, dict1: Dict, dict2: Dict) -> Dict:
        """Deep merge two dictionaries"""
        result = dict1.copy()
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def _setup_robots_parser(self) -> RobotFileParser:
        """Setup and return robots.txt parser"""
        parser = RobotFileParser()
        robots_url = urljoin(self.start_url, '/robots.txt')
        try:
            parser.set_url(robots_url)
            parser.read()
        except Exception as e:
            logger.warning(f"Could not read robots.txt: {e}")
        return parser

    def _setup_output_dir(self) -> Path:
        """Setup output directory for scraped content"""
        output_dir = Path(os.path.dirname(os.path.abspath(__file__))) / 'scraped_docs'
        output_dir.mkdir(exist_ok=True)
        return output_dir

    @backoff.on_exception(
        backoff.expo,
        RetryableError,
        max_tries=3,
        max_time=30
    )
    def extract_content(self, url: str) -> Tuple[str, str, str]:
        """Extract content with retry mechanism"""
        try:
            self.rate_limiter.wait()
            
            if not self.robots_parser.can_fetch("*", url):
                logger.warning(f"URL {url} is disallowed by robots.txt")
                return "", "", ""

            self.browser.get(url)
            
            # Wait for body and dynamic content
            WebDriverWait(self.browser, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Wait for content with multiple selectors
            for selector in self.config['selectors']['content']:
                try:
                    WebDriverWait(self.browser, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            # Handle dynamic content loading
            self._handle_dynamic_content()
            
            soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            
            title = self._extract_title(soup)
            description = self._extract_description(soup)
            content = self._extract_main_content(soup)
            
            return title, description, content
            
        except (TimeoutException, WebDriverException) as e:
            raise RetryableError(f"Retryable error occurred: {str(e)}")
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {str(e)}")
            return "", "", ""

    def _handle_dynamic_content(self):
        """Handle dynamic content loading with scroll and wait"""
        scroll_script = """
            return new Promise((resolve) => {
                let lastHeight = document.body.scrollHeight;
                let scrollAttempts = 0;
                const maxScrolls = 3;
                
                function scroll() {
                    window.scrollTo(0, document.body.scrollHeight);
                    setTimeout(() => {
                        let newHeight = document.body.scrollHeight;
                        if (newHeight > lastHeight && scrollAttempts < maxScrolls) {
                            lastHeight = newHeight;
                            scrollAttempts++;
                            scroll();
                        } else {
                            resolve();
                        }
                    }, 1000);
                }
                
                scroll();
            });
        """
        
        try:
            self.browser.execute_script(scroll_script)
            time.sleep(2)  # Additional wait for any final dynamic content
        except Exception as e:
            logger.warning(f"Error during dynamic content handling: {e}")

    def save_results(self, chunks: List[str], url: str):
        """Save results with metadata and chunks"""
        try:
            # Create a unique filename based on the domain and path
            parsed_url = urlparse(url)
            filename = f"{parsed_url.netloc.replace('.', '_')}_{int(time.time())}.json"
            output_file = self.output_dir / filename
            
            metadata = {
                "source_url": url,
                "scrape_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_chunks": len(chunks),
                "config_used": self.config
            }
            
            data = {
                "metadata": metadata,
                "chunks": chunks
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Results saved to: {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")

    def init_browser(self) -> webdriver.Chrome:
        """Initialize Chrome browser with optimized settings"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument(f'--window-size={random.randint(1024, 1920)},{random.randint(768, 1080)}')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        
        # Add additional options for modern web apps
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=IsolateOrigins,site-per-process')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Add additional preferences
        chrome_options.add_experimental_option('prefs', {
            'profile.default_content_settings.popups': 0,
            'download.default_directory': '/dev/null',
            'profile.content_settings.exceptions.automatic_downloads.*.setting': 1
        })
        
        browser = webdriver.Chrome(options=chrome_options)
        return browser

    def should_process_url(self, url: str) -> bool:
        """Determine if a URL should be processed based on configuration"""
        if not url:
            return False
            
        try:
            parsed_url = urlparse(url)
            if parsed_url.netloc != self.domain:
                return False
            
            # Check against exclude patterns from config
            url_without_fragment = url.split('#')[0]
            for pattern in self.config['exclude_patterns']:
                if pattern.lower() in url_without_fragment.lower():
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Error in should_process_url: {str(e)}")
            return False

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract title using configured selectors"""
        try:
            # Try configured title selectors
            for selector in self.config['selectors']['title']:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = self._clean_text(title_elem.get_text())
                    if title:
                        return title
            
            # Fallback to page title
            if soup.title:
                return self._clean_text(soup.title.string)
            
            return ""
        except Exception as e:
            logger.error(f"Error in _extract_title: {str(e)}")
            return ""

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract description using configured selectors"""
        try:
            # Try meta description
            meta_desc = soup.find('meta', {'name': ['description', 'Description']})
            if meta_desc:
                desc = self._clean_text(meta_desc.get('content', ''))
                if desc:
                    return desc
            
            # Try configured description selectors
            for selector in self.config['selectors']['description']:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    desc = self._clean_text(desc_elem.get_text())
                    if desc:
                        return desc
            
            return ""
        except Exception as e:
            logger.error(f"Error in _extract_description: {str(e)}")
            return ""

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content using configured selectors"""
        try:
            # Remove unwanted elements
            for unwanted in soup.select('nav, header, footer, .navigation, .sidebar, script, style, iframe, form'):
                unwanted.decompose()
            
            # Try configured content selectors
            for selector in self.config['selectors']['content']:
                content_elem = soup.select_one(selector)
                if content_elem:
                    # Further clean the content element
                    for unwanted in content_elem.select('nav, .sidebar, .toc, .table-of-contents, .navigation'):
                        unwanted.decompose()
                    
                    content = self._clean_text(content_elem.get_text())
                    if len(content) > 100:  # Only return if substantial content found
                        return content
            
            # Fallback: try to find the largest text block
            text_blocks = []
            for elem in soup.find_all(['div', 'section', 'article']):
                text = self._clean_text(elem.get_text())
                if len(text) > 100:  # Only consider substantial blocks
                    text_blocks.append((len(text), text))
            
            if text_blocks:
                return max(text_blocks, key=lambda x: x[0])[1]
            
            return ""
        except Exception as e:
            logger.error(f"Error in _extract_main_content: {str(e)}")
            return ""

    def _clean_text(self, text: str) -> str:
        """Clean text content"""
        if not text:
            return ""
        
        # Remove excessive whitespace while preserving paragraph breaks
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'\s{2,}', ' ', text)
        text = text.replace('\t', ' ')
        
        # Clean up common HTML artifacts
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&quot;', '"')
        text = text.replace('&apos;', "'")
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        
        # Clean up whitespace
        text = text.strip()
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        
        return text

    def extract_links(self, url: str) -> List[str]:
        """Extract and filter links from the page"""
        try:
            links = set()
            
            # Find all links in the page
            elements = self.browser.find_elements(By.TAG_NAME, "a")
            for element in elements:
                try:
                    href = element.get_attribute('href')
                    if href and self.should_process_url(href):
                        # Convert relative URLs to absolute
                        absolute_url = urljoin(url, href)
                        links.add(absolute_url)
                except (StaleElementReferenceException, WebDriverException):
                    continue
            
            # Sort links to prioritize documentation paths
            sorted_links = sorted(links, key=lambda x: (
                'docs' in x.lower() or 
                'documentation' in x.lower() or 
                'guide' in x.lower() or 
                'tutorial' in x.lower() or 
                'reference' in x.lower()
            ), reverse=True)
            
            return sorted_links
            
        except Exception as e:
            logger.error(f"Error extracting links from {url}: {str(e)}")
            return []

    def chunk_content(self, content: str, metadata: dict) -> List[str]:
        """Split content into chunks with metadata"""
        if not content:
            return []

        try:
            chunks = []
            current_chunk = []
            current_size = 0
            max_chunk_size = self.config['chunk_size']
            
            # Add metadata to each chunk
            metadata_str = "\n".join(f"{k}: {v}" for k, v in metadata.items())
            metadata_size = len(metadata_str)
            
            # Split content into sections based on headers and other markers
            section_markers = [
                r'^#{1,6}\s+',  # Markdown headers
                r'\n[-=]{3,}\n',    # Markdown underline headers
                r'^[A-Z][A-Za-z\s]{10,}(?:\n|\.|:)',  # Capitalized section titles
                r'\n\s*\d+\.\s+[A-Z]',  # Numbered sections
                r'\n\s*•\s+[A-Z]'   # Bullet points
            ]
            
            pattern = '|'.join(f'({marker})' for marker in section_markers)
            sections = re.split(pattern, content)
            
            # Filter out None and empty sections
            sections = [s for s in sections if s and s.strip()]
            
            for section in sections:
                section = section.strip()
                if not section:
                    continue
                
                # If section is too large, split into paragraphs
                if len(section) > max_chunk_size - metadata_size:
                    paragraphs = section.split('\n\n')
                    for para in paragraphs:
                        para = para.strip()
                        if not para:
                            continue
                        
                        # If paragraph is too large, split into sentences
                        if len(para) > max_chunk_size - metadata_size:
                            sentences = re.split(r'(?<=[.!?])\s+', para)
                            for sentence in sentences:
                                if current_size + len(sentence) + 1 > max_chunk_size - metadata_size:
                                    if current_chunk:
                                        chunks.append(metadata_str + "\n\n" + "\n".join(current_chunk))
                                    current_chunk = [sentence]
                                    current_size = len(sentence)
                                else:
                                    current_chunk.append(sentence)
                                    current_size += len(sentence) + 1
                        else:
                            if current_size + len(para) + 1 > max_chunk_size - metadata_size:
                                if current_chunk:
                                    chunks.append(metadata_str + "\n\n" + "\n".join(current_chunk))
                                current_chunk = [para]
                                current_size = len(para)
                            else:
                                current_chunk.append(para)
                                current_size += len(para) + 1
                else:
                    if current_size + len(section) + 1 > max_chunk_size - metadata_size:
                        if current_chunk:
                            chunks.append(metadata_str + "\n\n" + "\n".join(current_chunk))
                        current_chunk = [section]
                        current_size = len(section)
                    else:
                        current_chunk.append(section)
                        current_size += len(section) + 1
            
            if current_chunk:
                chunks.append(metadata_str + "\n\n" + "\n".join(current_chunk))
            
            return chunks
        except Exception as e:
            logger.error(f"Error in chunk_content: {str(e)}")
            return []

    def process_page(self, url: str) -> List[str]:
        """Process a single page and return content chunks"""
        if url in self.visited_urls:
            return []
            
        self.visited_urls.add(url)
        logger.info(f"Processing {url}")
        
        title, description, content = self.extract_content(url)
        if not content:
            return []
            
        metadata = {
            "url": url,
            "title": title,
            "description": description
        }
        
        chunks = self.chunk_content(content, metadata)
        logger.info(f"Added {len(chunks)} chunks from {url}")
        
        return chunks

    def scrape(self) -> List[str]:
        """Main scraping method"""
        try:
            all_chunks = []
            urls_to_process = [self.start_url]
            
            while urls_to_process and len(self.visited_urls) < self.config['max_pages']:
                url = urls_to_process.pop(0)
                chunks = self.process_page(url)
                all_chunks.extend(chunks)
                
                # Add new URLs to process
                new_links = self.extract_links(url)
                urls_to_process.extend([link for link in new_links if link not in self.visited_urls])
            
            logger.info(f"\nScraping complete! Scraped {len(self.visited_urls)} pages.")
            logger.info(f"Created {len(all_chunks)} chunks optimized for RAG.")
            
            return all_chunks
            
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return []
        finally:
            self.browser.quit()

class RateLimiter:
    def __init__(self, requests_per_second: float):
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0

    def wait(self):
        """Wait if necessary to maintain rate limit"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_interval:
            sleep_time = self.min_interval - time_since_last_request
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()

def main():
    if len(sys.argv) < 2:
        print("Usage: python doc_scraper.py <url> [config_file]")
        sys.exit(1)
        
    url = sys.argv[1]
    config = None
    
    # Load custom config if provided
    if len(sys.argv) > 2:
        config_file = sys.argv[2]
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            sys.exit(1)
    
    scraper = DocumentationScraper(url, config)
    chunks = scraper.scrape()
    scraper.save_results(chunks, url)

if __name__ == "__main__":
    main()