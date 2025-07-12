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

# --- Character Data Tools ---

def save_character(character_data: dict) -> str:
    """
    Saves a complete character sheet to the 'characters' collection in Firestore.
    The document ID will be the character's name in lowercase.
    """
    if not db:
        return "Error: Database client is not available."
    if 'name' not in character_data:
        return "Error: Character data must include a 'name' field."

    char_name = character_data['name']
    doc_id = char_name.lower()
    doc_ref = db.collection('characters').document(doc_id)
    
    try:
        doc_ref.set(character_data)
        print(f"[DatabaseManager] Character '{char_name}' saved successfully.")
        return f"Character '{char_name}' has been saved to the database."
    except Exception as e:
        return f"Error saving character '{char_name}': {e}"

def load_character(character_name: str) -> dict:
    """
    Loads a character sheet from the 'characters' collection by name.
    """
    if not db:
        return {"error": "Database client is not available."}

    doc_id = character_name.lower()
    doc_ref = db.collection('characters').document(doc_id)
    
    try:
        doc = doc_ref.get()
        if doc.exists:
            print(f"[DatabaseManager] Character '{character_name}' loaded successfully.")
            return doc.to_dict()
        else:
            return {"error": f"Character '{character_name}' not found."}
    except Exception as e:
        return {"error": f"Error loading character '{character_name}': {e}"}

# --- NPC Data Tools ---

def save_npc(npc_data: dict) -> str:
    """
    Saves an NPC's data to the 'npcs' collection in Firestore.
    A unique ID should be provided or created for the NPC.
    """
    if not db:
        return "Error: Database client is not available."
    if 'id' not in npc_data:
        return "Error: NPC data must include a unique 'id' field."

    doc_id = npc_data['id']
    doc_ref = db.collection('npcs').document(doc_id)
    
    try:
        doc_ref.set(npc_data)
        print(f"[DatabaseManager] NPC '{npc_data.get('name', doc_id)}' saved successfully.")
        return f"NPC '{npc_data.get('name', doc_id)}' has been saved."
    except Exception as e:
        return f"Error saving NPC '{doc_id}': {e}"


def load_npc(npc_id: str) -> dict:
    """
    Loads an NPC's data from the 'npcs' collection by its unique ID.
    """
    if not db:
        return {"error": "Database client is not available."}

    doc_ref = db.collection('npcs').document(npc_id)
    
    try:
        doc = doc_ref.get()
        if doc.exists:
            print(f"[DatabaseManager] NPC '{npc_id}' loaded successfully.")
            return doc.to_dict()
        else:
            return {"error": f"NPC with ID '{npc_id}' not found."}
    except Exception as e:
        return {"error": f"Error loading NPC '{npc_id}': {e}"}

# ==============================================================================
#  EXAMPLE USAGE (for testing the script from the command line)
# ==============================================================================
if __name__ == '__main__':
    print("\n--- Testing Database Manager ---")
