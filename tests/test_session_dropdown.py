#!/usr/bin/env python3
"""
Test script to verify the dropdown session switching functionality.
"""

import requests
import json
import time

def test_session_dropdown():
    """Test the dropdown session switching functionality."""
    
    print("🧪 Testing Dropdown Session Switching")
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
        else:
            print(f"❌ Failed to create campaign: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error creating campaign: {e}")
        return
    
    # Test 2: Get available sessions
    print("\n2. Getting available sessions...")
    try:
        response = requests.get(f"{base_url}/get-available-sessions/{campaign_id}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['total_sessions']} sessions:")
            for session in data['sessions']:
                print(f"   - {session['agent_name']} ({session['session_id']})")
                print(f"     Description: {session['description']}")
        else:
            print(f"❌ Failed to get available sessions: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error getting available sessions: {e}")
    
    # Test 3: Create some test sub-agent sessions
    print("\n3. Creating test sub-agent sessions...")
    try:
        test_sessions = [
            {"session_id": f"sub_agent_character_creation_{campaign_id}_{int(time.time())}", "agent_name": "Character Creation Agent"},
            {"session_id": f"sub_agent_narrative_{campaign_id}_{int(time.time())}", "agent_name": "Narrative Agent"},
            {"session_id": f"sub_agent_rules_lawyer_{campaign_id}_{int(time.time())}", "agent_name": "Rules Lawyer Agent"}
        ]
        
        for test_session in test_sessions:
            response = requests.post(f"{base_url}/switch-session/{campaign_id}", 
                                   json={
                                       'session_id': test_session['session_id'],
                                       'agent_name': test_session['agent_name']
                                   })
            if response.status_code == 200:
                print(f"✅ Created test session: {test_session['agent_name']}")
            else:
                print(f"❌ Failed to create test session: {test_session['agent_name']}")
    except Exception as e:
        print(f"❌ Error creating test sessions: {e}")
    
    # Test 4: Get available sessions again
    print("\n4. Getting available sessions after creating test sessions...")
    try:
        response = requests.get(f"{base_url}/get-available-sessions/{campaign_id}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['total_sessions']} sessions:")
            for session in data['sessions']:
                print(f"   - {session['agent_name']} ({session['session_id']})")
                print(f"     Description: {session['description']}")
        else:
            print(f"❌ Failed to get available sessions: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting available sessions: {e}")
    
    print("\n✅ Dropdown session switching test completed!")
    print(f"📝 Campaign ID for manual testing: {campaign_id}")
    print("🌐 Open http://localhost:5001/campaign?campaign_id=" + campaign_id + " to test the dropdown UI")

if __name__ == "__main__":
    test_session_dropdown() 