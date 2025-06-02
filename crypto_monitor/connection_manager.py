from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List

class ConnectionManager:
    def __init__(self):
        # Diccionario WebSocket -> lista de criptomonedas favoritas
        self.active_connections: Dict[WebSocket, List[str]] = {}

    async def connect(self, websocket: WebSocket, preferences: List[str]):
        await websocket.accept()
        self.active_connections[websocket] = preferences

    def disconnect(self, websocket: WebSocket):
        self.active_connections.pop(websocket, None)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        to_remove = []
        for connection in self.active_connections.keys():
            try:
                await connection.send_text(message)
            except Exception:
                to_remove.append(connection)
        for conn in to_remove:
            self.disconnect(conn)

