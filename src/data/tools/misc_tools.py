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
    
def set_state(state_name: str, state_value: str, tool_context: ToolContext) -> dict:
    """
    Set given state variable to given value.

    Args:
        state_name: str - The name of the state variable to set
        state_value: str - The value to set the state variable to

    Returns:
        dict - Action, state_name, state_value, and success
    """
    try:
      print(f"Current state: {tool_context.state.get(state_name, 'None')}")
      tool_context.state[state_name] = state_value
      print(f"{state_name} set to {state_value}")
      return {'action': 'set_state', 'state_name': state_name, 'state_value': state_value, 'success': True}
    except Exception as e:
      print(f"Error setting game state: {e}")
      return {'action': 'set_state', 'state_name': state_name, 'state_value': state_value, 'success': False}
    
def get_state(state_name: str, tool_context: ToolContext) -> dict:
    """
    Get given state variable.

    Args:
        state_name: str - The name of the state variable to get
    Returns:
        dict - Action, state_name, and state_value
    """
    try:
      state_value = tool_context.state.get(state_name, "")
      print(f"State {state_name} set to {state_value}")
      return {'action': 'get_state', 'state_name': state_name, 'state_value': state_value, 'success': True}
    except Exception as e:
      print(f"Error getting game state: {e}")
      return {'action': 'get_state', 'state_name': state_name, 'state_value': None, 'success': False}


def create_campaign(campaign_id: str, tool_context: ToolContext) -> dict:
  """
  Creates a new entry for a campaign in the 'campaigns' collection in the database.

  Args:
      campaign_id: str - Unique identifier for the campaign]
  Returns:
      dict - Action, created, and message
  """
  if not db_:
      return {'action': 'create_campaign', 'created': False, 'message': "Error: Database client is not available."}
      
  # Create the campaign collection and state document
  campaign_ref = db_.collection(campaign_id).document('state')
  
  # Initialize with basic state variables
  initial_state = {
      'created_date': firestore.SERVER_TIMESTAMP,
      'game_state': '',
      'last_scene': '',
      'campaign_outline': tool_context.state.get('campaign_outline', ''),
      'last_action': '',
      'characters': [],
      'npcs': [],
      'combat_participants': {},
      'combat_details': {},
      'dialogue_participants': [],
      'location': '',
      'current_act': ''
  }
  
  campaign_ref.set(initial_state)
      
  print(f"[DatabaseManager] Campaign '{campaign_id}' created successfully with state document.")
  return {'action': 'create_campaign', 'created': True, 'message': f"Campaign '{campaign_id}' has been created successfully."}
    

def save_campaign(campaign_id: str, context: str, tool_context: ToolContext) -> dict:
    """
    Saves/updates a campaign to the campaign collection with state document.
    Args:
        campaign_id: str - The ID of the campaign to save.
        context: str - The context of the campaign. This is a freeform summary of the main events of the campaign so far.

    Returns:
        dict - Action, updated, and message
    """
    if not db_:
        return {'action': 'save_campaign', 'updated': False, 'message': "Error: Database client is not available."}

    try:
        campaign_ref = db_.collection(campaign_id).document('state')
        
        # Check if campaign exists
        campaign_doc = campaign_ref.get()
        if not campaign_doc.exists:
            # Create the campaign if it doesn't exist
            initial_state = {
                'created_date': firestore.SERVER_TIMESTAMP,
                'game_state': '',
                'last_scene': '',
                'campaign_outline': tool_context.state.get('campaign_outline', ''),
                'last_action': '',
                'characters': [],
                'npcs': [],
                'combat_participants': {},
                'combat_details': {},
                'dialogue_participants': [],
                'location': '',
                'current_act': ''
            }
            campaign_ref.set(initial_state)
            print(f"[DatabaseManager] Campaign '{campaign_id}' created successfully.")
        
        # Get all state variables individually
        game_state = tool_context.state.get('game_state', '')
        last_scene = tool_context.state.get('last_scene', '')
        campaign_outline = tool_context.state.get('campaign_outline', '')
        last_action = tool_context.state.get('last_action', '')
        characters = tool_context.state.get('characters', [])
        npcs = tool_context.state.get('npcs', [])
        combat_participants = tool_context.state.get('combat_participants', {})
        combat_details = tool_context.state.get('combat_details', {})
        dialogue_participants = tool_context.state.get('dialogue_participants', [])
        location = tool_context.state.get('location', '')
        current_act = tool_context.state.get('current_act', '')
        
        # Prepare state variables document data
        state_variables_data = {
            'last_saved': firestore.SERVER_TIMESTAMP,
            'game_state': game_state,
            'last_scene': last_scene,
            'last_action': last_action,
            'context': context,
            'combat_participants': combat_participants,
            'combat_details': combat_details,
            'dialogue_participants': dialogue_participants,
            'characters': characters,
            'npcs': npcs,
            'location': location,
            'current_act': current_act
        }
        
        # Handle campaign outline
        if isinstance(campaign_outline, str) and campaign_outline:
            try:
                import json
                parsed_outline = json.loads(campaign_outline)
                state_variables_data['campaign_outline'] = parsed_outline
            except json.JSONDecodeError:
                state_variables_data['campaign_outline'] = campaign_outline
                print(f"[DatabaseManager] Warning: Campaign outline is not valid JSON for campaign '{campaign_id}'")
        elif isinstance(campaign_outline, dict):
            state_variables_data['campaign_outline'] = campaign_outline
        elif campaign_outline:
            state_variables_data['campaign_outline'] = campaign_outline
        
        # Update the state document
        campaign_ref.update(state_variables_data)
        
        print(f"[DatabaseManager] Campaign '{campaign_id}' updated successfully with state structure")
        return {
            'action': 'save_campaign', 
            'updated': True, 
            'message': f"Campaign '{campaign_id}' has been updated successfully with {len(context)} characters of context."
        }

    except Exception as e:
        return {'action': 'save_campaign', 'updated': False, 'message': f"Error saving campaign '{campaign_id}': {e}"}

def load_campaign(campaign_id: str, tool_context: ToolContext) -> dict:
    """
    Loads a campaign by its ID and restores all state variables to the shared state.
    Args:
        campaign_id: str - The ID of the campaign to load.

    Returns:
        dict - Action, loaded, and message
    """
    if not db_:
        return {"error": "Database client is not available."}

    try:
        campaign_ref = db_.collection(campaign_id).document('state')
        campaign_doc = campaign_ref.get()
        
        if campaign_doc.exists:
            campaign_data = campaign_doc.to_dict()
            
            # Load all state variables into the shared state
            tool_context.state['game_state'] = campaign_data.get('game_state', '')
            tool_context.state['last_scene'] = campaign_data.get('last_scene', '')
            tool_context.state['campaign_outline'] = campaign_data.get('campaign_outline', '')
            tool_context.state['last_action'] = campaign_data.get('last_action', '')
            tool_context.state['characters'] = campaign_data.get('characters', [])
            tool_context.state['npcs'] = campaign_data.get('npcs', [])
            tool_context.state['combat_participants'] = campaign_data.get('combat_participants', {})
            tool_context.state['combat_details'] = campaign_data.get('combat_details', {})
            tool_context.state['dialogue_participants'] = campaign_data.get('dialogue_participants', [])
            tool_context.state['location'] = campaign_data.get('location', '')
            tool_context.state['current_act'] = campaign_data.get('current_act', '')
            
            print(f"[DatabaseManager] Campaign '{campaign_id}' loaded successfully with all state variables.")
            return {'action': 'load_campaign', 'loaded': True, 'message': f"Campaign '{campaign_id}' loaded successfully with all state variables."}
        else:
            return {"error": f"Campaign with ID '{campaign_id}' not found."}
    except Exception as e:
        return {"error": f"Error loading campaign '{campaign_id}': {e}"}
    
def fix_campaign_data_structure(campaign_id: str) -> dict:
    """
    Fixes the data structure of an existing campaign to use the new state format.
    This function migrates data from the old structure to the new one.
    
    Args:
        campaign_id: str - The ID of the campaign to fix.
    
    Returns:
        dict - Action, fixed, and message
    """
    if not db_:
        return {'action': 'fix_campaign_data_structure', 'fixed': False, 'message': "Error: Database client is not available."}

    try:
        # Check if old structure exists (campaigns collection)
        old_campaign_ref = db_.collection('campaigns').document(campaign_id)
        old_campaign_doc = old_campaign_ref.get()
        
        if not old_campaign_doc.exists:
            return {'action': 'fix_campaign_data_structure', 'fixed': False, 'message': f"Campaign '{campaign_id}' not found in old structure."}
        
        old_campaign_data = old_campaign_doc.to_dict()
        
        # Create new structure
        new_campaign_ref = db_.collection(campaign_id).document('state')
        
        # Prepare state data
        state_variables_data = {
            'created_date': old_campaign_data.get('created_date', firestore.SERVER_TIMESTAMP),
            'last_saved': firestore.SERVER_TIMESTAMP,
            'game_state': old_campaign_data.get('game_state', ''),
            'last_scene': old_campaign_data.get('last_scene', ''),
            'last_action': old_campaign_data.get('last_action', ''),
            'context': old_campaign_data.get('context', ''),
            'combat_participants': old_campaign_data.get('combat_participants', {}),
            'combat_details': old_campaign_data.get('combat_details', {}),
            'dialogue_participants': old_campaign_data.get('dialogue_participants', []),
            'characters': old_campaign_data.get('characters', []),
            'npcs': old_campaign_data.get('npcs', []),
            'location': old_campaign_data.get('location', ''),
            'current_act': old_campaign_data.get('current_act', '')
        }
        
        # Handle campaign outline
        campaign_outline = old_campaign_data.get('campaign_outline', '')
        if isinstance(campaign_outline, str) and campaign_outline:
            try:
                import json
                parsed_outline = json.loads(campaign_outline)
                state_variables_data['campaign_outline'] = parsed_outline
            except json.JSONDecodeError:
                state_variables_data['campaign_outline'] = campaign_outline
        elif isinstance(campaign_outline, dict):
            state_variables_data['campaign_outline'] = campaign_outline
        elif campaign_outline:
            state_variables_data['campaign_outline'] = campaign_outline
        
        # Create the new state document
        new_campaign_ref.set(state_variables_data)
        
        print(f"[DatabaseManager] Campaign '{campaign_id}' data structure migrated successfully")
        return {
            'action': 'fix_campaign_data_structure', 
            'fixed': True, 
            'message': f"Campaign '{campaign_id}' data structure has been migrated to new state format."
        }

    except Exception as e:
        return {'action': 'fix_campaign_data_structure', 'fixed': False, 'message': f"Error fixing campaign '{campaign_id}': {e}"}
    