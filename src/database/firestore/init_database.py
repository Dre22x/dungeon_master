#!/usr/bin/env python3
"""
Firestore Database Initialization Script
This script initializes the Firestore database for the Dungeon Master application.
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_utils import get_db_client, save_character_to_campaign, load_character_from_campaign

def initialize_database():
    """Initialize the Firestore database with basic setup."""
    print("=== Firestore Database Initialization ===")
    
    # Test database connection
    print("\n1. Testing database connection...")
    db = get_db_client()
    
    if not db:
        print("❌ Failed to connect to Firestore. Please check your service account credentials.")
        return False
    
    print("✅ Successfully connected to Firestore!")
    
    # Test basic operations
    print("\n2. Testing basic database operations...")
    
    # Create a test character
    test_character = {
        "name": "TestCharacter",
        "race": "Human",
        "class": "Fighter",
        "level": 1,
        "ability_scores": {
            "STR": 15,
            "DEX": 12,
            "CON": 14,
            "INT": 10,
            "WIS": 8,
            "CHA": 13
        },
        "hit_points": 12,
        "armor_class": 15,
        "initiative": 1,
        "speed": 30,
        "skills": ["Athletics", "Intimidation", "Perception"],
        "proficiencies": ["Longsword", "Shield", "Light Armor", "Medium Armor"],
        "equipment": ["Longsword", "Shield", "Chain Mail", "Crossbow, light"],
        "spells": [],
        "features": ["Fighting Style: Defense", "Second Wind"],
        "background": "Soldier",
        "alignment": "Lawful Good",
        "experience_points": 0
    }
    
    # Save test character
    print("   Saving test character...")
    save_result = save_character_to_campaign("test_campaign", test_character)
    print(f"   {save_result}")
    
    # Load test character
    print("   Loading test character...")
    loaded_character = load_character_from_campaign("test_campaign", "TestCharacter")
    
    if "error" not in loaded_character:
        print("   ✅ Character loaded successfully!")
        print(f"   Character: {loaded_character['name']} - Level {loaded_character['level']} {loaded_character['race']} {loaded_character['class']}")
    else:
        print(f"   ❌ Error loading character: {loaded_character['error']}")
        return False
    
    # Create collections structure
    print("\n3. Setting up database collections...")
    
    collections = ['characters', 'npcs', 'monsters', 'items', 'spells', 'campaigns']
    
    for collection_name in collections:
        try:
            # Create a dummy document to ensure the collection exists
            doc_ref = db.collection(collection_name).document('_init')
            doc_ref.set({
                'created': True,
                'description': f'Initialization document for {collection_name} collection'
            })
            print(f"   ✅ Created collection: {collection_name}")
        except Exception as e:
            print(f"   ⚠️  Warning creating collection {collection_name}: {e}")
    
    print("\n=== Database Initialization Complete ===")
    print("✅ Your Firestore database is now ready to use!")
    print("\nCollections created:")
    for collection in collections:
        print(f"   - {collection}")
    
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