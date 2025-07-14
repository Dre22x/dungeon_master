#!/usr/bin/env python3
"""
Test script to verify the campaign loading workflow.
"""

import requests
import json
import time

def test_campaign_loading():
    """Test the campaign loading workflow."""
    base_url = "http://localhost:5001"
    
    print("🧪 Testing Campaign Loading Workflow")
    print("=" * 50)
    
    # Test 1: Create a new campaign
    print("\n1. Creating a new campaign...")
    response = requests.post(f"{base_url}/new-campaign")
    if response.status_code == 200:
        data = response.json()
        campaign_id = data['campaign_id']
        print(f"✅ New campaign created: {campaign_id}")
    else:
        print(f"❌ Failed to create campaign: {response.status_code}")
        return
    
    # Test 2: Load the campaign we just created
    print(f"\n2. Loading campaign {campaign_id}...")
    response = requests.get(f"{base_url}/load-campaign/{campaign_id}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Campaign loaded successfully")
        print(f"   Campaign ID: {data['campaign_id']}")
        print(f"   Agent Response: {data['agent_response'][:100]}...")
    else:
        print(f"❌ Failed to load campaign: {response.status_code}")
        return
    
    # Test 3: Initialize the campaign for chat interface
    print(f"\n3. Initializing campaign for chat interface...")
    response = requests.post(f"{base_url}/initialize-campaign", 
                           json={"campaign_id": campaign_id})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Campaign initialized successfully")
        print(f"   Agent Response: {data['agent_response'][:100]}...")
    else:
        print(f"❌ Failed to initialize campaign: {response.status_code}")
        return
    
    # Test 4: Send a chat message
    print(f"\n4. Sending a chat message...")
    response = requests.post(f"{base_url}/chat", 
                           json={"campaign_id": campaign_id, 
                                "message": "Hello, what's happening in our campaign?"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Chat message sent successfully")
        print(f"   Agent Response: {data['agent_response'][:100]}...")
    else:
        print(f"❌ Failed to send chat message: {response.status_code}")
        return
    
    print(f"\n🎉 All tests passed! Campaign {campaign_id} is working correctly.")

if __name__ == "__main__":
    test_campaign_loading() 