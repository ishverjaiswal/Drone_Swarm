import sys
import os
import asyncio
import time
import cv2
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from database import init_db, AsyncSessionLocal
from models import TelemetryLog

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
try:
    from drone_swarm.tello_swarm import TelloSwarm
except ImportError:
    TelloSwarm = None

app = FastAPI(title="Drone Swarm Live UDP Discovery GCS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()
swarm = None

# --- DYNAMIC SWARM STATE REGISTRY ---
# Structure: { ip_address: { "drone_id": str, "last_seen": float, "telemetry": dict } }
active_swarm = {}
ip_to_id_map = {}

def get_or_assign_drone_id(ip_address: str) -> str:
    """Dynamically registers new IPs to sequential tello_XX identifiers."""
    if ip_address not in ip_to_id_map:
        assigned_number = len(ip_to_id_map) + 1
        ip_to_id_map[ip_address] = f"tello_0{assigned_number}"
        print(f"🟢 [NET DISCOVERY] Live Drone Discovered at {ip_address} -> Assigned {ip_to_id_map[ip_address]}")
    return ip_to_id_map[ip_address]

def parse_tello_state_string(raw_data: str, drone_id: str) -> dict:
    """Parses standard Tello UDP state format: 'pitch:0;roll:0;yaw:0;bat:85;tof:120;templ:36;...'"""
    parsed = {
        "drone_id": drone_id,
        "battery": 0,
        "altitude": 0.0,
        "pitch": 0,
        "roll": 0,
        "yaw": 0,
        "temperature": 0.0
    }
    try:
        items = raw_data.strip().split(";")
        for item in items:
            if ":" in item:
                key, value = item.split(":")
                if key == "bat":
                    parsed["battery"] = int(value)
                elif key == "pitch":
                    parsed["pitch"] = int(value)
                elif key == "roll":
                    parsed["roll"] = int(value)
                elif key == "yaw":
                    parsed["yaw"] = int(value)
                elif key == "tof":  # Time of Flight sensor in cm -> convert to meters
                    parsed["altitude"] = round(float(value) / 100.0, 2)
                elif key == "templ":
                    parsed["temperature"] = float(value)
    except Exception as e:
        print(f"⚠️ [PARSE ERROR] Invalid telemetry packet from {drone_id}: {e}")
    return parsed

# --- FEATURE 1: UDP BROADCAST LISTENER (PORT 8890) ---
class TelloStateProtocol(asyncio.DatagramProtocol):
    def datagram_received(self, data: bytes, addr: tuple):
        sender_ip = addr[0]
        raw_text = data.decode("utf-8", errors="ignore")
        drone_id = get_or_assign_drone_id(sender_ip)
        
        # Parse live UDP telemetry
        telemetry = parse_tello_state_string(raw_text, drone_id)
        
        # Update dynamic swarm registry with live timestamp
        active_swarm[sender_ip] = {
            "drone_id": drone_id,
            "last_seen": time.time(),
            "telemetry": telemetry
        }

async def start_udp_listener():
    """Starts async background UDP server on port 8890 to listen for tello state broadcasts."""
    loop = asyncio.get_running_loop()
    print("📡 [NET DISCOVERY] Listening for live Tello UDP state packets on port 8890...")
    try:
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: TelloStateProtocol(),
            local_addr=('0.0.0.0', 8890)
        )
    except Exception as e:
        print(f"❌ [UDP ERROR] Could not bind port 8890: {e}")

@app.on_event("startup")
async def startup_event():
    await init_db()
    # Start UDP listener task for dynamic discovery
    asyncio.create_task(start_udp_listener())
    # Start telemetry broadcast and stale pruning loop
    asyncio.create_task(telemetry_loop())

# --- FEATURE 2: HEARTBEAT PRUNING & STALE DATA CLEARING ---
async def telemetry_loop():
    TIMEOUT_THRESHOLD = 2.0  # Seconds before marking unit as OFFLINE

    while True:
        current_time = time.time()
        broadcast_payload = {}
        stale_ips = []

        # Check all discovered units for stale telemetry (> 2.0s timeout)
        for sender_ip, info in list(active_swarm.items()):
            time_since_last_seen = current_time - info["last_seen"]

            if time_since_last_seen > TIMEOUT_THRESHOLD:
                print(f"🔴 [HEARTBEAT TIMEOUT] Lost signal from {info['drone_id']} ({sender_ip}) - Pruning")
                stale_ips.append(sender_ip)
            else:
                # Active & healthy unit
                broadcast_payload[info["drone_id"]] = info["telemetry"]

        # Clean up stale nodes from registry
        for ip in stale_ips:
            del active_swarm[ip]

        # 1. Broadcast active live telemetry map over WebSockets
        await manager.broadcast(broadcast_payload)

        # 2. Persist real flight telemetry into SQLite database
        if broadcast_payload:
            async with AsyncSessionLocal() as session:
                for drone_id, telemetry_data in broadcast_payload.items():
                    log_entry = TelemetryLog(**telemetry_data)
                    session.add(log_entry)
                await session.commit()

        await asyncio.sleep(0.5)  # 2Hz telemetry loop

def generate_video_frames_for_drone(requested_id: str):
    """Generates JPEG frame stream for a specific requested drone ID."""
    while True:
        target_ip = None
        for ip, assigned_id in ip_to_id_map.items():
            if assigned_id == requested_id:
                target_ip = ip
                break

        if swarm and hasattr(swarm, 'drones') and target_ip in swarm.drones:
            drone_obj = swarm.drones[target_ip]
            if hasattr(drone_obj, 'get_frame_read'):
                frame = drone_obj.get_frame_read()
                if frame is not None:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    if ret:
                        frame_bytes = buffer.tobytes()
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        asyncio.run(asyncio.sleep(0.04))

@app.get("/video_feed/{drone_id}")
async def video_feed(drone_id: str):
    return StreamingResponse(
        generate_video_frames_for_drone(drone_id),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.websocket("/ws/telemetry")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)