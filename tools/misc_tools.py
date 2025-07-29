import random
from google.adk.tools.tool_context import ToolContext
import os
from google.cloud import firestore
from google.oauth2 import service_account

# Set up Google Cloud credentials using service account key
SERVICE_ACCOUNT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "service-account-key.json")

# Set the environment variable for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_PATH

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

db_ = get_db_client()

def roll_dice(dice_notation: str) -> str:
    """
    Roll dice in D&D notation (e.g., '1d20', '2d6+3', '1d4-1').
    
    Args:
        dice_notation: str - Dice notation like '1d20', '2d6+3', '1d4-1'
    
    Returns:
        str - Result of the dice roll with details
    """
    try:
        # Parse the dice notation
        parts = dice_notation.replace(' ', '').split('+')
        main_part = parts[0]
        modifier = 0
        
        if len(parts) > 1:
            modifier = int(parts[1])
        elif '-' in main_part:
            main_part, neg_mod = main_part.split('-')
            modifier = -int(neg_mod)
        
        # Parse the main dice part (e.g., "2d6")
        if 'd' not in main_part:
            return f"Error: Invalid dice notation '{dice_notation}'. Use format like '1d20' or '2d6+3'."
        
        num_dice, die_size = main_part.split('d')
        num_dice = int(num_dice)
        die_size = int(die_size)
        
        if num_dice <= 0 or die_size <= 0:
            return f"Error: Invalid dice values in '{dice_notation}'. Number of dice and die size must be positive."
        
        # Roll the dice
        rolls = [random.randint(1, die_size) for _ in range(num_dice)]
        total = sum(rolls) + modifier
        
        # Format the result
        if num_dice == 1:
            roll_detail = f"Rolled {rolls[0]}"
        else:
            roll_detail = f"Rolled {rolls} (sum: {sum(rolls)})"
        
        if modifier != 0:
            modifier_str = f" + {modifier}" if modifier > 0 else f" - {abs(modifier)}"
            return f"{roll_detail}{modifier_str} = {total}"
        else:
            return f"{roll_detail} = {total}"
            
    except (ValueError, IndexError) as e:
        return f"Error parsing dice notation '{dice_notation}': {e}"
    
def set_game_state(new_state: str, tool_context: ToolContext) -> bool:
    """
    Set the game state.
    """
    try:
      tool_context.state['game_state'] = new_state
      print(f"Game state set to {new_state}")
      return True
    except Exception as e:
      print(f"Error setting game state: {e}")
      return False
    

def create_campaign(campaign_id: str, tool_context: ToolContext) -> dict:
  """
  Creates a new entry for a campaign in the 'campaigns' collection in the database.

  Args:
      campaign_id: str - Unique identifier for the campaign
  """
  if not db_:
      return {'action': 'create_campaign', 'created': False, 'message': "Error: Database client is not available."}
      
  # Create the campaign document
  campaign_ref = db_.collection('campaigns').document(campaign_id)
  campaign_ref.set({
      'id': campaign_id,
      'created_date': firestore.SERVER_TIMESTAMP
  })
      
  # Create sub-collections
  sub_collections = ['context', 'last_saved', 'characters', 'npcs', 'monsters', 'campaign_outline']
      
  for sub_collection in sub_collections:
      init_doc = campaign_ref.collection(sub_collection).document('_init')
      init_doc.set({
          'created': True,
          'campaign_id': campaign_id,
          'campaign_outline': tool_context.state['campaign_outline']
      })
      
  print(f"[DatabaseManager] Campaign '{campaign_id}' created successfully with {len(sub_collections)} sub-collections.")
  return {'action': 'create_campaign', 'created': True, 'message': f"Campaign '{campaign_id}' has been created successfully."}
    

def save_campaign(campaign_id: str, context: str, tool_context: ToolContext) -> dict:
    """
    Saves/updates a campaign to the 'campaigns' collection in Firestore.
    Args:
        campaign_id: str - The ID of the campaign to save.
        context: str - The context of the campaign. This is a freeform summary of the main events of the campaign so far.
    """
    if not db_:
        return {'action': 'save_campaign', 'updated': False, 'message': "Error: Database client is not available."}

    try:
        campaign_ref = db_.collection('campaigns').document(campaign_id)
        
        # Check if campaign exists
        campaign_doc = campaign_ref.get()
        if not campaign_doc.exists:
            return f"Error: Campaign '{campaign_id}' not found."
        
        # Update the campaign with context and timestamp
        update_data = {
            'context': context,
            'last_saved': firestore.SERVER_TIMESTAMP,
            'state': tool_context.state
        }
        
        campaign_ref.update(update_data)
        print(f"[DatabaseManager] Campaign '{campaign_id}' context updated successfully")
        return {'action': 'save_campaign', 'updated': True, 'message': f"Campaign '{campaign_id}' has been updated successfully with {len(context)} characters of context."}

    except Exception as e:
        return {'action': 'save_campaign', 'updated': False, 'message': f"Error saving campaign '{campaign_id}': {e}"}

def load_campaign(campaign_id: str) -> dict:
    """
    Loads a campaign by its ID. This includes the context, characters, npcs, monsters, locations, quests, and notes.
    Args:
        campaign_id: str - The ID of the campaign to load.
    """
    if not db_:
        return {"error": "Database client is not available."}

    try:
        campaign_ref = db_.collection('campaigns').document(campaign_id)
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
            return {'action': 'load_campaign', 'loaded': True, 'message': f"Campaign '{campaign_data.get('name', campaign_id)}' loaded successfully with all sub-collections."}
        else:
            return {"error": f"Campaign with ID '{campaign_id}' not found."}
    except Exception as e:
        return {"error": f"Error loading campaign '{campaign_id}': {e}"}
    