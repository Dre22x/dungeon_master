import uuid
from flask import Flask, render_template, jsonify
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from firestore import db_utils
from agents.agent import root_agent

# Initialize the Flask application
app = Flask(__name__, template_folder='.')

# ==============================================================================
#  AGENT & DATABASE LOGIC (Placeholders)
#  This is where you would import and call your existing Python agent code.
# ==============================================================================

def initialize_new_campaign_in_db():
    print("BACKEND: GM Agent is creating a new campaign...")
    new_id = str(uuid.uuid4())[:8] # Generate a simple unique ID
    db_utils.create_campaign(new_id)
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

async def initialize_agent_for_new_campaign(campaign_id: str):
    """
    Initializes the GM agent for a new campaign.
    """
    from google.adk.sessions import InMemorySessionService
    from google.adk.runners import Runner
    from google.genai import types
    
    # Set up the session and runner
    session_service = InMemorySessionService()
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

    # Run the agent workflow to start the new campaign
    async for event in runner.run_async(
        user_id="user_1", 
        session_id=f"session_{campaign_id}", 
        new_message=content
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
                print(f"[Root Agent] New campaign {campaign_id} started: {final_response}")
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

async def initialize_agent_with_campaign(campaign_id: str, campaign_data: dict):
    """
    Initializes the GM agent with the loaded campaign data.
    """
    from google.adk.sessions import InMemorySessionService
    from google.adk.runners import Runner
    from google.genai import types
    
    # Set up the session and runner
    session_service = InMemorySessionService()
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
    import json
    formatted_campaign_data = json.dumps(campaign_data, indent=2)
    
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

Your task is to continue this campaign from where it left off. 
Study the campaign data carefully and be ready to continue the story seamlessly.
Do NOT start a new campaign or character creation process.
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

# ==============================================================================
#  MAIN EXECUTION BLOCK
# ==============================================================================

if __name__ == '__main__':
    # This makes the app accessible on your local network, which is great for
    # testing on your iPhone. Just navigate to your computer's IP address.
    app.run(host='0.0.0.0', port=5001, debug=True)

