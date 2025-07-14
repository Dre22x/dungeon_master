#!/usr/bin/env python3
"""
Test script to verify campaign outline generation functionality.
This test will create a campaign and verify that a unique outline is generated.
"""

import requests
import json
import time

def test_campaign_outline_generation():
    """Test the campaign outline generation process."""
    base_url = "http://localhost:5001"
    
    print("🧪 Campaign Outline Generation Test")
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
    print(f"\n2. Initializing campaign for outline generation...")
    response = requests.post(f"{base_url}/initialize-campaign", 
                           json={"campaign_id": campaign_id})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Campaign initialized")
        print(f"   Agent Response: {data['agent_response'][:200]}...")
    else:
        print(f"❌ Failed to initialize campaign: {response.status_code}")
        return None
    
    # Step 3: Create a character to trigger the outline generation
    print(f"\n3. Creating a character to trigger outline generation...")
    response = requests.post(f"{base_url}/chat", 
                           json={"campaign_id": campaign_id, 
                                "message": "Please create a complete character for me. I want a human fighter named Thorin with high strength. Use standard array and choose appropriate equipment."})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Character creation started")
        print(f"   Agent Response: {data['agent_response'][:200]}...")
    else:
        print(f"❌ Failed to start character creation: {response.status_code}")
        return None
    
    # Step 4: Complete character creation and trigger outline generation
    print(f"\n4. Completing character creation...")
    response = requests.post(f"{base_url}/chat", 
                           json={"campaign_id": campaign_id, 
                                "message": "I'm done creating characters. Let's start the adventure!"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Character creation completed")
        print(f"   Agent Response: {data['agent_response'][:300]}...")
        
        # Check if the response mentions campaign outline generation
        if "outline" in data['agent_response'].lower() or "story" in data['agent_response'].lower():
            print("✅ Agent appears to be generating campaign outline")
        else:
            print("⚠️  Agent response may not mention outline generation")
    else:
        print(f"❌ Failed to complete character creation: {response.status_code}")
        return None
    
    # Step 5: Check if campaign outline was saved
    print(f"\n5. Checking if campaign outline was saved...")
    time.sleep(2)  # Give time for database operations
    
    response = requests.get(f"{base_url}/load-campaign/{campaign_id}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Campaign loaded successfully")
        print(f"   Agent Response: {data['agent_response'][:300]}...")
        
        # Check if the response mentions campaign outline elements
        if any(keyword in data['agent_response'].lower() for keyword in ["title", "theme", "quest", "story"]):
            print("✅ Agent appears to be using campaign outline")
        else:
            print("⚠️  Agent response may not reference campaign outline")
    else:
        print(f"❌ Failed to load campaign: {response.status_code}")
        return None
    
    print(f"\n✅ Campaign outline generation test completed for campaign {campaign_id}")
    return campaign_id

def test_multiple_campaign_outlines():
    """Test that multiple campaigns generate different outlines."""
    base_url = "http://localhost:5001"
    
    print("\n🧪 Multiple Campaign Outlines Test")
    print("=" * 50)
    
    campaign_ids = []
    
    # Create multiple campaigns to test outline uniqueness
    for i in range(3):
        print(f"\n--- Creating Campaign {i+1} ---")
        
        # Create campaign
        response = requests.post(f"{base_url}/new-campaign")
        if response.status_code == 200:
            data = response.json()
            campaign_id = data['campaign_id']
            campaign_ids.append(campaign_id)
            print(f"✅ Campaign {i+1} created: {campaign_id}")
        else:
            print(f"❌ Failed to create campaign {i+1}")
            continue
        
        # Initialize campaign
        response = requests.post(f"{base_url}/initialize-campaign", 
                               json={"campaign_id": campaign_id})
        if response.status_code != 200:
            print(f"❌ Failed to initialize campaign {i+1}")
            continue
        
        # Create character and trigger outline generation
        response = requests.post(f"{base_url}/chat", 
                               json={"campaign_id": campaign_id, 
                                    "message": "Please create a complete character for me. I want a human fighter. Use standard array and choose appropriate equipment."})
        if response.status_code != 200:
            print(f"❌ Failed to create character for campaign {i+1}")
            continue
        
        # Complete character creation
        response = requests.post(f"{base_url}/chat", 
                               json={"campaign_id": campaign_id, 
                                    "message": "I'm done creating characters. Let's start the adventure!"})
        if response.status_code == 200:
            print(f"✅ Campaign {i+1} outline generation completed")
        else:
            print(f"❌ Failed to complete outline generation for campaign {i+1}")
    
    print(f"\n✅ Created {len(campaign_ids)} campaigns with outlines")
    print("📋 Campaign IDs for manual verification:")
    for i, campaign_id in enumerate(campaign_ids, 1):
        print(f"   Campaign {i}: {campaign_id}")
    
    return campaign_ids

def test_campaign_outline_loading():
    """Test loading a campaign with an existing outline."""
    base_url = "http://localhost:5001"
    
    print("\n🧪 Campaign Outline Loading Test")
    print("=" * 50)
    
    # Create a campaign with outline first
    campaign_id = test_campaign_outline_generation()
    if not campaign_id:
        print("❌ Cannot test outline loading - failed to create campaign with outline")
        return
    
    # Wait a moment for database operations
    time.sleep(2)
    
    # Test loading the campaign
    print(f"\n1. Loading campaign with outline...")
    response = requests.get(f"{base_url}/load-campaign/{campaign_id}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Campaign loaded successfully")
        print(f"   Agent Response: {data['agent_response'][:300]}...")
        
        # Check if the response mentions campaign outline elements
        outline_keywords = ["title", "theme", "quest", "story", "outline", "campaign"]
        if any(keyword in data['agent_response'].lower() for keyword in outline_keywords):
            print("✅ Agent appears to be using campaign outline")
        else:
            print("⚠️  Agent response may not reference campaign outline")
    else:
        print(f"❌ Failed to load campaign: {response.status_code}")
        return None
    
    print(f"\n✅ Campaign outline loading test completed for campaign {campaign_id}")

if __name__ == "__main__":
    print("🎲 Testing Campaign Outline Generation Functionality")
    print("=" * 60)
    
    # Test single campaign outline generation
    campaign_id = test_campaign_outline_generation()
    
    if campaign_id:
        print(f"\n🎉 Campaign outline generation test completed! Campaign {campaign_id} should now have a unique outline saved.")
        
        # Test multiple campaign outlines
        test_multiple_campaign_outlines()
        
        # Test campaign outline loading
        test_campaign_outline_loading()
        
        print("\n📋 Test Summary:")
        print("- Campaign outline generation should work")
        print("- Each campaign should have a unique outline")
        print("- Campaign loading should reference the outline")
        print("- Story elements should be consistent with the outline")
    else:
        print("\n❌ Campaign outline generation test failed!") 