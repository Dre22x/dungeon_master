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

# Global variables to track processes
flask_process = None
adk_process = None

def signal_handler(signum, frame):
    """Handle Ctrl+C to gracefully shut down both processes."""
    print("\n🛑 Shutting down services...")
    if flask_process:
        flask_process.terminate()
        print("✅ Flask server stopped")
    if adk_process:
        adk_process.terminate()
        print("✅ ADK web interface stopped")
    sys.exit(0)

def start_flask_app():
    """Start the Flask web application."""
    global flask_process
    print("🚀 Starting Flask web server...")
    flask_dir = Path(__file__).parent / "UI"
    
    try:
        # Start Flask app
        flask_process = subprocess.Popen(
            [sys.executable, "app.py"],
            cwd=flask_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("✅ Flask server started successfully")
    except Exception as e:
        print(f"❌ Error starting Flask server: {e}")

def start_adk_web():
    """Start the ADK web interface."""
    global adk_process
    print("🌐 Starting ADK web interface...")
    
    try:
        # Start ADK web interface
        adk_process = subprocess.Popen(
            ["adk", "web", "."],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("✅ ADK web interface started successfully")
    except Exception as e:
        print(f"❌ Error starting ADK web interface: {e}")
        print("💡 Make sure you have ADK installed: pip install google-adk")

def check_ports():
    """Check if ports 5001 and 8000 are available."""
    import socket
    
    ports_to_check = [5001, 8000]
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
    
    # Check if we're in the right directory
    if not Path("adk.yaml").exists():
        print("❌ Error: adk.yaml not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check if ADK is installed
    try:
        subprocess.run(["adk", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: ADK not found. Please install it with: pip install google-adk")
        sys.exit(1)
    
    # Check port availability
    check_ports()
    
    print("📋 Starting services...")
    print()
    
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=start_flask_app, daemon=True)
    flask_thread.start()
    
    # Wait a moment for Flask to start
    time.sleep(2)
    
    # Start ADK web interface in a separate thread
    adk_thread = threading.Thread(target=start_adk_web, daemon=True)
    adk_thread.start()
    
    # Wait a moment for ADK to start
    time.sleep(3)
    
    print()
    print("🎉 All services started successfully!")
    print("=" * 50)
    print("🌐 Web Interface: http://localhost:5001")
    print("🤖 ADK Dev UI: http://localhost:8000")
    print()
    print("📝 Usage:")
    print("1. Open http://localhost:5001 in your browser")
    print("2. Create a new campaign or load an existing one")
    print("3. Use the ADK dev UI at http://localhost:8000 for agent interaction")
    print()
    print("Press Ctrl+C to stop all services")
    print()
    
    try:
        # Keep the main thread alive and monitor processes
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if flask_process and flask_process.poll() is not None:
                print("❌ Flask server stopped unexpectedly")
                break
            if adk_process and adk_process.poll() is not None:
                print("❌ ADK web interface stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main() 