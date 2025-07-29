import uuid
from flask import Flask, render_template, jsonify
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from firestore import db_utils
from root_agent.agent import root_agent
import datetime
import json
import threading

def make_json_serializable(obj):
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(v) for v in obj]
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()
    else:
        return str(obj)  # Convert any other objects to string

# Initialize the Flask application
app = Flask(__name__, template_folder='.')

# Global session service for persistent sessions
from google.adk.sessions import InMemorySessionService
session_service = InMemorySessionService()

# Global session tracking for InMemorySessionService
active_sessions = set()

def add_session_to_tracking(session_id):
    """Add a session to the active sessions tracking."""
    active_sessions.add(session_id)
    print(f"📝 Session added to tracking: {session_id}")

def remove_session_from_tracking(session_id):
    """Remove a session from the active sessions tracking."""
    active_sessions.discard(session_id)
    print(f"📝 Session removed from tracking: {session_id}")

def initialize_new_campaign_in_db(campaign_id=None):
    print("BACKEND: GM Agent is creating a new campaign...")
    if campaign_id is None:
        campaign_id = str(uuid.uuid4())[:8] # Generate a simple unique ID
    db_utils.create_campaign(campaign_id)
    return campaign_id

def load_campaign_from_db(campaign_id):
    print(f"BACKEND: Looking up campaign '{campaign_id}' in Firestore...")
    return db_utils.load_campaign(campaign_id)


# ==============================================================================
#  FLASK ROUTES (API Endpoints)
#  These are the URLs that the frontend JavaScript will call.
# ==============================================================================

@app.route('/')
def index():
    """
    This route serves the main HTML page.
    """
    return render_template('index.html')

@app.route('/campaign')
def campaign():
    """
    This route serves the campaign interface page.
    """
    return render_template('campaign.html')

async def initialize_agent_for_new_campaign(campaign_id: str):
    """
    Initializes the GM agent for a new campaign.
    """
    from google.adk.runners import Runner
    from google.genai import types
    
    # Set up the session and runner using global session service
    session_id = f"session_{campaign_id}"
    session = await session_service.create_session(
        app_name="dungeon_master",
        user_id="user_1",
        session_id=session_id,
    )
    
    # Track the session
    add_session_to_tracking(session_id)

    runner = Runner(
        agent=root_agent,
        app_name="dungeon_master",
        session_service=session_service
    )

    # Create a message that instructs the agent to start a new campaign
    new_campaign_instruction = f"""
start new campaign

A new campaign has been created with campaign_id: {campaign_id}

Please begin the NEW CAMPAIGN STARTUP workflow immediately.
"""

    content = types.Content(
        role='user', 
        parts=[types.Part(text=new_campaign_instruction)]
    )

    # Run the agent workflow to start the new campaign
    async for event in runner.run_async(
        user_id="user_1", 
        session_id=session_id, 
        new_message=content
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
                print(f"[Root Agent] New campaign {campaign_id} started: {final_response}")
                return final_response
        break

@app.route('/start-new-campaign', methods=['POST'])
def start_new_campaign():
    """
    API endpoint to start a new campaign by invoking the root agent directly.
    This bypasses the Flask app creation and goes straight to the ADK console.
    """
    import asyncio
    from flask import request
    
    data = request.get_json()
    campaign_id = data.get('campaign_id')
    
    if not campaign_id:
        return jsonify({"status": "error", "message": "Campaign ID is required"}), 400
    
    try:
        # Create the campaign in the database first
        initialize_new_campaign_in_db(campaign_id)
        
        # Initialize the root agent with the new campaign
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        agent_response = loop.run_until_complete(initialize_agent_for_new_campaign(campaign_id))
        loop.close()
        
        return jsonify({
            "status": "success", 
            "campaign_id": campaign_id,
            "agent_response": agent_response
        })
    except Exception as e:
        print(f"Error starting new campaign: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/new-campaign', methods=['POST'])
def new_campaign():
    """
    API endpoint to handle the creation of a new campaign.
    Creates the campaign in the database and initializes the agent.
    """
    import asyncio
    
    campaign_id = initialize_new_campaign_in_db()
    
    # Initialize the agent for the new campaign
    try:
        # Run the async function to initialize the agent
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        agent_response = loop.run_until_complete(initialize_agent_for_new_campaign(campaign_id))
        loop.close()
        
        return jsonify({
            "status": "success", 
            "campaign_id": campaign_id,
            "agent_response": agent_response
        })
    except Exception as e:
        print(f"Error initializing agent for new campaign: {e}")
        return jsonify({
            "status": "success", 
            "campaign_id": campaign_id,
            "agent_response": "Campaign created but agent initialization failed"
        }), 500

@app.route('/campaign/<string:campaign_id>/characters', methods=['GET'])
def get_campaign_characters(campaign_id):
    """
    API endpoint to get all characters for a specific campaign.
    """
    try:
        characters = db_utils.list_characters_in_campaign(campaign_id)
        if 'error' in characters:
            return jsonify({"status": "error", "message": characters['error']}), 404
        
        return jsonify({
            "status": "success",
            "characters": characters.get('characters', [])
        })
    except Exception as e:
        print(f"Error getting characters for campaign {campaign_id}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/equipment/<string:equipment_name>', methods=['GET'])
def get_equipment_details(equipment_name):
    """
    API endpoint to get detailed information about a piece of equipment.
    """
    try:
        from tools.equipment import get_equipment_details
        details = get_equipment_details(equipment_name)
        return jsonify({
            "status": "success",
            "details": details
        })
    except Exception as e:
        print(f"Error getting equipment details for {equipment_name}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/spells/<string:spell_name>', methods=['GET'])
def get_spell_details(spell_name):
    """
    API endpoint to get detailed information about a spell.
    """
    try:
        from tools.spells import get_spell_details
        details = get_spell_details(spell_name)
        return jsonify({
            "status": "success",
            "details": details
        })
    except Exception as e:
        print(f"Error getting spell details for {spell_name}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/skills/<string:skill_name>', methods=['GET'])
def get_skill_details(skill_name):
    """
    API endpoint to get detailed information about a skill.
    """
    try:
        from tools.character_data import get_skill_details
        details = get_skill_details(skill_name)
        return jsonify({
            "status": "success",
            "details": details
        })
    except Exception as e:
        print(f"Error getting skill details for {skill_name}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/proficiencies/<string:proficiency_name>', methods=['GET'])
def get_proficiency_details(proficiency_name):
    """
    API endpoint to get detailed information about a proficiency.
    """
    try:
        from tools.character_data import get_proficiency_details
        details = get_proficiency_details(proficiency_name)
        return jsonify({
            "status": "success",
            "details": details
        })
    except Exception as e:
        print(f"Error getting proficiency details for {proficiency_name}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/skills_index', methods=['GET'])
def get_skills_index():
    """
    Returns a mapping of skill display names to their API indexes.
    """
    try:
        from tools.character_data import get_all_skills
        skills_data = get_all_skills()
        # skills_data is a dict with 'results' key containing the list
        skills = skills_data.get('results', [])
        mapping = {s['name']: s['index'] for s in skills}
        return jsonify({"status": "success", "mapping": mapping})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/proficiencies_index', methods=['GET'])
def get_proficiencies_index():
    """
    Returns a mapping of proficiency display names to their API indexes.
    """
    try:
        from tools.character_data import get_all_proficiencies
        profs_data = get_all_proficiencies()
        # profs_data is a dict with 'results' key containing the list
        profs = profs_data.get('results', [])
        mapping = {p['name']: p['index'] for p in profs}
        return jsonify({"status": "success", "mapping": mapping})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

async def initialize_agent_with_campaign(campaign_id: str, campaign_data: dict):
    """
    Initializes the GM agent with the loaded campaign data.
    """
    from google.adk.runners import Runner
    from google.genai import types
    
    # Set up the session and runner using global session service
    session_id = f"session_{campaign_id}"
    session = await session_service.create_session(
        app_name="dungeon_master",
        user_id="user_1",
        session_id=session_id,
    )
    
    # Track the session
    add_session_to_tracking(session_id)

    runner = Runner(
        agent=root_agent,
        app_name="dungeon_master",
        session_service=session_service
    )

    # Format the campaign data for the agent
    formatted_campaign_data = json.dumps(campaign_data, indent=2)
    
    # Create a more detailed campaign summary
    characters_summary = ""
    if 'characters' in campaign_data and campaign_data['characters']:
        characters_summary = "\nCHARACTERS:\n"
        for char in campaign_data['characters']:
            characters_summary += f"- {char.get('name', 'Unknown')} ({char.get('race', 'Unknown')} {char.get('class', 'Unknown')} Level {char.get('level', 1)})\n"
    
    npcs_summary = ""
    if 'npcs' in campaign_data and campaign_data['npcs']:
        npcs_summary = "\nIMPORTANT NPCS:\n"
        for npc in campaign_data['npcs']:
            npcs_summary += f"- {npc.get('name', 'Unknown')} ({npc.get('role', 'Unknown')}): {npc.get('description', 'No description')}\n"
    
    quests_summary = ""
    if 'quests' in campaign_data and campaign_data['quests']:
        quests_summary = "\nACTIVE QUESTS:\n"
        for quest in campaign_data['quests']:
            quests_summary += f"- {quest.get('name', 'Unknown Quest')}: {quest.get('description', 'No description')}\n"
    
    # Extract and prominently display the campaign context
    campaign_context = ""
    if 'context' in campaign_data and campaign_data['context']:
        campaign_context = f"""
CURRENT CAMPAIGN CONTEXT (Most Recent Story State):
{campaign_data['context']}

"""
    else:
        campaign_context = """
CURRENT CAMPAIGN CONTEXT:
No context has been saved yet. This appears to be a new campaign or the context was not properly saved.
"""
    
    campaign_summary = f"""
CAMPAIGN LOADED - Campaign ID: {campaign_id}

{campaign_context}
{characters_summary}
{npcs_summary}
{quests_summary}

FULL CAMPAIGN DATA (for reference):
{formatted_campaign_data}

This is an existing campaign that has been loaded from the database. 
The campaign context above contains the most recent story state and events.

Your task is to continue this campaign from where it left off. 
Study the campaign context carefully and be ready to continue the story seamlessly.
Do NOT start a new campaign or character creation process.

IMPORTANT: Provide a brief summary of the campaign so far as your first response to help the player understand where they left off.
"""

    content = types.Content(
        role='user', 
        parts=[types.Part(text=campaign_summary)]
    )

    # Run the agent workflow to load campaign context
    async for event in runner.run_async(
        user_id="user_1", 
        session_id=f"session_{campaign_id}", 
        new_message=content
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
                print(f"[Root Agent] Campaign {campaign_id} loaded: {final_response}")
                return final_response
            break

@app.route('/load-campaign/<string:campaign_id>', methods=['GET'])
def load_campaign(campaign_id):
    """
    API endpoint to handle loading an existing campaign.
    Loads campaign data and initializes the GM agent with full context.
    """
    import asyncio
    
    campaign_data = load_campaign_from_db(campaign_id)
    campaign_data = make_json_serializable(campaign_data)
    if not campaign_data or 'error' in campaign_data:
        # Return a 404 Not Found error if the campaign doesn't exist
        return jsonify({"status": "error", "message": "Campaign not found"}), 404
    
    # Initialize the agent with campaign data
    try:
        # Run the async function to initialize the agent
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        agent_response = loop.run_until_complete(initialize_agent_with_campaign(campaign_id, campaign_data))
        loop.close()
        
        return jsonify({
            "status": "success",
            "campaign_id": campaign_id,
            "campaign_data": campaign_data,
            "agent_response": agent_response
        })
    except Exception as e:
        print(f"Error initializing agent with campaign data: {e}")
        return jsonify({
            "status": "success",
            "campaign_id": campaign_id,
            "campaign_data": campaign_data,
            "agent_response": "Campaign loaded but agent initialization failed"
        }), 500

@app.route('/initialize-campaign', methods=['POST'])
def initialize_campaign():
    """
    API endpoint to initialize a campaign for the chat interface.
    """
    import asyncio
    from flask import request
    
    data = request.get_json()
    campaign_id = data.get('campaign_id')
    
    if not campaign_id:
        return jsonify({"status": "error", "message": "Campaign ID is required"}), 400
    
    try:
        # Check if campaign exists
        campaign_data = load_campaign_from_db(campaign_id)
        campaign_data = make_json_serializable(campaign_data)
        
        # Initialize the agent with campaign data
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Check if this is an existing campaign with content
        is_existing_campaign = (
            campaign_data and 
            not 'error' in campaign_data and
            (
                ('characters' in campaign_data and len(campaign_data['characters']) > 0) or
                ('context' in campaign_data and campaign_data['context']) or
                ('notes' in campaign_data and len(campaign_data['notes']) > 0)
            )
        )
        
        if is_existing_campaign:
            # Existing campaign - load it with context
            print(f"[App] Loading existing campaign {campaign_id} with data")
            agent_response = loop.run_until_complete(initialize_agent_with_campaign(campaign_id, campaign_data))
        else:
            # New campaign - start character creation
            print(f"[App] Starting new campaign {campaign_id}")
            agent_response = loop.run_until_complete(initialize_agent_for_new_campaign(campaign_id))
        
        loop.close()
        
        return jsonify({
            "status": "success",
            "campaign_id": campaign_id,
            "agent_response": agent_response
        })
        
    except Exception as e:
        print(f"Error initializing campaign: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/chat', methods=['POST'])
def chat():
    """
    API endpoint to handle chat messages with the agent.
    Player input is automatically routed to the Player Interface Agent.
    """
    import asyncio
    from flask import request
    from google.adk.sessions import InMemorySessionService
    from google.adk.runners import Runner
    from google.genai import types
    
    data = request.get_json()
    campaign_id = data.get('campaign_id')
    message = data.get('message')
    
    if not campaign_id or not message:
        return jsonify({"status": "error", "message": "Campaign ID and message are required"}), 400
    
    try:
        # Set up the runner using global session service
        runner = Runner(
            agent=root_agent,
            app_name="dungeon_master",
            session_service=session_service
        )

        # Create the message content - this goes to root_agent which will route to Player Interface Agent
        content = types.Content(
            role='user', 
            parts=[types.Part(text=message)]
        )

        # Run the agent workflow
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        agent_response = ""
        
        async def run_agent():
            async for event in runner.run_async(
                user_id="user_1", 
                session_id=f"session_{campaign_id}", 
                new_message=content
            ):
                if event.is_final_response():
                    if event.content and event.content.parts:
                        return event.content.parts[0].text
            return ""
        
        agent_response = loop.run_until_complete(run_agent())
        loop.close()
        
        return jsonify({
            "status": "success",
            "agent_response": agent_response
        })
        
    except Exception as e:
        print(f"Error in chat: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/sessions', methods=['GET'])
def list_sessions():
    """
    API endpoint to list all active sessions.
    """
    try:
        session_list = []
        for session_id in active_sessions:
            # Extract campaign ID from session ID
            campaign_id = session_id.replace('session_', '') if session_id.startswith('session_') else session_id
            
            session_info = {
                'session_id': session_id,
                'user_id': 'user_1',
                'created_at': None,  # InMemorySessionService doesn't provide creation time
            }
            session_list.append(session_info)
        
        return jsonify({
            "status": "success",
            "sessions": session_list,
            "total_sessions": len(session_list)
        })
        
    except Exception as e:
        print(f"Error listing sessions: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/sessions/<string:session_id>', methods=['DELETE'])
def delete_session(session_id):
    """
    API endpoint to delete a specific session.
    """
    import asyncio
    
    try:
        # Run the async delete operation
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(session_service.delete_session(
            app_name="dungeon_master",
            user_id="user_1",
            session_id=session_id
        ))
        loop.close()
        
        # Remove from active sessions tracking
        remove_session_from_tracking(session_id)
        
        return jsonify({
            "status": "success",
            "message": f"Session {session_id} deleted successfully"
        })
        
    except Exception as e:
        print(f"Error deleting session {session_id}: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ==============================================================================
#  SESSION SWITCHING API
# ==============================================================================

@app.route('/switch-session/<string:campaign_id>', methods=['POST'])
def switch_session(campaign_id):
    """
    API endpoint to manually switch to a specific session for a campaign.
    """
    from flask import request
    
    data = request.get_json() or {}
    session_id = data.get('session_id')
    agent_name = data.get('agent_name', 'Unknown')
    
    if not session_id:
        return jsonify({
            "status": "error",
            "message": "Session ID is required"
        }), 400
    
    try:
        return jsonify({
            "status": "success",
            "session_id": session_id,
            "agent_name": agent_name
        })
        
    except Exception as e:
        print(f"Error switching session: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/get-current-session/<string:campaign_id>', methods=['GET'])
def get_current_session(campaign_id):
    """
    API endpoint to get the current active session for a campaign.
    """
    try:
        # For now, return the root agent session
        # In the future, this could track the currently active session
        session_id = f"session_{campaign_id}"
        
        return jsonify({
            "status": "success",
            "campaign_id": campaign_id,
            "session_id": session_id,
            "agent_name": "Root Agent"
        })
        
    except Exception as e:
        print(f"Error getting current session: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/get-available-sessions/<string:campaign_id>', methods=['GET'])
def get_available_sessions(campaign_id):
    """
    API endpoint to get all available sessions for a campaign.
    """
    try:
        # Get all sessions for this campaign
        campaign_sessions = []
        
        # Add the root agent session
        root_session_id = f"session_{campaign_id}"
        if root_session_id in active_sessions:
            campaign_sessions.append({
                'session_id': root_session_id,
                'agent_name': 'Root Agent',
                'agent_type': 'root',
                'description': 'Main campaign coordinator and orchestrator'
            })
        
        # Add any sub-agent sessions that match this campaign
        for session_id in active_sessions:
            if session_id.startswith(f"sub_agent_") and f"_{campaign_id}_" in session_id:
                # Extract agent name from session ID
                # Format: sub_agent_{agent_name}_{campaign_id}_{timestamp}
                parts = session_id.split('_')
                if len(parts) >= 4:
                    agent_name = parts[2].replace('_', ' ').title()
                    agent_type = parts[2]
                    
                    # Map agent types to descriptions
                    agent_descriptions = {
                        'character_creation': 'Handles character creation and customization',
                        'narrative': 'Manages story elements and environmental descriptions',
                        'rules_lawyer': 'Handles combat mechanics and rules questions',
                        'npc': 'Manages NPC dialogue and roleplay',
                        'campaign_creation': 'Creates campaign outlines and story structure',
                        'player_interface': 'Handles direct player communication'
                    }
                    
                    description = agent_descriptions.get(agent_type, f'Specialized agent for {agent_name.lower()} tasks')
                    
                    campaign_sessions.append({
                        'session_id': session_id,
                        'agent_name': agent_name,
                        'agent_type': agent_type,
                        'description': description
                    })
        
        return jsonify({
            "status": "success",
            "campaign_id": campaign_id,
            "sessions": campaign_sessions,
            "total_sessions": len(campaign_sessions)
        })
        
    except Exception as e:
        print(f"Error getting available sessions: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ==============================================================================
#  MAIN EXECUTION BLOCK
# ==============================================================================

if __name__ == '__main__':
    # This makes the app accessible on your local network, which is great for
    # testing on your iPhone. Just navigate to your computer's IP address.
    app.run(host='0.0.0.0', port=5001, debug=True)

