import os
import google.auth
from google.cloud import firestore
from google.oauth2 import service_account

# Set up Google Cloud credentials using service account key
SERVICE_ACCOUNT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "service-account-key.json")

# Set the environment variable for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_PATH

# ==============================================================================
#  DATABASE INITIALIZATION
# ==============================================================================


def get_db_client():
    """Initializes and returns a Firestore client."""
    try:
        # Use service account credentials
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH)
        db = firestore.Client(credentials=credentials)
        print("[DatabaseManager] Firestore client initialized successfully.")
        return db
    except Exception as e:
        print(f"[DatabaseManager] FATAL: Could not initialize Firestore client: {e}")
        print(f"[DatabaseManager] Please ensure the service account key file exists at: {SERVICE_ACCOUNT_PATH}")
        return None

db = get_db_client()

# ==============================================================================
#  CAMPAIGN-CENTRIC DATABASE FUNCTIONS
# ==============================================================================

# --- Campaign Management Tools ---

def create_campaign(campaign_data: dict) -> str:
    """
    Creates a new campaign with all necessary sub-collections.
    Required fields: 'id', 'name'
    Optional fields: 'dm_name', 'description', 'settings', 'status'
    """
    if not db:
        return "Error: Database client is not available."
    if 'id' not in campaign_data or 'name' not in campaign_data:
        return "Error: Campaign data must include 'id' and 'name' fields."

    campaign_id = campaign_data['id']
    campaign_name = campaign_data['name']
    
    try:
        # Import firestore for SERVER_TIMESTAMP
        from google.cloud import firestore
        
        # Set default values if not provided
        campaign_data.setdefault('dm_name', 'Dungeon Master')
        campaign_data.setdefault('status', 'active')
        campaign_data.setdefault('description', f'A D&D campaign run by {campaign_data["dm_name"]}')
        campaign_data.setdefault('settings', {
            'world': 'Forgotten Realms',
            'starting_level': 1,
            'max_level': 20
        })
        campaign_data['created_date'] = firestore.SERVER_TIMESTAMP
        
        # Create the campaign document
        campaign_ref = db.collection('campaigns').document(campaign_id)
        campaign_ref.set(campaign_data)
        
        # Create sub-collections
        sub_collections = ['characters', 'npcs', 'monsters', 'locations', 'quests', 'notes']
        
        for sub_collection in sub_collections:
            init_doc = campaign_ref.collection(sub_collection).document('_init')
            init_doc.set({
                'created': True,
                'description': f'Initialization document for {sub_collection} sub-collection',
                'campaign_id': campaign_id,
                'campaign_name': campaign_name
            })
        
        print(f"[DatabaseManager] Campaign '{campaign_name}' created successfully with {len(sub_collections)} sub-collections.")
        return f"Campaign '{campaign_name}' has been created successfully."
        
    except Exception as e:
        return f"Error creating campaign '{campaign_name}': {e}"

def save_campaign(campaign_id: str, campaign_data: dict) -> str:
    """
    Saves/updates a campaign to the 'campaigns' collection in Firestore.
    """
    if not db:
        return "Error: Database client is not available."
    if 'name' not in campaign_data:
        return "Error: Campaign data must include a 'name' field."

    try:
        campaign_ref = db.collection('campaigns').document(campaign_id)
        campaign_data['id'] = campaign_id
        campaign_ref.set(campaign_data)
        print(f"[DatabaseManager] Campaign '{campaign_data['name']}' saved successfully.")
        return f"Campaign '{campaign_data['name']}' has been saved to the database."
    except Exception as e:
        return f"Error saving campaign '{campaign_id}': {e}"

def get_campaign(campaign_id: str) -> dict:
    """
    Loads a campaign by its ID.
    """
    if not db:
        return {"error": "Database client is not available."}

    try:
        campaign_ref = db.collection('campaigns').document(campaign_id)
        campaign_doc = campaign_ref.get()
        
        if campaign_doc.exists:
            campaign_data = campaign_doc.to_dict()
            print(f"[DatabaseManager] Campaign '{campaign_data.get('name', campaign_id)}' loaded successfully.")
            return campaign_data
        else:
            return {"error": f"Campaign with ID '{campaign_id}' not found."}
    except Exception as e:
        return {"error": f"Error loading campaign '{campaign_id}': {e}"}

def list_all_campaigns() -> dict:
    """
    Lists all campaigns in the database.
    """
    if not db:
        return {"error": "Database client is not available."}
    
    try:
        campaigns_ref = db.collection('campaigns')
        campaigns = campaigns_ref.stream()
        
        campaign_list = []
        for campaign in campaigns:
            campaign_data = campaign.to_dict()
            campaign_data['_id'] = campaign.id
            campaign_list.append(campaign_data)
        
        print(f"[DatabaseManager] Found {len(campaign_list)} campaigns")
        return {
            "campaigns": campaign_list,
            "count": len(campaign_list)
        }
    except Exception as e:
        return {"error": f"Error listing campaigns: {e}"}

def delete_campaign(campaign_id: str) -> str:
    """
    Deletes a campaign and all its sub-collections.
    WARNING: This will delete ALL data associated with the campaign!
    """
    if not db:
        return "Error: Database client is not available."
    
    try:
        campaign_ref = db.collection('campaigns').document(campaign_id)
        campaign_doc = campaign_ref.get()
        
        if not campaign_doc.exists:
            return f"Error: Campaign '{campaign_id}' not found."
        
        # Get campaign name for logging
        campaign_name = campaign_doc.to_dict().get('name', campaign_id)
        
        # Delete all sub-collections
        sub_collections = ['characters', 'npcs', 'monsters', 'locations', 'quests', 'notes']
        deleted_count = 0
        
        for sub_collection in sub_collections:
            docs = campaign_ref.collection(sub_collection).stream()
            for doc in docs:
                doc.reference.delete()
                deleted_count += 1
        
        # Delete the campaign document
        campaign_ref.delete()
        
        print(f"[DatabaseManager] Campaign '{campaign_name}' and {deleted_count} sub-documents deleted successfully.")
        return f"Campaign '{campaign_name}' has been deleted successfully."
        
    except Exception as e:
        return f"Error deleting campaign '{campaign_id}': {e}"

# --- Character Management (Campaign-Specific) ---

def save_character_to_campaign(campaign_id: str, character_data: dict) -> str:
    """
    Saves a character to a specific campaign's characters sub-collection.
    """
    if not db:
        return "Error: Database client is not available."
    if 'name' not in character_data:
        return "Error: Character data must include a 'name' field."

    char_name = character_data['name']
    doc_id = char_name.lower().replace(' ', '-')
    
    try:
        char_ref = db.collection('campaigns').document(campaign_id).collection('characters').document(doc_id)
        character_data['campaign_id'] = campaign_id
        char_ref.set(character_data)
        print(f"[DatabaseManager] Character '{char_name}' saved to campaign '{campaign_id}' successfully.")
        return f"Character '{char_name}' has been saved to campaign '{campaign_id}'."
    except Exception as e:
        return f"Error saving character '{char_name}' to campaign '{campaign_id}': {e}"

def load_character_from_campaign(campaign_id: str, character_name: str) -> dict:
    """
    Loads a character from a specific campaign's characters sub-collection.
    """
    if not db:
        return {"error": "Database client is not available."}

    doc_id = character_name.lower().replace(' ', '-')
    
    try:
        char_ref = db.collection('campaigns').document(campaign_id).collection('characters').document(doc_id)
        char_doc = char_ref.get()
        
        if char_doc.exists:
            char_data = char_doc.to_dict()
            print(f"[DatabaseManager] Character '{character_name}' loaded from campaign '{campaign_id}' successfully.")
            return char_data
        else:
            return {"error": f"Character '{character_name}' not found in campaign '{campaign_id}'."}
    except Exception as e:
        return {"error": f"Error loading character '{character_name}' from campaign '{campaign_id}': {e}"}

def list_characters_in_campaign(campaign_id: str) -> dict:
    """
    Lists all characters in a specific campaign.
    """
    if not db:
        return {"error": "Database client is not available."}
    
    try:
        chars_ref = db.collection('campaigns').document(campaign_id).collection('characters')
        characters = chars_ref.stream()
        
        char_list = []
        for char in characters:
            if char.id != '_init':  # Skip initialization document
                char_data = char.to_dict()
                char_data['_id'] = char.id
                char_list.append(char_data)
        
        print(f"[DatabaseManager] Found {len(char_list)} characters in campaign '{campaign_id}'")
        return {
            "campaign_id": campaign_id,
            "characters": char_list,
            "count": len(char_list)
        }
    except Exception as e:
        return {"error": f"Error listing characters in campaign '{campaign_id}': {e}"}

def delete_character_from_campaign(campaign_id: str, character_name: str) -> str:
    """
    Deletes a character from a specific campaign.
    """
    if not db:
        return "Error: Database client is not available."

    doc_id = character_name.lower().replace(' ', '-')
    
    try:
        char_ref = db.collection('campaigns').document(campaign_id).collection('characters').document(doc_id)
        char_doc = char_ref.get()
        
        if not char_doc.exists:
            return f"Error: Character '{character_name}' not found in campaign '{campaign_id}'."
        
        char_ref.delete()
        print(f"[DatabaseManager] Character '{character_name}' deleted from campaign '{campaign_id}' successfully.")
        return f"Character '{character_name}' has been deleted from campaign '{campaign_id}'."
        
    except Exception as e:
        return f"Error deleting character '{character_name}' from campaign '{campaign_id}': {e}"

# --- NPC Management (Campaign-Specific) ---

def save_npc_to_campaign(campaign_id: str, npc_data: dict) -> str:
    """
    Saves an NPC to a specific campaign's npcs sub-collection.
    """
    if not db:
        return "Error: Database client is not available."
    if 'name' not in npc_data:
        return "Error: NPC data must include a 'name' field."

    npc_name = npc_data['name']
    doc_id = npc_name.lower().replace(' ', '-')
    
    try:
        npc_ref = db.collection('campaigns').document(campaign_id).collection('npcs').document(doc_id)
        npc_data['campaign_id'] = campaign_id
        npc_ref.set(npc_data)
        print(f"[DatabaseManager] NPC '{npc_name}' saved to campaign '{campaign_id}' successfully.")
        return f"NPC '{npc_name}' has been saved to campaign '{campaign_id}'."
    except Exception as e:
        return f"Error saving NPC '{npc_name}' to campaign '{campaign_id}': {e}"

def load_npc_from_campaign(campaign_id: str, npc_name: str) -> dict:
    """
    Loads an NPC from a specific campaign's npcs sub-collection.
    """
    if not db:
        return {"error": "Database client is not available."}

    doc_id = npc_name.lower().replace(' ', '-')
    
    try:
        npc_ref = db.collection('campaigns').document(campaign_id).collection('npcs').document(doc_id)
        npc_doc = npc_ref.get()
        
        if npc_doc.exists:
            npc_data = npc_doc.to_dict()
            print(f"[DatabaseManager] NPC '{npc_name}' loaded from campaign '{campaign_id}' successfully.")
            return npc_data
        else:
            return {"error": f"NPC '{npc_name}' not found in campaign '{campaign_id}'."}
    except Exception as e:
        return {"error": f"Error loading NPC '{npc_name}' from campaign '{campaign_id}': {e}"}

def list_npcs_in_campaign(campaign_id: str) -> dict:
    """
    Lists all NPCs in a specific campaign.
    """
    if not db:
        return {"error": "Database client is not available."}
    
    try:
        npcs_ref = db.collection('campaigns').document(campaign_id).collection('npcs')
        npcs = npcs_ref.stream()
        
        npc_list = []
        for npc in npcs:
            if npc.id != '_init':  # Skip initialization document
                npc_data = npc.to_dict()
                npc_data['_id'] = npc.id
                npc_list.append(npc_data)
        
        print(f"[DatabaseManager] Found {len(npc_list)} NPCs in campaign '{campaign_id}'")
        return {
            "campaign_id": campaign_id,
            "npcs": npc_list,
            "count": len(npc_list)
        }
    except Exception as e:
        return {"error": f"Error listing NPCs in campaign '{campaign_id}': {e}"}

# --- Monster Management (Campaign-Specific) ---

def save_monster_to_campaign(campaign_id: str, monster_data: dict) -> str:
    """
    Saves a monster to a specific campaign's monsters sub-collection.
    """
    if not db:
        return "Error: Database client is not available."
    if 'name' not in monster_data:
        return "Error: Monster data must include a 'name' field."

    monster_name = monster_data['name']
    doc_id = monster_name.lower().replace(' ', '-')
    
    try:
        monster_ref = db.collection('campaigns').document(campaign_id).collection('monsters').document(doc_id)
        monster_data['campaign_id'] = campaign_id
        monster_ref.set(monster_data)
        print(f"[DatabaseManager] Monster '{monster_name}' saved to campaign '{campaign_id}' successfully.")
        return f"Monster '{monster_name}' has been saved to campaign '{campaign_id}'."
    except Exception as e:
        return f"Error saving monster '{monster_name}' to campaign '{campaign_id}': {e}"

def load_monster_from_campaign(campaign_id: str, monster_name: str) -> dict:
    """
    Loads a monster from a specific campaign's monsters sub-collection.
    """
    if not db:
        return {"error": "Database client is not available."}

    doc_id = monster_name.lower().replace(' ', '-')
    
    try:
        monster_ref = db.collection('campaigns').document(campaign_id).collection('monsters').document(doc_id)
        monster_doc = monster_ref.get()
        
        if monster_doc.exists:
            monster_data = monster_doc.to_dict()
            print(f"[DatabaseManager] Monster '{monster_name}' loaded from campaign '{campaign_id}' successfully.")
            return monster_data
        else:
            return {"error": f"Monster '{monster_name}' not found in campaign '{campaign_id}'."}
    except Exception as e:
        return {"error": f"Error loading monster '{monster_name}' from campaign '{campaign_id}': {e}"}

def list_monsters_in_campaign(campaign_id: str) -> dict:
    """
    Lists all monsters in a specific campaign.
    """
    if not db:
        return {"error": "Database client is not available."}
    
    try:
        monsters_ref = db.collection('campaigns').document(campaign_id).collection('monsters')
        monsters = monsters_ref.stream()
        
        monster_list = []
        for monster in monsters:
            if monster.id != '_init':  # Skip initialization document
                monster_data = monster.to_dict()
                monster_data['_id'] = monster.id
                monster_list.append(monster_data)
        
        print(f"[DatabaseManager] Found {len(monster_list)} monsters in campaign '{campaign_id}'")
        return {
            "campaign_id": campaign_id,
            "monsters": monster_list,
            "count": len(monster_list)
        }
    except Exception as e:
        return {"error": f"Error listing monsters in campaign '{campaign_id}': {e}"}

# --- Character Item & Spell Management ---

def add_item_to_character(campaign_id: str, character_name: str, item_data: dict) -> str:
    """
    Adds an item to a character's equipment/inventory.
    """
    if not db:
        return "Error: Database client is not available."
    if 'name' not in item_data:
        return "Error: Item data must include a 'name' field."

    try:
        # Load the character first
        char_data = load_character_from_campaign(campaign_id, character_name)
        if 'error' in char_data:
            return f"Error: {char_data['error']}"
        
        # Initialize equipment list if it doesn't exist
        if 'equipment' not in char_data:
            char_data['equipment'] = []
        
        # Add the item
        char_data['equipment'].append(item_data)
        
        # Save the updated character
        return save_character_to_campaign(campaign_id, char_data)
        
    except Exception as e:
        return f"Error adding item to character '{character_name}': {e}"

def remove_item_from_character(campaign_id: str, character_name: str, item_name: str) -> str:
    """
    Removes an item from a character's equipment/inventory.
    """
    if not db:
        return "Error: Database client is not available."

    try:
        # Load the character first
        char_data = load_character_from_campaign(campaign_id, character_name)
        if 'error' in char_data:
            return f"Error: {char_data['error']}"
        
        # Check if equipment exists
        if 'equipment' not in char_data:
            return f"Error: Character '{character_name}' has no equipment."
        
        # Find and remove the item
        original_count = len(char_data['equipment'])
        char_data['equipment'] = [item for item in char_data['equipment'] if item.get('name') != item_name]
        
        if len(char_data['equipment']) == original_count:
            return f"Error: Item '{item_name}' not found in character '{character_name}' equipment."
        
        # Save the updated character
        return save_character_to_campaign(campaign_id, char_data)
        
    except Exception as e:
        return f"Error removing item from character '{character_name}': {e}"

def add_spell_to_character(campaign_id: str, character_name: str, spell_data: dict) -> str:
    """
    Adds a spell to a character's spell list.
    """
    if not db:
        return "Error: Database client is not available."
    if 'name' not in spell_data:
        return "Error: Spell data must include a 'name' field."

    try:
        # Load the character first
        char_data = load_character_from_campaign(campaign_id, character_name)
        if 'error' in char_data:
            return f"Error: {char_data['error']}"
        
        # Initialize spells list if it doesn't exist
        if 'spells' not in char_data:
            char_data['spells'] = []
        
        # Add the spell
        char_data['spells'].append(spell_data)
        
        # Save the updated character
        return save_character_to_campaign(campaign_id, char_data)
        
    except Exception as e:
        return f"Error adding spell to character '{character_name}': {e}"

def remove_spell_from_character(campaign_id: str, character_name: str, spell_name: str) -> str:
    """
    Removes a spell from a character's spell list.
    """
    if not db:
        return "Error: Database client is not available."

    try:
        # Load the character first
        char_data = load_character_from_campaign(campaign_id, character_name)
        if 'error' in char_data:
            return f"Error: {char_data['error']}"
        
        # Check if spells exist
        if 'spells' not in char_data:
            return f"Error: Character '{character_name}' has no spells."
        
        # Find and remove the spell
        original_count = len(char_data['spells'])
        char_data['spells'] = [spell for spell in char_data['spells'] if spell.get('name') != spell_name]
        
        if len(char_data['spells']) == original_count:
            return f"Error: Spell '{spell_name}' not found in character '{character_name}' spell list."
        
        # Save the updated character
        return save_character_to_campaign(campaign_id, char_data)
        
    except Exception as e:
        return f"Error removing spell from character '{character_name}': {e}"

def get_character_items(campaign_id: str, character_name: str) -> dict:
    """
    Gets all items/equipment for a character.
    """
    if not db:
        return {"error": "Database client is not available."}

    try:
        char_data = load_character_from_campaign(campaign_id, character_name)
        if 'error' in char_data:
            return char_data
        
        items = char_data.get('equipment', [])
        return {
            "character_name": character_name,
            "campaign_id": campaign_id,
            "items": items,
            "count": len(items)
        }
        
    except Exception as e:
        return {"error": f"Error getting items for character '{character_name}': {e}"}

def get_character_spells(campaign_id: str, character_name: str) -> dict:
    """
    Gets all spells for a character.
    """
    if not db:
        return {"error": "Database client is not available."}

    try:
        char_data = load_character_from_campaign(campaign_id, character_name)
        if 'error' in char_data:
            return char_data
        
        spells = char_data.get('spells', [])
        return {
            "character_name": character_name,
            "campaign_id": campaign_id,
            "spells": spells,
            "count": len(spells)
        }
        
    except Exception as e:
        return {"error": f"Error getting spells for character '{character_name}': {e}"}

# --- Campaign Statistics ---

def get_campaign_stats(campaign_id: str) -> dict:
    """
    Gets statistics about a specific campaign including counts of all sub-collections.
    """
    if not db:
        return {"error": "Database client is not available."}
    
    try:
        campaign_ref = db.collection('campaigns').document(campaign_id)
        campaign_doc = campaign_ref.get()
        
        if not campaign_doc.exists:
            return {"error": f"Campaign '{campaign_id}' not found."}
        
        campaign_data = campaign_doc.to_dict()
        sub_collections = ['characters', 'npcs', 'monsters', 'locations', 'quests', 'notes']
        
        stats = {
            "campaign_id": campaign_id,
            "campaign_name": campaign_data.get('name', 'Unknown'),
            "dm_name": campaign_data.get('dm_name', 'Unknown'),
            "status": campaign_data.get('status', 'Unknown'),
            "sub_collections": {}
        }
        
        total_items = 0
        
        for sub_collection in sub_collections:
            try:
                docs = list(campaign_ref.collection(sub_collection).stream())
                # Filter out initialization documents
                actual_docs = [doc for doc in docs if doc.id != '_init']
                doc_count = len(actual_docs)
                total_items += doc_count
                
                stats["sub_collections"][sub_collection] = {
                    "document_count": doc_count,
                    "documents": [doc.id for doc in actual_docs]
                }
            except Exception as e:
                stats["sub_collections"][sub_collection] = {
                    "document_count": 0,
                    "error": str(e)
                }
        
        stats["total_items"] = total_items
        
        print(f"[DatabaseManager] Campaign '{campaign_data.get('name', campaign_id)}' stats: {total_items} total items")
        return stats
        
    except Exception as e:
        return {"error": f"Error getting campaign stats for '{campaign_id}': {e}"}

# ==============================================================================
#  EXAMPLE USAGE (for testing the script from the command line)
# ==============================================================================
if __name__ == '__main__':
    print("\n--- Testing Campaign-Centric Database Utils ---")
    
    # Example: List all campaigns
    print("\n1. Listing all campaigns...")
    campaigns = list_all_campaigns()
    if 'error' not in campaigns:
        print(f"   Found {campaigns['count']} campaigns:")
        for campaign in campaigns['campaigns']:
            print(f"     - {campaign.get('name', 'Unknown')} (ID: {campaign.get('id', 'Unknown')})")
    else:
        print(f"   Error: {campaigns['error']}")
    
    # Example: Get campaign stats
    print("\n2. Getting campaign stats...")
    stats = get_campaign_stats('lost-mines-phandelver')
    if 'error' not in stats:
        print(f"   Campaign: {stats['campaign_name']}")
        print(f"   DM: {stats['dm_name']}")
        print(f"   Total items: {stats['total_items']}")
        for sub_collection, sub_stats in stats['sub_collections'].items():
            print(f"     {sub_collection}: {sub_stats['document_count']} items")
    else:
        print(f"   Error: {stats['error']}")
    
    # Example: List characters in a campaign
    print("\n3. Listing characters in campaign...")
    characters = list_characters_in_campaign('lost-mines-phandelver')
    if 'error' not in characters:
        print(f"   Found {characters['count']} characters:")
        for char in characters['characters']:
            print(f"     - {char.get('name', 'Unknown')} (Level {char.get('level', '?')} {char.get('class', 'Unknown')})")
    else:
        print(f"   Error: {characters['error']}")
    
    # Example: Create a new campaign
    print("\n4. Creating a new test campaign...")
    new_campaign = {
        "id": "test-campaign",
        "name": "Test Campaign",
        "dm_name": "Test DM",
        "description": "A test campaign for demonstration"
    }
    result = create_campaign(new_campaign)
    print(f"   {result}")
    
    # Example: Save a character to the new campaign
    print("\n5. Saving a character to the new campaign...")
    test_character = {
        "name": "Test Character",
        "race": "Human",
        "class": "Wizard",
        "level": 1,
        "ability_scores": {"STR": 8, "DEX": 12, "CON": 10, "INT": 16, "WIS": 14, "CHA": 13}
    }
    save_result = save_character_to_campaign('test-campaign', test_character)
    print(f"   {save_result}")
    
    # Example: Add items to character
    print("\n6. Adding items to character...")
    sword_item = {
        "name": "Longsword",
        "type": "Weapon",
        "damage": "1d8 slashing",
        "properties": ["Versatile (1d10)"]
    }
    add_item_result = add_item_to_character('test-campaign', 'Test Character', sword_item)
    print(f"   {add_item_result}")
    
    # Example: Add spell to character
    print("\n7. Adding spell to character...")
    fireball_spell = {
        "name": "Fireball",
        "level": 3,
        "school": "Evocation",
        "casting_time": "1 action",
        "range": "150 feet",
        "components": ["V", "S", "M (a tiny ball of bat guano and sulfur)"],
        "duration": "Instantaneous",
        "description": "A bright streak flashes from your pointing finger to a point you choose within range..."
    }
    add_spell_result = add_spell_to_character('test-campaign', 'Test Character', fireball_spell)
    print(f"   {add_spell_result}")
    
    # Example: Get character items and spells
    print("\n8. Getting character items and spells...")
    items_result = get_character_items('test-campaign', 'Test Character')
    if 'error' not in items_result:
        print(f"   Character has {items_result['count']} items:")
        for item in items_result['items']:
            print(f"     - {item.get('name', 'Unknown')} ({item.get('type', 'Unknown')})")
    
    spells_result = get_character_spells('test-campaign', 'Test Character')
    if 'error' not in spells_result:
        print(f"   Character has {spells_result['count']} spells:")
        for spell in spells_result['spells']:
            print(f"     - {spell.get('name', 'Unknown')} (Level {spell.get('level', '?')})")
    
    print("\nUpdated Database Structure:")
    print("campaigns/")
    print("  ├── {campaign_id}/")
    print("  │   ├── characters/")
    print("  │   │   └── {character_name}/")
    print("  │   │       ├── equipment/ (items as part of character data)")
    print("  │   │       └── spells/ (spells as part of character data)")
    print("  │   ├── npcs/")
    print("  │   ├── monsters/")
    print("  │   ├── locations/")
    print("  │   ├── quests/")
    print("  │   └── notes/")
