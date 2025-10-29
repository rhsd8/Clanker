"""
WebSocket Server for Robot UI Communication
Broadcasts robot state changes to React frontend
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import uvicorn
from typing import Set
import json

app = FastAPI(title="Robot WebSocket Server")

# Enable CORS for React frontend (localhost only - extended display)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active WebSocket connections
active_connections: Set[WebSocket] = set()

# Current robot state
current_state = {"state": "idle", "text": ""}


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Robot WebSocket Server Running"}


@app.get("/state")
async def get_state():
    """Get current robot state"""
    return current_state


@app.post("/state")
async def update_state(state: str, text: str = ""):
    """
    Update robot state and broadcast to all connected clients

    Args:
        state: Robot state (idle, listening, thinking, speaking)
        text: Optional text to display
    """
    current_state["state"] = state
    current_state["text"] = text

    # Broadcast to all connected clients
    await broadcast_state(state, text)

    return {"success": True, "state": state}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time state updates"""
    await websocket.accept()
    active_connections.add(websocket)

    print(f"✅ Client connected. Total connections: {len(active_connections)}")

    # Send current state to newly connected client
    await websocket.send_json(current_state)

    try:
        while True:
            # Keep connection alive and listen for messages
            data = await websocket.receive_text()
            # Echo back for testing
            await websocket.send_text(f"Echo: {data}")

    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print(f"❌ Client disconnected. Total connections: {len(active_connections)}")


async def broadcast_state(state: str, text: str = ""):
    """Broadcast state change to all connected clients"""
    message = {"state": state, "text": text}

    # Remove disconnected clients
    disconnected = set()

    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception as e:
            print(f"⚠️  Error sending to client: {e}")
            disconnected.add(connection)

    # Clean up disconnected clients
    for conn in disconnected:
        active_connections.remove(conn)


# Helper function to call from Python code
async def send_state(state: str, text: str = ""):
    """Send state update (called from main.py)"""
    await broadcast_state(state, text)


if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Starting Robot WebSocket Server")
    print("=" * 50)
    print("📡 WebSocket: ws://localhost:8000/ws")
    print("🌐 HTTP API: http://localhost:8000")
    print("=" * 50)

    uvicorn.run(
        app,
        host="localhost",
        port=8000,
        log_level="info"
    )
