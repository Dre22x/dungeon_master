import uuid
from flask import Flask, render_template, jsonify
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from firestore import db_utils
from agents.agent import root_agent
import datetime
import json
import threading
import queue
from flask_sock import Sock

def make_json_serializable(obj):
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(v) for v in obj]
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()
    else:
        return obj

# Initialize the Flask application
app = Flask(__name__, template_folder='.')

# Initialize WebSocket extension
sock = Sock(app)

# Global session service for persistent sessions
from google.adk.sessions import InMemorySessionService
session_service = InMemorySessionService()

# Global debug message queue for streaming debug output
debug_messages = queue.Queue()
debug_subscribers = set()

# ==============================================================================
#  AGENT & DATABASE LOGIC (Placeholders)
#  This is where you would import and call your existing Python agent code.
# ==============================================================================

def send_debug_message(message, message_type='info', campaign_id=None):
    """Send a debug message to all connected clients."""
    debug_data = {
        'message': message,
        'type': message_type,
        'campaign_id': campaign_id,
        'timestamp': datetime.datetime.now().isoformat()
    }
    debug_messages.put(debug_data)
    
    # Send to all connected subscribers
    for ws in list(debug_subscribers):
        try:
            ws.send(json.dumps(debug_data))
        except Exception as e:
            print(f"Error sending debug message: {e}")
            debug_subscribers.discard(ws)

@sock.route('/debug-stream/<campaign_id>')
def debug_stream(ws, campaign_id):
    """WebSocket endpoint for streaming debug output."""
    debug_subscribers.add(ws)
    send_debug_message(f"Debug stream connected for campaign {campaign_id}", 'info', campaign_id)
    
    try:
        while True:
            # Keep connection alive
            ws.receive()
    except Exception as e:
        print(f"Debug WebSocket error: {e}")
    finally:
        debug_subscribers.discard(ws)
        send_debug_message(f"Debug stream disconnected for campaign {campaign_id}", 'warning', campaign_id)

def initialize_new_campaign_in_db():
    print("BACKEND: GM Agent is creating a new campaign...")
    new_id = str(uuid.uuid4())[:8] # Generate a simple unique ID
    send_debug_message(f"Creating new campaign with ID: {new_id}", 'info')
    db_utils.create_campaign(new_id)
    send_debug_message(f"Campaign {new_id} created successfully in database", 'info')
    return new_id

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
    
    send_debug_message(f"Initializing root agent for new campaign {campaign_id}", 'agent_transfer')
    
    # Set up the session and runner using global session service
    session = await session_service.create_session(
        app_name="dungeon_master",
        user_id="user_1",
        session_id=f"session_{campaign_id}",
    )

    runner = Runner(
        agent=root_agent,
        app_name="dungeon_master",
        session_service=session_service
    )

    # Create a message that instructs the agent to start a new campaign
    new_campaign_instruction = f"""
I want to start a new campaign with ID: {campaign_id}

Please begin the character creation process and then start a new adventure.
The campaign has been created in the database and is ready for you to manage.
"""

    content = types.Content(
        role='user', 
        parts=[types.Part(text=new_campaign_instruction)]
    )

    send_debug_message(f"Sending new campaign instruction to root agent", 'console')

    # Run the agent workflow to start the new campaign
    async for event in runner.run_async(
        user_id="user_1", 
        session_id=f"session_{campaign_id}", 
        new_message=content
    ):
        # Debug logging for agent events during initialization
        if hasattr(event, 'agent') and event.agent:
            send_debug_message(f"Agent called during initialization: {event.agent.name}", 'agent_transfer', campaign_id)
        
        if hasattr(event, 'actions') and event.actions:
            if hasattr(event.actions, 'escalate') and event.actions.escalate:
                send_debug_message(f"Agent escalated during initialization: {event.actions.escalate.agent_name}", 'agent_transfer', campaign_id)
        
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
                print(f"[Root Agent] New campaign {campaign_id} started: {final_response}")
                send_debug_message(f"Root agent completed new campaign initialization", 'agent_transfer', campaign_id)
                return final_response
            break

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
            "agent_response": agent_response,
            "adk_url": f"http://localhost:8000/dev-ui/?app=agents&session=session_{campaign_id}"
        })
    except Exception as e:
        print(f"Error initializing agent for new campaign: {e}")
        return jsonify({
            "status": "success", 
            "campaign_id": campaign_id,
            "agent_response": "Campaign created but agent initialization failed",
            "adk_url": f"http://localhost:8000/dev-ui/?app=agents&session=session_{campaign_id}"
        })

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
    session = await session_service.create_session(
        app_name="dungeon_master",
        user_id="user_1",
        session_id=f"session_{campaign_id}",
    )

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
    
    campaign_summary = f"""
CAMPAIGN CONTEXT - Campaign ID: {campaign_id}

CAMPAIGN DATA:
{formatted_campaign_data}

This is an existing campaign that has been loaded from the database. 
The campaign data above contains all the current state including:
- Characters and their stats
- NPCs and their relationships
- Monsters and encounters
- Locations and quests
- Campaign notes and story context
- Previous story events and decisions

{characters_summary}
{npcs_summary}
{quests_summary}

Your task is to continue this campaign from where it left off. 
Study the campaign data carefully and be ready to continue the story seamlessly.
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
        # Debug logging for agent events during campaign loading
        if hasattr(event, 'agent') and event.agent:
            send_debug_message(f"Agent called during campaign loading: {event.agent.name}", 'agent_transfer', campaign_id)
        
        if hasattr(event, 'actions') and event.actions:
            if hasattr(event.actions, 'escalate') and event.actions.escalate:
                send_debug_message(f"Agent escalated during campaign loading: {event.actions.escalate.agent_name}", 'agent_transfer', campaign_id)
        
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
                print(f"[Root Agent] Campaign {campaign_id} loaded: {final_response}")
                send_debug_message(f"Root agent completed campaign loading", 'agent_transfer', campaign_id)
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
            "agent_response": agent_response,
            "adk_url": f"http://localhost:8000/dev-ui/?app=agents&session=session_{campaign_id}"
        })
    except Exception as e:
        print(f"Error initializing agent with campaign data: {e}")
        return jsonify({
            "status": "success",
            "campaign_id": campaign_id,
            "campaign_data": campaign_data,
            "agent_response": "Campaign loaded but agent initialization failed",
            "adk_url": f"http://localhost:8000/dev-ui/?app=agents&session=session_{campaign_id}"
        })

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
        
        if not campaign_data or 'error' in campaign_data:
            # Campaign doesn't exist, create a new one
            initialize_new_campaign_in_db()
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
    
    send_debug_message(f"Received chat message: '{message[:50]}{'...' if len(message) > 50 else ''}'", 'api', campaign_id)
    
    try:
        # Set up the runner using global session service
        runner = Runner(
            agent=root_agent,
            app_name="dungeon_master",
            session_service=session_service
        )

        # Create the message content
        content = types.Content(
            role='user', 
            parts=[types.Part(text=message)]
        )

        send_debug_message(f"Routing message to root agent", 'agent_transfer', campaign_id)

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
                # Debug logging for agent events
                if hasattr(event, 'agent') and event.agent:
                    send_debug_message(f"Agent called: {event.agent.name}", 'agent_transfer', campaign_id)
                
                if hasattr(event, 'actions') and event.actions:
                    if hasattr(event.actions, 'escalate') and event.actions.escalate:
                        send_debug_message(f"Agent escalated to: {event.actions.escalate.agent_name}", 'agent_transfer', campaign_id)
                
                if event.is_final_response():
                    if event.content and event.content.parts:
                        return event.content.parts[0].text
            return ""
        
        agent_response = loop.run_until_complete(run_agent())
        loop.close()
        
        send_debug_message(f"Root agent response received", 'agent_transfer', campaign_id)
        
        return jsonify({
            "status": "success",
            "agent_response": agent_response
        })
        
    except Exception as e:
        print(f"Error in chat: {e}")
        send_debug_message(f"Error in chat: {str(e)}", 'error', campaign_id)
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

