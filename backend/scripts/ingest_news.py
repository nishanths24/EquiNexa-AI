import os
import sys
import yfinance as yf
from datetime import datetime, timezone
import hashlib

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.app.ai.embeddings.local_provider import LocalEmbeddingProvider
from backend.app.ai.rag.vectorstores.chroma_store import ChromaVectorStore
from backend.app.ai.rag.vectorstores.vector_store import VectorItem

def ingest_news():
    universe = ["AAPL", "MSFT", "GOOGL"]
    
    embedder = LocalEmbeddingProvider()
    vs = ChromaVectorStore("./data/chroma_db")
    vs.ensure_collection("financial_news", dim=384)
    
    for ticker in universe:
        print(f"Fetching news for {ticker}...")
        tkr = yf.Ticker(ticker)
        news = tkr.news
        
        items = []
        for item in news:
            article = item.get("content") or {}
            title = article.get("title", "")
            provider = article.get("provider") or {}
            publisher = provider.get("displayName", "")
            click_url = article.get("clickThroughUrl") or {}
            link = click_url.get("url", "")
            pub_dt_str = article.get("pubDate", "")
            
            if not title:
                continue
                
            if pub_dt_str:
                # yfinance returns ISO string like "2026-09-29T14:14:34Z"
                try:
                    pub_dt = pub_dt_str.replace("Z", "+00:00")
                    dt_obj = datetime.fromisoformat(pub_dt)
                    pub_dt = dt_obj.isoformat()
                except ValueError:
                    pub_dt = datetime.now(timezone.utc).isoformat()
            else:
                pub_dt = datetime.now(timezone.utc).isoformat()
            
            content = f"Title: {title}\nPublisher: {publisher}\nTicker: {ticker}"
            
            # Content Hash
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            
            vector = embedder.embed_text(content)
            
            payload = {
                "text": content,
                "title": title,
                "publisher": publisher,
                "url": link,
                "published_at": pub_dt,
                "ingested_at": datetime.now(timezone.utc).isoformat(),
                "ticker": ticker,
                "content_hash": content_hash
            }
            
            items.append(VectorItem(id=content_hash, vector=vector.tolist(), payload=payload))
            
        if items:
            vs.upsert("financial_news", items)
            print(f"Ingested {len(items)} articles for {ticker}")

if __name__ == "__main__":
    ingest_news()
