"""
utils.py - Core HTTP Client, HTML Parsing, and Security/Crawlability Utilities
Used by all sub-skills for deterministic, provider-neutral website audits.
"""

import urllib.request
import urllib.parse
import re
import json
from typing import Dict, Any, Tuple, List, Optional
from bs4 import BeautifulSoup


DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
BOT_USER_AGENTS = {
    "GPTBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.0; +https://openai.com/gptbot)",
    "PerplexityBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)",
    "ClaudeBot": "Mozilla/5.0 (compatible; ClaudeBot/1.0; +https://anthropic.com/claudebot)"
}


def normalize_url(url: str) -> str:
    """Ensure URL has protocol scheme."""
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url.rstrip("/")


def extract_domain(url: str) -> str:
    """Extract domain host name from URL."""
    parsed = urllib.parse.urlparse(normalize_url(url))
    return parsed.netloc or parsed.path.split("/")[0]


def fetch_url(url: str, user_agent: str = DEFAULT_USER_AGENT, timeout: int = 10) -> Tuple[int, str, Dict[str, str]]:
    """
    Fetch URL content safely. Returns (status_code, body_text, headers_dict).
    """
    url = normalize_url(url)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": user_agent, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status = response.getcode()
            headers = dict(response.info())
            body = response.read().decode('utf-8', errors='ignore')
            return status, body, headers
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore') if e.fp else ""
        return e.code, body, dict(e.headers) if e.headers else {}
    except Exception as e:
        return 0, str(e), {}


def extract_raw_text_word_count(html_content: str) -> int:
    """Extract text from raw HTML (simulating plain web crawler) and count words."""
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup(['script', 'style', 'head', 'meta', 'svg', 'path', 'link', 'noscript']):
        tag.extract()
    text = soup.get_text(separator=' ')
    words = [w for w in text.split() if len(w) > 1]
    return len(words)


def extract_json_ld_schemas(html_content: str) -> List[Dict[str, Any]]:
    """Extract all Schema.org JSON-LD scripts from HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    schemas = []
    for script in soup.find_all('script', type='application/ld+json'):
        if script.string:
            try:
                data = json.loads(script.string)
                if isinstance(data, list):
                    schemas.extend(data)
                elif isinstance(data, dict):
                    schemas.append(data)
            except Exception:
                pass
    return schemas
