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
            'locations',
            'quests',
            'notes'
        ]
        
        for sub_collection in sub_collections:
            # Create an initialization document in each sub-collection
            init_doc = campaign_ref.collection(sub_collection).document('_init')
            init_doc.set({
                'created': True,
                "description": f'Initialization document for {sub_collection} sub-collection',
                'campaign_id': campaign_id,
                'campaign_name': campaign_name
            })
            print(f"   ✅ Created sub-collection: {sub_collection}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error creating campaign structure: {e}")
        return False