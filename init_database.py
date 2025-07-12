#!/usr/bin/env python3
"""
Firestore Database Initialization Script
This script initializes the Firestore database for the Dungeon Master application
with a campaign-centric structure where campaigns are the top-level collections
and all other data (characters, npcs, monsters, etc.) are sub-collections within campaigns.
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firestore.database_manager import get_db_client

def create_campaign_structure(db, campaign_id: str, campaign_name: str, dm_name: str = "Dungeon Master"):
    """Creates a campaign with all necessary sub-collections."""
    try:
        # Import firestore for SERVER_TIMESTAMP
        from google.cloud import firestore
        
        # Create the campaign document
        campaign_data = {
            "id": campaign_id,
            "name": campaign_name,
            "dm_name": dm_name,
            "created_date": firestore.SERVER_TIMESTAMP,
            "status": "active",
            "description": f"A D&D campaign run by {dm_name}",
            "settings": {
                "world": "Forgotten Realms",
                "starting_level": 1,
                "max_level": 20
            }
        }
        
        campaign_ref = db.collection('campaigns').document(campaign_id)
        campaign_ref.set(campaign_data)
        print(f"   ✅ Created campaign: {campaign_name}")
        
        # Create sub-collections with initialization documents
        sub_collections = [
            'characters',
            'npcs', 
            'monsters',
            'items',
            'spells',
            'locations',
            'quests',
            'sessions',
            'notes'
        ]
        
        for sub_collection in sub_collections:
            # Create an initialization document in each sub-collection
            init_doc = campaign_ref.collection(sub_collection).document('_init')
            init_doc.set({
                'created': True,
                'description': f'Initialization document for {sub_collection} sub-collection',
                'campaign_id': campaign_id,
                'campaign_name': campaign_name
            })
            print(f"   ✅ Created sub-collection: {sub_collection}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error creating campaign structure: {e}")
        return False

def initialize_database():
    """Initialize the Firestore database with campaign-centric structure."""
    print("=== Firestore Database Initialization (Campaign-Centric) ===")
    
    # Test database connection
    print("\n1. Testing database connection...")
    db = get_db_client()
    
    if not db:
        print("❌ Failed to connect to Firestore. Please check your service account credentials.")
        return False
    
    print("✅ Successfully connected to Firestore!")
    
    # Import firestore for SERVER_TIMESTAMP
    from google.cloud import firestore
    
    # Create sample campaigns
    print("\n2. Creating sample campaigns with sub-collections...")
    
    sample_campaigns = [
        {
            "id": "lost-mines-phandelver",
            "name": "Lost Mine of Phandelver",
            "dm_name": "Dungeon Master"
        },
        {
            "id": "curse-of-strahd",
            "name": "Curse of Strahd",
            "dm_name": "Dungeon Master"
        },
        {
            "id": "homebrew-campaign",
            "name": "Homebrew Adventure",
            "dm_name": "Dungeon Master"
        }
    ]
    
    campaigns_created = 0
    for campaign in sample_campaigns:
        success = create_campaign_structure(
            db, 
            campaign["id"], 
            campaign["name"], 
            campaign["dm_name"]
        )
        if success:
            campaigns_created += 1
    
    # Test creating a sample character in a campaign
    print("\n3. Testing character creation within a campaign...")
    
    try:
        campaign_ref = db.collection('campaigns').document('lost-mines-phandelver')
        
        # Create a sample character
        sample_character = {
            "name": "Boric Stonebeard",
            "race": "Dwarf",
            "class": "Fighter",
            "level": 1,
            "ability_scores": {
                "STR": 15,
                "DEX": 12,
                "CON": 14,
                "INT": 8,
                "WIS": 13,
                "CHA": 10
            },
            "hit_points": 12,
            "armor_class": 15,
            "initiative": 1,
            "speed": 25,
            "proficiencies": ["Longsword", "Shield", "Light Armor", "Medium Armor"],
            "equipment": ["Longsword", "Shield", "Chain Mail", "Crossbow, light"],
            "spells": [],
            "features": ["Fighting Style: Defense", "Second Wind"],
            "background": "Soldier",
            "alignment": "Lawful Good",
            "experience_points": 0,
            "player_name": "Player 1",
            "campaign_id": "lost-mines-phandelver"
        }
        
        # Save character to the campaign's characters sub-collection
        char_ref = campaign_ref.collection('characters').document('boric-stonebeard')
        char_ref.set(sample_character)
        print("   ✅ Created sample character: Boric Stonebeard")
        
        # Test loading the character
        loaded_char = char_ref.get()
        if loaded_char.exists:
            char_data = loaded_char.to_dict()
            print(f"   ✅ Character loaded: {char_data['name']} - Level {char_data['level']} {char_data['race']} {char_data['class']}")
        
    except Exception as e:
        print(f"   ❌ Error creating sample character: {e}")
    
    # Test creating a sample NPC
    print("\n4. Testing NPC creation within a campaign...")
    
    try:
        sample_npc = {
            "name": "Sildar Hallwinter",
            "type": "NPC",
            "race": "Human",
            "class": "Fighter",
            "level": 4,
            "role": "Quest Giver",
            "location": "Phandelver",
            "description": "A retired soldier who hires adventurers to find his missing friend",
            "stats": {
                "STR": 14,
                "DEX": 12,
                "CON": 13,
                "INT": 10,
                "WIS": 11,
                "CHA": 15
            },
            "campaign_id": "lost-mines-phandelver"
        }
        
        npc_ref = campaign_ref.collection('npcs').document('sildar-hallwinter')
        npc_ref.set(sample_npc)
        print("   ✅ Created sample NPC: Sildar Hallwinter")
        
    except Exception as e:
        print(f"   ❌ Error creating sample NPC: {e}")
    
    # Test creating a sample monster
    print("\n5. Testing monster creation within a campaign...")
    
    try:
        sample_monster = {
            "name": "Goblin",
            "type": "Monster",
            "challenge_rating": "1/4",
            "size": "Small",
            "type": "Humanoid",
            "alignment": "Neutral Evil",
            "armor_class": 15,
            "hit_points": 7,
            "speed": 30,
            "stats": {
                "STR": 8,
                "DEX": 14,
                "CON": 10,
                "INT": 10,
                "WIS": 8,
                "CHA": 8
            },
            "actions": ["Scimitar", "Shortbow"],
            "languages": ["Common", "Goblin"],
            "campaign_id": "lost-mines-phandelver"
        }
        
        monster_ref = campaign_ref.collection('monsters').document('goblin')
        monster_ref.set(sample_monster)
        print("   ✅ Created sample monster: Goblin")
        
    except Exception as e:
        print(f"   ❌ Error creating sample monster: {e}")
    
    print("\n=== Database Initialization Complete ===")
    print("✅ Your Firestore database is now ready with campaign-centric structure!")
    print(f"\nCreated {campaigns_created} campaigns with the following sub-collections:")
    sub_collections = ['characters', 'npcs', 'monsters', 'items', 'spells', 'locations', 'quests', 'sessions', 'notes']
    for sub_collection in sub_collections:
        print(f"   - {sub_collection}")
    
    print("\nSample campaigns created:")
    for campaign in sample_campaigns:
        print(f"   - {campaign['name']} (ID: {campaign['id']})")
    
    print("\nDatabase Structure:")
    print("campaigns/")
    print("  ├── {campaign_id}/")
    print("  │   ├── characters/")
    print("  │   ├── npcs/")
    print("  │   ├── monsters/")
    print("  │   ├── items/")
    print("  │   ├── spells/")
    print("  │   ├── locations/")
    print("  │   ├── quests/")
    print("  │   ├── sessions/")
    print("  │   └── notes/")
    
    return True

if __name__ == "__main__":
    try:
        success = initialize_database()
        if success:
            print("\n🎉 Database initialization successful!")
            print("You can now run your Dungeon Master application.")
        else:
            print("\n❌ Database initialization failed.")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during initialization: {e}")
        sys.exit(1) 