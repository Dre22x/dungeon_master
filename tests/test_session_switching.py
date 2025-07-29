#!/usr/bin/env python3
"""
Test script to verify session switching functionality.
"""

import requests
import json
import time

def test_session_switching():
    """Test the session switching functionality."""
    
    print("🧪 Testing Session Switching Functionality")
    print("=" * 50)
    
    base_url = "http://localhost:5001"
    
    # Test 1: Create a new campaign
    print("1. Creating a new campaign...")
    try:
        response = requests.post(f"{base_url}/new-campaign")
        if response.status_code == 200:
            data = response.json()
            campaign_id = data['campaign_id']
            print(f"✅ Campaign created: {campaign_id}")
            print(f"   ADK URL: {data['adk_url']}")
        else:
            print(f"❌ Failed to create campaign: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error creating campaign: {e}")
        return
    
    # Test 2: Get current session
    print("\n2. Getting current session...")
    try:
        response = requests.get(f"{base_url}/get-current-session/{campaign_id}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Current session: {data['session_id']}")
            print(f"   Agent: {data['agent_name']}")
            print(f"   ADK URL: {data['adk_url']}")
        else:
            print(f"❌ Failed to get current session: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting current session: {e}")
    
    # Test 3: Manual session switch
    print("\n3. Testing manual session switch...")
    try:
        test_session_id = f"test_session_{int(time.time())}"
        test_agent_name = "Test Agent"
        
        response = requests.post(f"{base_url}/switch-session/{campaign_id}", 
                               json={
                                   'session_id': test_session_id,
                                   'agent_name': test_agent_name
                               })
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Session switched to: {data['session_id']}")
            print(f"   Agent: {data['agent_name']}")
            print(f"   ADK URL: {data['adk_url']}")
        else:
            print(f"❌ Failed to switch session: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error switching session: {e}")
    
    # Test 4: List sessions
    print("\n4. Listing all sessions...")
    try:
        response = requests.get(f"{base_url}/sessions")
        if response.status_code == 200:
            data = response.json()
            sessions = data.get('sessions', [])
            print(f"✅ Found {len(sessions)} sessions:")
            for session in sessions:
                print(f"   - {session['session_id']} (User: {session['user_id']})")
        else:
            print(f"❌ Failed to list sessions: {response.status_code}")
    except Exception as e:
        print(f"❌ Error listing sessions: {e}")
    
    print("\n✅ Session switching test completed!")
    print(f"📝 Campaign ID for manual testing: {campaign_id}")

if __name__ == "__main__":
    test_session_switching() 