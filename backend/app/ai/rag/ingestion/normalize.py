import re
import unicodedata
from urllib.parse import urlparse, urlunparse

def normalize_text(text: str) -> str:
    """Normalize unicode and whitespace."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    # Strip HTML tags naively (use bs4 in prod)
    text = re.sub(r'<[^>]+>', ' ', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def canonicalize_url(url: str) -> str:
    """Strip tracking parameters."""
    parsed = urlparse(url)
    clean_query = "" # remove query params entirely for news canonicalization, or filter
    # simple version: keep scheme, netloc, path
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
