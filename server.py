import os
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import socket
import secrets

app = FastAPI(title="Etherdesk Server")

security = HTTPBasic()

load_dotenv()

# load credentials from environment variables, fallback to defaults if not set
USERNAME = os.getenv("USERNAME", "babe")
PASSWORD = os.getenv("PASSWORD", "Diwakar@25")

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Get absolute path for the Etherdesk directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
PROMPT_FILE = os.path.join(BASE_DIR, "prompt.txt")
RESPONSE_FILE = os.path.join(BASE_DIR, "response.txt")

# Ensure files exist
if not os.path.exists(PROMPT_FILE):
    with open(PROMPT_FILE, "w", encoding="utf-8") as f:
        f.write("")
if not os.path.exists(RESPONSE_FILE):
    with open(RESPONSE_FILE, "w", encoding="utf-8") as f:
        f.write("")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class ChatMessage(BaseModel):
    message: str

class WriteFileRequest(BaseModel):
    path: str
    content: str

class TerminalRequest(BaseModel):
    command: str
    cwd: str = "f:/bn"

@app.get("/", response_class=HTMLResponse)
async def read_root(user: str = Depends(authenticate)):
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Etherdesk UI not found! Please ensure static/index.html exists."

@app.post("/api/chat/send")
async def send_chat(msg: ChatMessage, user: str = Depends(authenticate)):
    # Write the message to prompt.txt for Antigravity to read
    with open(PROMPT_FILE, "w", encoding="utf-8") as f:
        f.write(msg.message)
    # Clear the response file so we know when a new response arrives
    with open(RESPONSE_FILE, "w", encoding="utf-8") as f:
        f.write("")
    return {"status": "success", "message": "Prompt sent to Antigravity."}

@app.get("/api/chat/receive")
async def receive_chat(user: str = Depends(authenticate)):
    # Read the response from response.txt
    if os.path.exists(RESPONSE_FILE):
        with open(RESPONSE_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            if content.strip():
                return {"status": "success", "message": content}
    return {"status": "waiting", "message": ""}

@app.get("/api/fs/list")
async def list_files(path: str = "f:/bn", user: str = Depends(authenticate)):
    # Simple endpoint to list files in a directory
    if not os.path.exists(path):
        return JSONResponse(status_code=404, content={"error": "Path not found"})
    
    try:
        items = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            is_dir = os.path.isdir(item_path)
            items.append({
                "name": item,
                "path": item_path.replace("\\", "/"),
                "is_dir": is_dir
            })
        # Sort directories first, then files
        items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
        return {"items": items}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/fs/read")
async def read_file(path: str, user: str = Depends(authenticate)):
    if not os.path.exists(path) or os.path.isdir(path):
        return JSONResponse(status_code=404, content={"error": "File not found or is directory"})
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        # Fallback for binary files or decoding issues
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/fs/write")
async def write_file(req: WriteFileRequest, user: str = Depends(authenticate)):
    if os.path.isdir(req.path):
        return JSONResponse(status_code=400, content={"error": "Cannot write to a directory"})
    try:
        with open(req.path, "w", encoding="utf-8") as f:
            f.write(req.content)
        return {"status": "success"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/terminal/run")
async def run_terminal(req: TerminalRequest, user: str = Depends(authenticate)):
    import subprocess
    try:
        process = subprocess.Popen(
            req.command, 
            shell=True,
            cwd=req.cwd,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(timeout=60)
        return {"stdout": stdout, "stderr": stderr, "returncode": process.returncode}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == "__main__":
    ip = get_local_ip()
    print(f"====================================================")
    print(f"[*] Etherdesk Server is running!")
    print(f"[*] Open this URL in your phone's browser:")
    print(f"    http://{ip}:8080")
    print(f"====================================================")
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)
