import hashlib
from typing import List
from backend.app.ai.rag.sources.news_source import RawArticle

def get_content_hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def deduplicate_exact(articles: List[RawArticle]) -> List[RawArticle]:
    """Exact deduplication based on content hash."""
    seen_hashes = set()
    unique = []
    
    for article in sorted(articles, key=lambda a: a.published_at):
        h = get_content_hash(article.content)
        if h not in seen_hashes:
            seen_hashes.add(h)
            unique.append(article)
            
    return unique
