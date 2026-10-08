import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class SupabaseClient:
    """
    Supabase (PostgreSQL + Auth) integration client for V2 Architecture.
    Handles TimescaleDB data caching and JWT authentication verification.
    """
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL", "")
        self.supabase_key = os.getenv("SUPABASE_KEY", "")
        self._client = None
        
        if not self.supabase_url or not self.supabase_key:
            logger.warning("Supabase URL or Key is missing. Database persistence is disabled (Basic Architecture fallback mode).")

    @property
    def client(self):
        # We lazy-load the client to prevent application startup failure if not configured
        if not self._client and self.supabase_url and self.supabase_key:
            try:
                from supabase import create_client, Client
                self._client = create_client(self.supabase_url, self.supabase_key)
            except ImportError:
                logger.error("supabase-py library not installed. Please add it to requirements.txt")
        return self._client

supabase_db = SupabaseClient()
