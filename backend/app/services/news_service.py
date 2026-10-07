from typing import List
from datetime import timedelta
from app.models.domain.news import NewsArticle

def deduplicate_news(articles: List[NewsArticle], time_window_hours: int = 2) -> List[NewsArticle]:
    """
    Phase 8 Deduplication Engine:
    Merge identical headlines within a configurable time window.
    """
    # Sort newest first
    sorted_articles = sorted(articles, key=lambda x: x.published_at, reverse=True)
    deduped = []
    
    for article in sorted_articles:
        is_duplicate = False
        for seen in deduped:
            time_diff = abs((article.published_at - seen.published_at).total_seconds()) / 3600.0
            if time_diff <= time_window_hours:
                # Normalizing for simple dedup check
                headline_a = article.headline.lower().strip()
                headline_b = seen.headline.lower().strip()
                if headline_a == headline_b:
                    is_duplicate = True
                    break
        
        if not is_duplicate:
            deduped.append(article)
            
    return deduped

def apply_delay_labels(articles: List[NewsArticle]) -> List[NewsArticle]:
    """
    Phase 8 Delayed Labeling:
    If news published > 15 minutes before retrieval time, label as DELAYED.
    """
    for article in articles:
        age_minutes = (article.retrieved_at - article.published_at).total_seconds() / 60.0
        if age_minutes > 15:
            article.delay_label = "DELAYED"
        else:
            article.delay_label = "LIVE"
    return articles
