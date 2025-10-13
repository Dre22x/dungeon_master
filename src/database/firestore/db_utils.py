import os
from google.cloud import firestore
from google.oauth2 import service_account

# Set up Google Cloud credentials using service account key
SERVICE_ACCOUNT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "config", "service-account-key.json")

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

def create_campaign(campaign_id: str, status: str = 'active') -> str:
    """
    Creates a new entry for a campaign in the 'campaigns' collection in the database.

    Args:
        campaign_id: str - Unique identifier for the campaign
        status: str - Campaign status (default: 'active')
    """
    if not db:
        return "Error: Database client is not available."
        
    # Create the campaign document
    campaign_ref = db.collection('campaigns').document(campaign_id)
    campaign_ref.set({
        'id': campaign_id,
        'status': status,
        'created_date': firestore.SERVER_TIMESTAMP
    })
        
    # Create sub-collections
    sub_collections = ['context', 'last_saved', 'characters', 'npcs', 'monsters']
        
    for sub_collection in sub_collections:
        init_doc = campaign_ref.collection(sub_collection).document('_init')
        init_doc.set({
            'created': True,
            'campaign_id': campaign_id,
        })
        
    print(f"[DatabaseManager] Campaign '{campaign_id}' created successfully with {len(sub_collections)} sub-collections.")
    return f"Campaign '{campaign_id}' has been created successfully."

def save_campaign(campaign_id: str, context: str) -> str:
    """
    Saves/updates a campaign to the 'campaigns' collection in Firestore.
    Args:
        campaign_id: str - The ID of the campaign to save.
        context: str - The context of the campaign. This is a freeform summary of the main events of the campaign so far.
    """
    if not db:
        return "Error: Database client is not available."

    try:
        campaign_ref = db.collection('campaigns').document(campaign_id)
        
        # Check if campaign exists
        campaign_doc = campaign_ref.get()
        if not campaign_doc.exists:
            return f"Error: Campaign '{campaign_id}' not found."
        
        # Update the campaign with context and timestamp
        update_data = {
            'context': context,
            'last_saved': firestore.SERVER_TIMESTAMP,
        }
        
        campaign_ref.update(update_data)
        print(f"[DatabaseManager] Campaign '{campaign_id}' context updated successfully.")
        return f"Campaign '{campaign_id}' has been updated successfully."

    except Exception as e:
        return f"Error saving campaign '{campaign_id}': {e}"

def load_campaign(campaign_id: str) -> dict:
    """
    Loads a campaign by its ID. This includes the context, characters, npcs, monsters, locations, quests, and notes.
    Args:
        campaign_id: str - The ID of the campaign to load.
    """
    if not db:
        return {"error": "Database client is not available."}

    try:
        campaign_ref = db.collection('campaigns').document(campaign_id)
        campaign_doc = campaign_ref.get()
        
        if campaign_doc.exists:
            campaign_data = campaign_doc.to_dict()
            
            # Load all sub-collections
            sub_collections = ['characters', 'npcs', 'monsters', 'locations', 'quests', 'notes']
            
            for sub_collection in sub_collections:
                try:
                    docs = campaign_ref.collection(sub_collection).stream()
                    collection_data = []
                    for doc in docs:
                        if doc.id != '_init':  # Skip the initialization document
                            doc_data = doc.to_dict()
                            doc_data['_id'] = doc.id
                            collection_data.append(doc_data)
                    campaign_data[sub_collection] = collection_data
                except Exception as e:
                    print(f"[DatabaseManager] Warning: Could not load {sub_collection} for campaign {campaign_id}: {e}")
                    campaign_data[sub_collection] = []
            
            print(f"[DatabaseManager] Campaign '{campaign_data.get('name', campaign_id)}' loaded successfully with all sub-collections.")
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

def change_game_state(campaign_id: str, state: str) -> str:
    """
    Changes the state of a campaign.
    """
    if not db:
        return "Error: Database client is not available."
    if state not in ['exploration', 'combat', 'dialogue']:
        return "Error: Invalid state. Must be one of: exploration, combat, dialogue."
    try:
        campaign_ref = db.collection('campaigns').document(campaign_id)
        campaign_ref.update({'state': state})
        return f"Campaign '{campaign_id}' state changed to '{state}' successfully."
    except Exception as e:
        return f"Error changing campaign '{campaign_id}' state to '{state}': {e}"
    
def get_game_state(campaign_id: str) -> str:
    """
    Gets the state of a campaign.
    """
    if not db:
        return "Error: Database client is not available."
    try:
        campaign_ref = db.collection('campaigns').document(campaign_id)
        campaign_doc = campaign_ref.get()
        if campaign_doc.exists:
            return campaign_doc.to_dict().get('state', 'unknown')
        else:
            return "Error: Campaign not found."
    except Exception as e:
        return f"Error getting campaign '{campaign_id}' state: {e}"

# --- Character Management (Campaign-Specific) ---

def save_character_to_campaign(campaign_id: str, character_data: dict) -> str:
    """
    Saves a character to a specific campaign's characters sub-collection.
    Args:
        campaign_id: str - The ID of the campaign to save the character to.
        character_data: dict - The data to save for the character.
            -   name: str - The name of the character.
            -   class: str - The class of the character.
            -   level: int - The level of the character.
            -   race: str - The race of the character.
            -   background: str - The background of the character.
            -   alignment: str - The alignment of the character.
            -   experience: int - The experience points of the character.
            -   ability_scores: dict - The ability scores of the character.
                -   strength: int - The strength score of the character.
                -   dexterity: int - The dexterity score of the character.
                -   constitution: int - The constitution score of the character.
                -   intelligence: int - The intelligence score of the character.
                -   wisdom: int - The wisdom score of the character.
                -   charisma: int - The charisma score of the character.
            -   inventory: list - The inventory of the character.
            -   spells: list - The spells of the character.
            -   equipment: list - The equipment of the character.
            -   notes: str - The notes of the character.
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

def save_npc_to_campaign(campaign_id: str, name: str, npc_type: str, 
                         description: str, location: str, 
                         role: str, notes: str) -> str:
    """
    Saves an NPC to a specific campaign's npcs sub-collection.
    
    Args:
        campaign_id: str - The ID of the campaign to save the NPC to
        name: str - The name of the NPC
        npc_type: str - The type of NPC (e.g., 'merchant', 'quest_giver', 'enemy', 'ally')
        description: str - Physical description and personality of the NPC
        location: str - Where the NPC can typically be found
        role: str - The NPC's role in the campaign or story
        notes: str - Additional notes about the NPC
    """
    if not db:
        return "Error: Database client is not available."
    if not name:
        return "Error: NPC name is required."

    doc_id = name.lower().replace(' ', '-')
    
    try:
        # Create NPC data dictionary
        npc_data = {
            'name': name,
            'campaign_id': campaign_id
        }
        
        # Add optional fields if provided
        if npc_type:
            npc_data['npc_type'] = npc_type
        if description:
            npc_data['description'] = description
        if location:
            npc_data['location'] = location
        if role:
            npc_data['role'] = role
        if notes:
            npc_data['notes'] = notes
        
        npc_ref = db.collection('campaigns').document(campaign_id).collection('npcs').document(doc_id)
        npc_ref.set(npc_data)
        print(f"[DatabaseManager] NPC '{name}' saved to campaign '{campaign_id}' successfully.")
        return f"NPC '{name}' has been saved to campaign '{campaign_id}'."
    except Exception as e:
        return f"Error saving NPC '{name}' to campaign '{campaign_id}': {e}"

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
