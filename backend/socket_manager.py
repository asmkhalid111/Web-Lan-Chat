from typing import Dict
from fastapi import WebSocket
import json

class ConnectionManager:
    def __init__(self):
        # Maps student_id to their active WebSocket connection
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, student_id: str):
        await websocket.accept()
        self.active_connections[student_id] = websocket
        await self.broadcast_user_status()

    def disconnect(self, student_id: str):
        if student_id in self.active_connections:
            del self.active_connections[student_id]
        # We need to run broadcast_user_status, but disconnect isn't async here.
        # We will handle it in the websocket endpoint.

    async def send_personal_message(self, message: dict, student_id: str):
        if student_id in self.active_connections:
            await self.active_connections[student_id].send_text(json.dumps(message))

    async def broadcast(self, message: dict):
        # Convert message to JSON string
        json_msg = json.dumps(message)
        for connection in self.active_connections.values():
            await connection.send_text(json_msg)
            
    async def broadcast_user_status(self):
        # Send a list of online users to everyone
        online_users = list(self.active_connections.keys())
        await self.broadcast({"type": "status", "online_users": online_users})

manager = ConnectionManager()
