# sudo dnf install python3-pip
from fastapi import FastAPI, Response, Request
from fastapi.responses import HTMLResponse, StreamingResponse
import time
import os
import subprocess
import asyncio
import socket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # atau ganti dengan daftar origin yang diperbolehkan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path ke file log Nginx
LOG_FILE = "/var/log/nginx/access.log"

@app.get("/", response_class=HTMLResponse)
def read_index():
    index_path = "/usr/share/nginx/html/index.html"
    if os.path.isfile(index_path):
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                content = f.read()
            return content
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading index file: {e}")
    else:
        raise HTTPException(status_code=404, detail="Index file not found.")

subscribers = []

async def broadcast_logs():
    # Jalankan tail -f secara asynchronous
    process = await asyncio.create_subprocess_exec(
        "tail", "-f", LOG_FILE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        text=False
    )
    while True:
        line = await process.stdout.readline()
        if line:
            for queue in subscribers:
                await queue.put(line)
        else:
            await asyncio.sleep(0.1)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(broadcast_logs())

@app.get("/stream-logs")
async def stream_logs(request: Request):
    queue = asyncio.Queue()
    subscribers.append(queue)

    async def event_generator():
        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    line = await asyncio.wait_for(queue.get(), timeout=2.0)
                    yield f"data: {line}\n\n"
                except asyncio.TimeoutError:
                    yield ":\n\n"
        finally:
            subscribers.remove(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# Definisikan server yang akan dipantau
servers = {
    "web-public-1": {
        "ip": "192.168.100.5",
        "ports": [22, 80, 443]
    },
    "web-public-2": {
        "ip": "192.168.100.4",
        "ports": [22, 80, 443]
    },
    "storage-server-private": {
        "ip": "192.168.100.28",
        "ports": [2049, 111]
    },
    "api-public": {
        "ip": "172.31.0.14",
        "ports": [22, 80, 443]
    },
    "database-server-private": {
        "ip": "only api-public can access",
        "ports": [3306]
    }
}

def is_port_open(ip: str, port: int, timeout: int = 2) -> bool:
    """
    Coba koneksi ke IP dan port tertentu dengan timeout.
    Kembalikan True jika koneksi berhasil, False jika gagal.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        sock.close()
        return True
    except Exception:
        return False

@app.get("/status")
def check_status():
    """
    Endpoint untuk memeriksa status setiap server.
    Jika salah satu port terbuka, server dianggap online.
    """
    status = {}
    for server_name, data in servers.items():
        ip = data["ip"]
        port_status = {}
        online = False  # Asumsikan server down
        for port in data["ports"]:
            port_ok = is_port_open(ip, port)
            port_status[port] = "online" if port_ok else "down"
            if port_ok:
                online = True
        status[server_name] = {
            "ip": ip,
            "overall": "online" if online else "down",
            "ports": port_status
        }
    return status
