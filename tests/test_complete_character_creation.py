#!/usr/bin/env python3
"""
Test script to complete the full character creation process.
"""

import requests
import json
import time

def complete_character_creation():
    """Complete the full character creation process."""
    base_url = "http://localhost:5001"
    
    print("🧪 Complete Character Creation Test")
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
    
    # Step 2: Initialize the campaign
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
    
    # Step 3: Start character creation
    print(f"\n3. Starting character creation...")
    response = requests.post(f"{base_url}/chat", 
                           json={"campaign_id": campaign_id, 
                                "message": "I want to create a human fighter named Thorin"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Character creation started")
        print(f"   Agent Response: {data['agent_response'][:100]}...")
    else:
        print(f"❌ Failed to start character creation: {response.status_code}")
        return None
    
    # Step 4: Provide character details
    print(f"\n4. Providing character details...")
    response = requests.post(f"{base_url}/chat", 
                           json={"campaign_id": campaign_id, 
                                "message": "I want to be a level 1 fighter with high strength. Use standard array: 15, 14, 13, 12, 10, 8. Put 15 in Strength, 14 in Constitution, 13 in Dexterity, 12 in Wisdom, 10 in Charisma, 8 in Intelligence."})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Character details provided")
        print(f"   Agent Response: {data['agent_response'][:100]}...")
    else:
        print(f"❌ Failed to provide character details: {response.status_code}")
        return None
    
    # Step 5: Choose background
    print(f"\n5. Choosing background...")
    response = requests.post(f"{base_url}/chat", 
                           json={"campaign_id": campaign_id, 
                                "message": "I want the Soldier background"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Background chosen")
        print(f"   Agent Response: {data['agent_response'][:100]}...")
    else:
        print(f"❌ Failed to choose background: {response.status_code}")
        return None
    
    # Step 6: Choose equipment
    print(f"\n6. Choosing equipment...")
    response = requests.post(f"{base_url}/chat", 
                           json={"campaign_id": campaign_id, 
                                "message": "I want a longsword, shield, crossbow with 20 bolts, and chain mail armor"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Equipment chosen")
        print(f"   Agent Response: {data['agent_response'][:100]}...")
    else:
        print(f"❌ Failed to choose equipment: {response.status_code}")
        return None
    
    # Step 7: Finalize character
    print(f"\n7. Finalizing character...")
    response = requests.post(f"{base_url}/chat", 
                           json={"campaign_id": campaign_id, 
                                "message": "Please finalize my character Thorin"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Character finalized")
        print(f"   Agent Response: {data['agent_response'][:100]}...")
    else:
        print(f"❌ Failed to finalize character: {response.status_code}")
        return None
    
    # Step 8: Check if character was saved
    print(f"\n8. Checking if character was saved...")
    time.sleep(2)  # Give time for database operations
    
    response = requests.get(f"{base_url}/load-campaign/{campaign_id}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Campaign loaded")
        print(f"   Agent Response: {data['agent_response'][:100]}...")
    else:
        print(f"❌ Failed to load campaign: {response.status_code}")
        return None
    
    print(f"\n✅ Character creation process completed for campaign {campaign_id}")
    return campaign_id

if __name__ == "__main__":
    campaign_id = complete_character_creation()
    
    if campaign_id:
        print(f"\n🎉 Character creation test completed! Campaign {campaign_id} should now have a character saved.")
        print("You can test loading this campaign to see if it provides a campaign summary instead of starting character creation.") 