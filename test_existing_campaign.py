#!/usr/bin/env python3
"""
Test script to create an existing campaign with data and test loading.
"""

import requests
import json
import time

def create_existing_campaign():
    """Create a campaign with some existing data to test loading."""
    base_url = "http://localhost:5001"
    
    print("🧪 Creating Existing Campaign Test")
    print("=" * 50)
    
    # Step 1: Create a new campaign
    print("\n1. Creating a new campaign...")
    response = requests.post(f"{base_url}/new-campaign")
    if response.status_code == 200:
        data = response.json()
        campaign_id = data['campaign_id']
        print(f"✅ New campaign created: {campaign_id}")
    else:
        print(f"❌ Failed to create campaign: {response.status_code}")
        return None
    
    # Step 2: Initialize the campaign (this will start character creation)
    print(f"\n2. Initializing campaign for character creation...")
    response = requests.post(f"{base_url}/initialize-campaign", 
                           json={"campaign_id": campaign_id})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Campaign initialized")
        print(f"   Agent Response: {data['agent_response'][:100]}...")
    else:
        print(f"❌ Failed to initialize campaign: {response.status_code}")
        return None
    
    # Step 3: Send a message to create a character (simulate character creation)
    print(f"\n3. Creating a character...")
    response = requests.post(f"{base_url}/chat", 
                           json={"campaign_id": campaign_id, 
                                "message": "I want to create a human fighter named Thorin"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Character creation message sent")
        print(f"   Agent Response: {data['agent_response'][:100]}...")
    else:
        print(f"❌ Failed to send character creation message: {response.status_code}")
        return None
    
    # Step 4: Send another message to continue character creation
    print(f"\n4. Continuing character creation...")
    response = requests.post(f"{base_url}/chat", 
                           json={"campaign_id": campaign_id, 
                                "message": "I want to be a level 1 fighter with high strength"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Character creation continued")
        print(f"   Agent Response: {data['agent_response'][:100]}...")
    else:
        print(f"❌ Failed to continue character creation: {response.status_code}")
        return None
    
    print(f"\n✅ Campaign {campaign_id} now has some data. You can test loading it.")
    return campaign_id

def test_loading_existing_campaign(campaign_id):
    """Test loading an existing campaign with data."""
    base_url = "http://localhost:5001"
    
    print(f"\n🧪 Testing Loading of Existing Campaign {campaign_id}")
    print("=" * 50)
    
    # Test 1: Load the campaign
    print(f"\n1. Loading campaign {campaign_id}...")
    response = requests.get(f"{base_url}/load-campaign/{campaign_id}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Campaign loaded successfully")
        print(f"   Campaign ID: {data['campaign_id']}")
        print(f"   Agent Response: {data['agent_response'][:200]}...")
    else:
        print(f"❌ Failed to load campaign: {response.status_code}")
        return
    
    # Test 2: Initialize the campaign for chat interface
    print(f"\n2. Initializing campaign for chat interface...")
    response = requests.post(f"{base_url}/initialize-campaign", 
                           json={"campaign_id": campaign_id})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Campaign initialized successfully")
        print(f"   Agent Response: {data['agent_response'][:200]}...")
    else:
        print(f"❌ Failed to initialize campaign: {response.status_code}")
        return
    
    # Test 3: Send a chat message
    print(f"\n3. Sending a chat message...")
    response = requests.post(f"{base_url}/chat", 
                           json={"campaign_id": campaign_id, 
                                "message": "What's happening in our campaign?"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Chat message sent successfully")
        print(f"   Agent Response: {data['agent_response'][:200]}...")
    else:
        print(f"❌ Failed to send chat message: {response.status_code}")
        return
    
    print(f"\n🎉 Existing campaign loading test completed!")

if __name__ == "__main__":
    # First create an existing campaign with data
    campaign_id = create_existing_campaign()
    
    if campaign_id:
        # Wait a moment for the data to be saved
        time.sleep(2)
        
        # Then test loading it
        test_loading_existing_campaign(campaign_id) 