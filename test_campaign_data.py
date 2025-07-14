#!/usr/bin/env python3
"""
Test script to inspect campaign data in the database.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firestore import db_utils

def inspect_campaign_data(campaign_id):
    """Inspect the campaign data in the database."""
    print(f"🔍 Inspecting Campaign Data for {campaign_id}")
    print("=" * 50)
    
    # Load campaign data
    campaign_data = db_utils.load_campaign(campaign_id)
    
    if 'error' in campaign_data:
        print(f"❌ Error loading campaign: {campaign_data['error']}")
        return
    
    print(f"✅ Campaign loaded successfully")
    print(f"   Campaign ID: {campaign_data.get('id', 'Unknown')}")
    print(f"   Status: {campaign_data.get('status', 'Unknown')}")
    print(f"   Context: {campaign_data.get('context', 'No context')}")
    
    # Check sub-collections
    sub_collections = ['characters', 'npcs', 'monsters', 'locations', 'quests', 'notes']
    
    for sub_collection in sub_collections:
        items = campaign_data.get(sub_collection, [])
        print(f"   {sub_collection.capitalize()}: {len(items)} items")
        for item in items:
            if sub_collection == 'characters':
                print(f"     - {item.get('name', 'Unknown')} ({item.get('race', 'Unknown')} {item.get('class', 'Unknown')} Level {item.get('level', 1)})")
            elif sub_collection == 'npcs':
                print(f"     - {item.get('name', 'Unknown')} ({item.get('role', 'Unknown')})")
            elif sub_collection == 'quests':
                print(f"     - {item.get('name', 'Unknown Quest')}")
            else:
                print(f"     - {item.get('name', 'Unknown')}")
    
    # Get campaign stats
    stats = db_utils.get_campaign_stats(campaign_id)
    if 'error' not in stats:
        print(f"\n📊 Campaign Statistics:")
        print(f"   Total items: {stats.get('total_items', 0)}")
        for sub_collection, sub_stats in stats.get('sub_collections', {}).items():
            print(f"   {sub_collection}: {sub_stats.get('document_count', 0)} documents")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        campaign_id = sys.argv[1]
        inspect_campaign_data(campaign_id)
    else:
        print("Usage: python test_campaign_data.py <campaign_id>")
        print("Example: python test_campaign_data.py 8fa5e9b6") 