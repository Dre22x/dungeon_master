#!/usr/bin/env python3
"""
Session Manager for Dungeon Master
Helps manage sessions and provides easy access to ADK web interface.
"""

import requests
import json
import webbrowser
import sys
from typing import List, Dict, Any

class SessionManager:
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all active sessions."""
        try:
            response = requests.get(f"{self.base_url}/sessions")
            if response.status_code == 200:
                data = response.json()
                return data.get('sessions', [])
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to server: {e}")
            return []
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a specific session."""
        try:
            response = requests.delete(f"{self.base_url}/sessions/{session_id}")
            if response.status_code == 200:
                print(f"✅ Session {session_id} deleted successfully")
                return True
            else:
                print(f"❌ Error deleting session: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to server: {e}")
            return False
    
    def open_adk_web(self, campaign_id: str = None):
        """Open ADK web interface with optional session."""
        if campaign_id:
            url = f"http://localhost:8000/dev-ui/?app=dungeon_master&session=session_{campaign_id}"
            print(f"🌐 Opening ADK web for campaign: {campaign_id}")
        else:
            url = "http://localhost:8000/dev-ui/?app=dungeon_master"
            print("🌐 Opening ADK web interface")
        
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"❌ Error opening browser: {e}")
            print(f"Please manually navigate to: {url}")
    
    def display_sessions(self):
        """Display all sessions in a formatted way."""
        sessions = self.list_sessions()
        
        if not sessions:
            print("📭 No active sessions found")
            return
        
        print(f"📋 Active Sessions ({len(sessions)}):")
        print("=" * 80)
        
        for i, session in enumerate(sessions, 1):
            session_id = session.get('session_id', 'Unknown')
            user_id = session.get('user_id', 'Unknown')
            created_at = session.get('created_at', 'Unknown')
            adk_url = session.get('adk_web_url', 'N/A')
            
            # Extract campaign ID from session ID
            campaign_id = session_id.replace('session_', '') if session_id.startswith('session_') else session_id
            
            print(f"{i}. Session ID: {session_id}")
            print(f"   Campaign ID: {campaign_id}")
            print(f"   User ID: {user_id}")
            print(f"   Created: {created_at}")
            print(f"   ADK Web URL: {adk_url}")
            print("-" * 80)

def main():
    manager = SessionManager()
    
    if len(sys.argv) < 2:
        print("🎲 Dungeon Master Session Manager")
        print("=" * 40)
        print("Usage:")
        print("  python session_manager.py list                    - List all sessions")
        print("  python session_manager.py open [campaign_id]      - Open ADK web")
        print("  python session_manager.py delete <session_id>     - Delete session")
        print("  python session_manager.py web                     - Open ADK web (no session)")
        print()
        
        # Show current sessions
        manager.display_sessions()
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        manager.display_sessions()
    
    elif command == "open":
        campaign_id = sys.argv[2] if len(sys.argv) > 2 else None
        manager.open_adk_web(campaign_id)
    
    elif command == "web":
        manager.open_adk_web()
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("❌ Please provide a session ID to delete")
            print("Usage: python session_manager.py delete <session_id>")
            return
        
        session_id = sys.argv[2]
        manager.delete_session(session_id)
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'python session_manager.py' to see available commands")

if __name__ == "__main__":
    main() 