#!/usr/bin/env python3
"""
Test script to verify multiple character creation functionality.
This test will create a campaign and then create multiple characters.
"""

import requests
import json
import time

def test_multiple_character_creation():
    """Test the multiple character creation process."""
    base_url = "http://localhost:5001"
    
    print("🧪 Multiple Character Creation Test")
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
    
    # Step 3: Create first character (Fighter)
    print(f"\n3. Creating first character (Fighter)...")
    response = requests.post(f"{base_url}/chat", 
                           json={"campaign_id": campaign_id, 
                                "message": "I want to create a human fighter named Thorin"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ First character creation started")
        print(f"   Agent Response: {data['agent_response'][:100]}...")
    else:
        print(f"❌ Failed to start first character creation: {response.status_code}")
        return None
    
    # Step 4: Complete first character
    print(f"\n4. Completing first character...")
    response = requests.post(f"{base_url}/chat", 
                           json={"campaign_id": campaign_id, 
                                "message": "Please create a complete character for me. I want a human fighter named Thorin with high strength. Use standard array and choose appropriate equipment."})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ First character completed")
        print(f"   Agent Response: {data['agent_response'][:100]}...")
    else:
        print(f"❌ Failed to complete first character: {response.status_code}")
        return None
    
    # Step 5: Check if agent asks about creating another character
    print(f"\n5. Checking if agent asks about multiple characters...")
    response = requests.post(f"{base_url}/chat", 
                           json={"campaign_id": campaign_id, 
                                "message": "What's next?"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Agent response received")
        print(f"   Agent Response: {data['agent_response'][:200]}...")
        
        # Check if the response mentions creating another character
        if "another character" in data['agent_response'].lower() or "create another" in data['agent_response'].lower():
            print("✅ Agent correctly asked about creating another character")
        else:
            print("⚠️  Agent did not ask about creating another character")
    else:
        print(f"❌ Failed to get agent response: {response.status_code}")
        return None
    
    # Step 6: Create second character (Wizard)
    print(f"\n6. Creating second character (Wizard)...")
    response = requests.post(f"{base_url}/chat", 
                           json={"campaign_id": campaign_id, 
                                "message": "Yes, I want to create another character. I want an elf wizard named Elara"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Second character creation started")
        print(f"   Agent Response: {data['agent_response'][:100]}...")
    else:
        print(f"❌ Failed to start second character creation: {response.status_code}")
        return None
    
    # Step 7: Complete second character
    print(f"\n7. Completing second character...")
    response = requests.post(f"{base_url}/chat", 
                           json={"campaign_id": campaign_id, 
                                "message": "Please create a complete character for me. I want an elf wizard named Elara with high intelligence. Use standard array and choose appropriate spells."})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Second character completed")
        print(f"   Agent Response: {data['agent_response'][:100]}...")
    else:
        print(f"❌ Failed to complete second character: {response.status_code}")
        return None
    
    # Step 8: Check if agent asks about creating a third character
    print(f"\n8. Checking if agent asks about creating a third character...")
    response = requests.post(f"{base_url}/chat", 
                           json={"campaign_id": campaign_id, 
                                "message": "What's next?"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Agent response received")
        print(f"   Agent Response: {data['agent_response'][:200]}...")
        
        # Check if the response mentions creating another character
        if "another character" in data['agent_response'].lower() or "create another" in data['agent_response'].lower():
            print("✅ Agent correctly asked about creating another character")
        else:
            print("⚠️  Agent did not ask about creating another character")
    else:
        print(f"❌ Failed to get agent response: {response.status_code}")
        return None
    
    # Step 9: Decline to create a third character
    print(f"\n9. Declining to create a third character...")
    response = requests.post(f"{base_url}/chat", 
                           json={"campaign_id": campaign_id, 
                                "message": "No, I'm done creating characters. Let's start the adventure!"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Character creation process completed")
        print(f"   Agent Response: {data['agent_response'][:200]}...")
    else:
        print(f"❌ Failed to complete character creation: {response.status_code}")
        return None
    
    # Step 10: Check if characters were saved
    print(f"\n10. Checking if characters were saved...")
    time.sleep(2)  # Give time for database operations
    
    response = requests.get(f"{base_url}/campaign/{campaign_id}/characters")
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            characters = data['characters']
            print(f"✅ Characters loaded: {len(characters)} characters found")
            for i, char in enumerate(characters, 1):
                print(f"   Character {i}: {char.get('name', 'Unknown')} - {char.get('race', 'Unknown')} {char.get('class', 'Unknown')}")
        else:
            print(f"❌ Failed to load characters: {data.get('message', 'Unknown error')}")
    else:
        print(f"❌ Failed to get characters: {response.status_code}")
        return None
    
    print(f"\n✅ Multiple character creation test completed for campaign {campaign_id}")
    return campaign_id

def test_campaign_loading_with_multiple_characters():
    """Test loading a campaign that has multiple characters."""
    base_url = "http://localhost:5001"
    
    print("\n🧪 Campaign Loading with Multiple Characters Test")
    print("=" * 50)
    
    # Create a campaign with multiple characters first
    campaign_id = test_multiple_character_creation()
    if not campaign_id:
        print("❌ Cannot test campaign loading - failed to create campaign with multiple characters")
        return
    
    # Wait a moment for database operations
    time.sleep(2)
    
    # Test loading the campaign
    print(f"\n1. Loading campaign with multiple characters...")
    response = requests.get(f"{base_url}/load-campaign/{campaign_id}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Campaign loaded successfully")
        print(f"   Agent Response: {data['agent_response'][:200]}...")
        
        # Check if the response mentions multiple characters
        if "characters" in data['agent_response'].lower() and ("two" in data['agent_response'].lower() or "multiple" in data['agent_response'].lower()):
            print("✅ Agent correctly mentioned multiple characters")
        else:
            print("⚠️  Agent response may not have mentioned multiple characters")
    else:
        print(f"❌ Failed to load campaign: {response.status_code}")
        return None
    
    print(f"\n✅ Campaign loading test completed for campaign {campaign_id}")

if __name__ == "__main__":
    print("🎲 Testing Multiple Character Creation Functionality")
    print("=" * 60)
    
    # Test multiple character creation
    campaign_id = test_multiple_character_creation()
    
    if campaign_id:
        print(f"\n🎉 Multiple character creation test completed! Campaign {campaign_id} should now have multiple characters saved.")
        
        # Test campaign loading
        test_campaign_loading_with_multiple_characters()
        
        print("\n📋 Test Summary:")
        print("- Multiple character creation should work")
        print("- Agent should ask about creating additional characters")
        print("- Campaign should save multiple characters")
        print("- Campaign loading should recognize multiple characters")
    else:
        print("\n❌ Multiple character creation test failed!") 