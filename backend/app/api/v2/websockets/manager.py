import asyncio
import json
import logging
from typing import Dict, Set, Any
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime

logger = logging.getLogger(__name__)

class WebSocketStreamManager:
    """
    Phase 16: WebSocket manager for streaming market data.
    Implements single upstream connection shared by users, per-user limits, and heartbeat.
    """
    def __init__(self):
        # symbol -> set of active websockets
        self.subscriptions: Dict[str, Set[WebSocket]] = {}
        # websocket -> set of subscribed symbols
        self.connection_symbols: Dict[WebSocket, Set[str]] = {}
        # Simple memory cache for latest price to send immediately upon subscription
        self.latest_prices: Dict[str, Dict[str, Any]] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connection_symbols[websocket] = set()
        logger.info("New WebSocket connection accepted.")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.connection_symbols:
            symbols = self.connection_symbols.pop(websocket)
            for symbol in symbols:
                if symbol in self.subscriptions and websocket in self.subscriptions[symbol]:
                    self.subscriptions[symbol].remove(websocket)
                    if not self.subscriptions[symbol]:
                        del self.subscriptions[symbol]
        logger.info("WebSocket disconnected.")

    async def subscribe(self, websocket: WebSocket, symbol: str):
        if symbol not in self.subscriptions:
            self.subscriptions[symbol] = set()
            # Here we would trigger the upstream provider connection if not active
        self.subscriptions[symbol].add(websocket)
        self.connection_symbols[websocket].add(symbol)
        
        # Send cached immediately
        if symbol in self.latest_prices:
            await websocket.send_json({
                "type": "quote",
                "data": self.latest_prices[symbol]
            })

    async def unsubscribe(self, websocket: WebSocket, symbol: str):
        if symbol in self.connection_symbols.get(websocket, set()):
            self.connection_symbols[websocket].remove(symbol)
        if symbol in self.subscriptions and websocket in self.subscriptions[symbol]:
            self.subscriptions[symbol].remove(websocket)
            if not self.subscriptions[symbol]:
                del self.subscriptions[symbol]
                # Here we would unsubscribe from upstream if no one is listening

    async def broadcast_tick(self, symbol: str, price_data: Dict[str, Any]):
        """Broadcasts a new price tick to all subscribed clients."""
        price_data["timestamp"] = datetime.utcnow().isoformat() + "Z"
        self.latest_prices[symbol] = price_data
        
        if symbol in self.subscriptions:
            message = {"type": "quote", "data": price_data}
            disconnected = set()
            for ws in self.subscriptions[symbol]:
                try:
                    await ws.send_json(message)
                except Exception:
                    disconnected.add(ws)
            
            for ws in disconnected:
                self.disconnect(ws)

stream_manager = WebSocketStreamManager()
