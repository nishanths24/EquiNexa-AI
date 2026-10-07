from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Any
import json
import logging

from app.api.v2.websockets.manager import stream_manager

router = APIRouter(
    prefix="/stream",
    tags=["V2 Stream"]
)
logger = logging.getLogger(__name__)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Phase 16: Stream manager endpoint.
    Expects messages like: {"action": "subscribe", "symbol": "RELIANCE.NS"}
    """
    await stream_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                action = message.get("action")
                symbol = message.get("symbol")
                
                if action == "subscribe" and symbol:
                    await stream_manager.subscribe(websocket, symbol)
                elif action == "unsubscribe" and symbol:
                    await stream_manager.unsubscribe(websocket, symbol)
                elif action == "ping":
                    await websocket.send_json({"type": "pong"})
            except json.JSONDecodeError:
                logger.warning("Invalid JSON received on websocket")
                
    except WebSocketDisconnect:
        stream_manager.disconnect(websocket)
