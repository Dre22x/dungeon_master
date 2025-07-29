#!/usr/bin/env python3
"""
Test script to verify pre-invocation session switching functionality.
"""

import requests
import json
import time

def test_pre_invocation_switch():
    """Test the pre-invocation session switching functionality."""
    
    print("🧪 Testing Pre-Invocation Session Switching")
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
    
    # Test 2: Get available sessions (should include root agent session)
    print("\n2. Getting available sessions...")
    try:
        response = requests.get(f"{base_url}/get-available-sessions/{campaign_id}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['total_sessions']} sessions:")
            for session in data['sessions']:
                print(f"   - {session['agent_name']} ({session['session_id']})")
        else:
            print(f"❌ Failed to get available sessions: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting available sessions: {e}")
    
    # Test 3: Simulate a sub-agent invocation (this would trigger pre-invocation switch)
    print("\n3. Simulating sub-agent invocation...")
    try:
        # Create a test sub-agent session ID
        timestamp = int(time.time())
        test_session_id = f"sub_agent_character_creation_{campaign_id}_{timestamp}"
        test_agent_name = "Character Creation Agent"
        
        # Trigger pre-invocation session switch
        response = requests.post(f"{base_url}/switch-session/{campaign_id}", 
                               json={
                                   'session_id': test_session_id,
                                   'agent_name': test_agent_name
                               })
        if response.status_code == 200:
            print(f"✅ Pre-invocation switch triggered for {test_agent_name}")
            print(f"   Session ID: {test_session_id}")
        else:
            print(f"❌ Failed to trigger pre-invocation switch: {response.status_code}")
    except Exception as e:
        print(f"❌ Error simulating sub-agent invocation: {e}")
    
    # Test 4: Get available sessions again (should include the new sub-agent session)
    print("\n4. Getting available sessions after pre-invocation switch...")
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
    
    # Test 5: Test immediate session switching
    print("\n5. Testing immediate session switching...")
    try:
        # Create another test session
        timestamp = int(time.time())
        test_session_id_2 = f"sub_agent_narrative_{campaign_id}_{timestamp}"
        test_agent_name_2 = "Narrative Agent"
        
        response = requests.post(f"{base_url}/switch-session/{campaign_id}", 
                               json={
                                   'session_id': test_session_id_2,
                                   'agent_name': test_agent_name_2
                               })
        if response.status_code == 200:
            print(f"✅ Immediate switch triggered for {test_agent_name_2}")
            print(f"   Session ID: {test_session_id_2}")
        else:
            print(f"❌ Failed to trigger immediate switch: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing immediate session switching: {e}")
    
    print("\n✅ Pre-invocation session switching test completed!")
    print(f"📝 Campaign ID for manual testing: {campaign_id}")
    print("🌐 Open http://localhost:5001/campaign?campaign_id=" + campaign_id + " to test the console switching")
    print("💡 The console should switch to new sessions immediately when agents are invoked")

if __name__ == "__main__":
    test_pre_invocation_switch() 