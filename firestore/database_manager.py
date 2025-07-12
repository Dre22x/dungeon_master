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
#  DATABASE TOOL FUNCTIONS
# ==============================================================================

# --- Campaign-Centric Database Functions ---

def create_campaign(campaign_data: dict) -> str:
    """
    Creates a new campaign with all necessary sub-collections.
    """
    if not db:
        return "Error: Database client is not available."
    if 'id' not in campaign_data or 'name' not in campaign_data:
        return "Error: Campaign data must include 'id' and 'name' fields."

    campaign_id = campaign_data['id']
    campaign_name = campaign_data['name']
    
    try:
        # Create the campaign document
        campaign_ref = db.collection('campaigns').document(campaign_id)
        campaign_ref.set(campaign_data)
        
        # Create sub-collections
        sub_collections = ['characters', 'npcs', 'monsters', 'items', 'spells', 'locations', 'quests', 'sessions', 'notes']
        
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
        sub_collections = ['characters', 'npcs', 'monsters', 'items', 'spells', 'locations', 'quests', 'sessions', 'notes']
        
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

# --- Database Management Tools ---

def clear_database():
    """
    Completely clears all data from the Firestore database.
    WARNING: This will delete ALL documents in ALL collections!
    """
    if not db:
        return "Error: Database client is not available."
    
    try:
        # Get all collections
        collections = db.collections()
        deleted_count = 0
        
        for collection in collections:
            collection_name = collection.id
            print(f"[DatabaseManager] Clearing collection: {collection_name}")
            
            # Get all documents in the collection
            docs = collection.stream()
            for doc in docs:
                doc.reference.delete()
                deleted_count += 1
                print(f"[DatabaseManager] Deleted document: {doc.id}")
        
        print(f"[DatabaseManager] Database cleared successfully. Deleted {deleted_count} documents.")
        return f"Database cleared successfully. Deleted {deleted_count} documents."
        
    except Exception as e:
        return f"Error clearing database: {e}"

def list_all_collections():
    """
    Lists all collections in the database.
    """
    if not db:
        return {"error": "Database client is not available."}
    
    try:
        collections = list(db.collections())
        collection_names = [col.id for col in collections]
        print(f"[DatabaseManager] Found {len(collection_names)} collections: {collection_names}")
        return {
            "collections": collection_names,
            "count": len(collection_names)
        }
    except Exception as e:
        return {"error": f"Error listing collections: {e}"}

def list_documents_in_collection(collection_name: str):
    """
    Lists all documents in a specific collection.
    """
    if not db:
        return {"error": "Database client is not available."}
    
    try:
        collection_ref = db.collection(collection_name)
        docs = collection_ref.stream()
        
        documents = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data['_id'] = doc.id
            documents.append(doc_data)
        
        print(f"[DatabaseManager] Found {len(documents)} documents in collection '{collection_name}'")
        return {
            "collection": collection_name,
            "documents": documents,
            "count": len(documents)
        }
    except Exception as e:
        return {"error": f"Error listing documents in collection '{collection_name}': {e}"}

def get_database_stats():
    """
    Gets statistics about the database including collection counts and document counts.
    """
    if not db:
        return {"error": "Database client is not available."}
    
    try:
        collections = list(db.collections())
        stats = {
            "total_collections": len(collections),
            "collections": {}
        }
        
        total_documents = 0
        
        for collection in collections:
            collection_name = collection.id
            docs = list(collection.stream())
            doc_count = len(docs)
            total_documents += doc_count
            
            stats["collections"][collection_name] = {
                "document_count": doc_count,
                "documents": [doc.id for doc in docs]
            }
        
        stats["total_documents"] = total_documents
        
        print(f"[DatabaseManager] Database stats: {stats['total_collections']} collections, {total_documents} total documents")
        return stats
        
    except Exception as e:
        return {"error": f"Error getting database stats: {e}"}

def search_documents(collection_name: str, field_name: str, field_value):
    """
    Searches for documents in a collection where a specific field matches a value.
    """
    if not db:
        return {"error": "Database client is not available."}
    
    try:
        collection_ref = db.collection(collection_name)
        query = collection_ref.where(field_name, "==", field_value)
        docs = query.stream()
        
        results = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data['_id'] = doc.id
            results.append(doc_data)
        
        print(f"[DatabaseManager] Found {len(results)} documents in '{collection_name}' where {field_name} == {field_value}")
        return {
            "collection": collection_name,
            "search_field": field_name,
            "search_value": field_value,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        return {"error": f"Error searching documents: {e}"}
    
if __name__ == "__main__":
    clear_database()