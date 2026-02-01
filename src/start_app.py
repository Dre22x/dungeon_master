#!/usr/bin/env python3
"""
Startup script for the AI Dungeon Master application.
This script will automatically start both the Flask web server and the ADK web interface.
"""

import subprocess
import sys
import os
import time
import threading
import signal
from pathlib import Path

flask_process = None
adk_process = None

def signal_handler(signum, frame):
    print("\n🛑 Shutting down services...")
    if flask_process:
        flask_process.terminate()
        print("✅ Flask server stopped")
    if adk_process:
        adk_process.terminate()
        print("✅ ADK web interface stopped")
    sys.exit(0)
``
def start_flask_app():
    """Start the Flask web application."""
    global flask_process
    print("🚀 Starting Flask web server...")
    flask_dir = Path(__file__).parent / "web"
    venv_python = Path(__file__).parent.parent / "venv" / "bin" / "python"
    
    try:
        # Start Flask app using virtual environment Python
        flask_process = subprocess.Popen(
            [str(venv_python), "app.py"],
            cwd=flask_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("✅ Flask server started successfully")
    except Exception as e:
        print(f"❌ Error starting Flask server: {e}")

def check_ports():
    """Check if port 5001 is available."""
    import socket
    
    ports_to_check = [5001]
    unavailable_ports = []
    
    for port in ports_to_check:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        if result == 0:
            unavailable_ports.append(port)
    
    if unavailable_ports:
        print(f"⚠️  Warning: Ports {unavailable_ports} are already in use.")
        print("   Make sure no other instances are running.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)

def main():
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    print("🎲 AI Dungeon Master - Automated Startup")
    print("=" * 50)
    
    project_root = Path(__file__).parent.parent
    if not (project_root / "adk.yaml").exists():
        print("❌ Error: adk.yaml not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    try:
        subprocess.run(["adk", "--version"], capture_output=True, check=True)
        print("✅ ADK is available (optional for development)")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ℹ️  ADK not found - this is optional now since we use custom chat interface")
    
    # Check port availability
    check_ports()
    
    print("📋 Starting services...")
    print()
    
    flask_thread = threading.Thread(target=start_flask_app, daemon=True)
    flask_thread.start()
    
    time.sleep(2)
    
    print("🎉 All services started successfully!")
    print("=" * 50)
    print("🌐 Web Interface: http://localhost:5001")
    print()
    print("📝 Usage:")
    print("1. Open http://localhost:5001 in your browser")
    print("2. Create a new campaign or load an existing one")
    print("3. Use the built-in chat interface for agent interaction")
    print()
    print("Press Ctrl+C to stop all services")
    print()
    
    try:
        while True:
            time.sleep(1)
            
            if flask_process and flask_process.poll() is not None:
                print("❌ Flask server stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main() 