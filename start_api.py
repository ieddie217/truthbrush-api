#!/usr/bin/env python3
"""
Script to start both FastAPI server and ngrok tunnel.
"""

import subprocess
import time
import sys
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

def verify_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "youruser")
    correct_password = secrets.compare_digest(credentials.password, "yourpass")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def start_services():
    """Start both FastAPI server and ngrok tunnel."""
    
    print("🚀 Starting Truthbrush API Server...")
    
    # Start FastAPI server
    print("📡 Starting FastAPI server...")
    uvicorn_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"
    ])
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(5)
    
    # Start ngrok tunnel
    print("🌐 Starting ngrok tunnel...")
    ngrok_process = subprocess.Popen(["ngrok", "http", "8000"])
    
    print("\n✅ Both services are running!")
    print("📱 FastAPI Server: http://localhost:8000")
    print("🔗 ngrok URL will appear in the ngrok window")
    print("\nPress Ctrl+C to stop both services...")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        uvicorn_process.terminate()
        ngrok_process.terminate()
        print("✅ Services stopped.")

if __name__ == "__main__":
    start_services() 