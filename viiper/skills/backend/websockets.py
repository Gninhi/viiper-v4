"""Premium WebSockets & Real-time Communication Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class WebSocketsSkill(Skill):
    """Real-time communication with Socket.io and FastAPI WebSockets."""

    metadata: SkillMetadata = SkillMetadata(
        name="WebSockets & Real-time",
        slug="websockets",
        category=SkillCategory.BACKEND_API,
        difficulty=SkillDifficulty.ADVANCED,
        tags=["websockets", "socket.io", "real-time", "chat", "notifications"],
        estimated_time_minutes=35,
        description="Bi-directional real-time communication with rooms, auth, and events",
    )

    dependencies: list = [
        Dependency(name="socket.io", version="^4.6.1", package_manager="npm", reason="WebSocket server (Node.js)"),
        Dependency(name="socket.io-client", version="^4.6.1", package_manager="npm", reason="WebSocket client"),
        Dependency(name="fastapi", version="^0.109.0", package_manager="pip", reason="FastAPI framework"),
        Dependency(name="websockets", version="^12.0", package_manager="pip", reason="WebSocket support (Python)"),
    ]

    best_practices: list = [
        BestPractice(
            title="Authenticate WebSocket Connections",
            description="Verify token before accepting connection",
            code_reference="io.use(socketAuth middleware)",
            benefit="Prevent unauthorized access",
        ),
        BestPractice(
            title="Use Rooms for Targeted Broadcasting",
            description="Group clients into rooms",
            code_reference="socket.join('room-id')",
            benefit="Send messages to specific groups",
        ),
        BestPractice(
            title="Handle Reconnections Gracefully",
            description="Client should auto-reconnect on disconnect",
            code_reference="reconnection: true, reconnectionDelay: 1000",
            benefit="Better UX, resilient connections",
        ),
        BestPractice(
            title="Emit Acknowledgements",
            description="Use callbacks to confirm message receipt",
            code_reference="socket.emit('msg', data, (ack) => {})",
            benefit="Reliable message delivery",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Emit to Room",
            description="Send message to specific room",
            code='''io.to('room-123').emit('message', {
  text: 'Hello room!',
  userId: user.id
})''',
        ),
        UsageExample(
            name="WebSocket Endpoint",
            description="FastAPI WebSocket route",
            code='''@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Connected!")''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="No authentication on WebSocket",
            why="Anyone can connect and receive data",
            good="Verify JWT token on connection",
        ),
        AntiPattern(
            bad="Broadcasting to all clients always",
            why="Wastes bandwidth, privacy issues",
            good="Use rooms for targeted messages",
        ),
        AntiPattern(
            bad="Blocking operations in event handlers",
            why="Blocks event loop, poor performance",
            good="Use async/await or queues",
        ),
    ]

    file_structure: dict = {
        "backend/lib/socket.ts": "Socket.io server (Node.js)",
        "backend/lib/websocket.py": "WebSocket server (FastAPI)",
        "frontend/lib/socket-client.ts": "Socket.io client (React)",
    }

    socket_server_ts: str = r'''// backend/lib/socket.ts
import { Server as SocketServer } from 'socket.io'
import { Server as HttpServer } from 'http'
import { verifyToken } from '../auth/jwt'

interface SocketData {
  userId: string
  email: string
}

export function setupSocketIO(httpServer: HttpServer) {
  const io = new SocketServer(httpServer, {
    cors: {
      origin: process.env.CLIENT_URL || 'http://localhost:3000',
      credentials: true,
    },
  })

  // Authentication middleware
  io.use(async (socket, next) => {
    try {
      const token = socket.handshake.auth.token

      if (!token) {
        return next(new Error('Authentication required'))
      }

      // Verify JWT token
      const payload = verifyToken(token)
      socket.data.userId = payload.userId
      socket.data.email = payload.email

      next()
    } catch (error) {
      next(new Error('Invalid token'))
    }
  })

  // Connection handler
  io.on('connection', (socket) => {
    const { userId, email } = socket.data as SocketData

    console.log(`User connected: ${userId} (${email})`)

    // Join user's private room
    socket.join(`user:${userId}`)

    // Send welcome message
    socket.emit('connected', {
      message: 'Connected to server',
      userId,
    })

    // Handle joining a room
    socket.on('join-room', (roomId: string) => {
      socket.join(roomId)
      socket.emit('room-joined', { roomId })

      // Notify others in room
      socket.to(roomId).emit('user-joined', {
        userId,
        email,
      })
    })

    // Handle leaving a room
    socket.on('leave-room', (roomId: string) => {
      socket.leave(roomId)
      socket.emit('room-left', { roomId })

      // Notify others
      socket.to(roomId).emit('user-left', { userId })
    })

    // Handle chat messages
    socket.on('send-message', (data: { roomId: string; message: string }) => {
      const { roomId, message } = data

      // Broadcast to room (except sender)
      socket.to(roomId).emit('new-message', {
        userId,
        email,
        message,
        timestamp: new Date(),
      })
    })

    // Handle typing indicator
    socket.on('typing', (data: { roomId: string; isTyping: boolean }) => {
      const { roomId, isTyping } = data

      socket.to(roomId).emit('user-typing', {
        userId,
        isTyping,
      })
    })

    // Handle private messages
    socket.on('private-message', (data: { recipientId: string; message: string }) => {
      const { recipientId, message } = data

      // Send to recipient's private room
      io.to(`user:${recipientId}`).emit('private-message', {
        senderId: userId,
        senderEmail: email,
        message,
        timestamp: new Date(),
      })
    })

    // Disconnect handler
    socket.on('disconnect', (reason) => {
      console.log(`User disconnected: ${userId} (${reason})`)

      // Notify all rooms the user was in
      const rooms = Array.from(socket.rooms).filter(r => r !== socket.id)
      rooms.forEach(room => {
        socket.to(room).emit('user-left', { userId })
      })
    })
  })

  return io
}

// Utility: Send notification to specific user
export function sendNotificationToUser(
  io: SocketServer,
  userId: string,
  notification: any
) {
  io.to(`user:${userId}`).emit('notification', notification)
}

// Utility: Broadcast to room
export function broadcastToRoom(
  io: SocketServer,
  roomId: string,
  event: string,
  data: any
) {
  io.to(roomId).emit(event, data)
}
'''

    websocket_server_py: str = r'''# backend/lib/websocket.py
from fastapi import WebSocket, WebSocketDisconnect, status
from typing import Dict, Set, Optional
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manage WebSocket connections."""

    def __init__(self):
        # Map of user_id -> set of WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}

        # Map of room_id -> set of user_ids
        self.rooms: Dict[str, Set[str]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        """Accept new WebSocket connection."""
        await websocket.accept()

        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()

        self.active_connections[user_id].add(websocket)

        logger.info(f"User {user_id} connected")

    def disconnect(self, websocket: WebSocket, user_id: str):
        """Remove WebSocket connection."""
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)

            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

        # Remove from all rooms
        for room_id in list(self.rooms.keys()):
            self.leave_room(user_id, room_id)

        logger.info(f"User {user_id} disconnected")

    def join_room(self, user_id: str, room_id: str):
        """Add user to room."""
        if room_id not in self.rooms:
            self.rooms[room_id] = set()

        self.rooms[room_id].add(user_id)
        logger.info(f"User {user_id} joined room {room_id}")

    def leave_room(self, user_id: str, room_id: str):
        """Remove user from room."""
        if room_id in self.rooms:
            self.rooms[room_id].discard(user_id)

            if not self.rooms[room_id]:
                del self.rooms[room_id]

            logger.info(f"User {user_id} left room {room_id}")

    async def send_personal_message(self, message: dict, user_id: str):
        """Send message to specific user."""
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending message to {user_id}: {e}")

    async def send_to_room(self, message: dict, room_id: str, exclude_user: Optional[str] = None):
        """Send message to all users in room."""
        if room_id not in self.rooms:
            return

        for user_id in self.rooms[room_id]:
            if exclude_user and user_id == exclude_user:
                continue

            await self.send_personal_message(message, user_id)

    async def broadcast(self, message: dict):
        """Broadcast message to all connected users."""
        for user_id in list(self.active_connections.keys()):
            await self.send_personal_message(message, user_id)

# Global manager instance
manager = ConnectionManager()

# Example FastAPI WebSocket endpoints
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from backend.lib.websocket import manager
from backend.auth.jwt import get_current_user_ws

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    user = Depends(get_current_user_ws)
):
    user_id = user["userId"]

    await manager.connect(websocket, user_id)

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()

            message_type = data.get("type")

            if message_type == "join_room":
                room_id = data["roomId"]
                manager.join_room(user_id, room_id)

                await manager.send_to_room(
                    {"type": "user_joined", "userId": user_id},
                    room_id
                )

            elif message_type == "send_message":
                room_id = data["roomId"]
                message = data["message"]

                await manager.send_to_room(
                    {
                        "type": "new_message",
                        "userId": user_id,
                        "message": message,
                        "timestamp": datetime.utcnow().isoformat()
                    },
                    room_id,
                    exclude_user=user_id
                )

            elif message_type == "leave_room":
                room_id = data["roomId"]
                manager.leave_room(user_id, room_id)

                await manager.send_to_room(
                    {"type": "user_left", "userId": user_id},
                    room_id
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
"""
'''

    socket_client_ts: str = r'''// frontend/lib/socket-client.ts
import { io, Socket } from 'socket.io-client'

class SocketClient {
  private socket: Socket | null = null
  private token: string | null = null

  connect(token: string) {
    this.token = token

    this.socket = io(process.env.NEXT_PUBLIC_WS_URL || 'http://localhost:3001', {
      auth: { token },
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
    })

    // Connection events
    this.socket.on('connect', () => {
      console.log('Socket connected')
    })

    this.socket.on('disconnect', (reason) => {
      console.log('Socket disconnected:', reason)
    })

    this.socket.on('connect_error', (error) => {
      console.error('Connection error:', error.message)
    })

    return this.socket
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
  }

  joinRoom(roomId: string) {
    this.socket?.emit('join-room', roomId)
  }

  leaveRoom(roomId: string) {
    this.socket?.emit('leave-room', roomId)
  }

  sendMessage(roomId: string, message: string) {
    this.socket?.emit('send-message', { roomId, message })
  }

  sendPrivateMessage(recipientId: string, message: string) {
    this.socket?.emit('private-message', { recipientId, message })
  }

  onMessage(callback: (data: any) => void) {
    this.socket?.on('new-message', callback)
  }

  onPrivateMessage(callback: (data: any) => void) {
    this.socket?.on('private-message', callback)
  }

  onUserJoined(callback: (data: any) => void) {
    this.socket?.on('user-joined', callback)
  }

  onUserLeft(callback: (data: any) => void) {
    this.socket?.on('user-left', callback)
  }

  onNotification(callback: (data: any) => void) {
    this.socket?.on('notification', callback)
  }

  // React hook
  getSocket() {
    return this.socket
  }
}

export const socketClient = new SocketClient()

// React hook for WebSocket
import { useEffect, useState } from 'react'

export function useSocket(token: string | null) {
  const [socket, setSocket] = useState<Socket | null>(null)
  const [isConnected, setIsConnected] = useState(false)

  useEffect(() => {
    if (!token) return

    const sock = socketClient.connect(token)
    setSocket(sock)

    sock.on('connect', () => setIsConnected(true))
    sock.on('disconnect', () => setIsConnected(false))

    return () => {
      socketClient.disconnect()
      setIsConnected(false)
    }
  }, [token])

  return { socket, isConnected }
}
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "backend/lib/socket.ts": self.socket_server_ts,
            "backend/lib/websocket.py": self.websocket_server_py,
            "frontend/lib/socket-client.ts": self.socket_client_ts,
        }
