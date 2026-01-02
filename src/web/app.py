from flask import Flask, render_template, jsonify
import sys
import os
from ..agents.agent import root_agent
import datetime
import json
from ..main import main_async

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

@app.route('/start-new-campaign', methods=['POST'])
def start_new_campaign():
    """
    API endpoint to start a new campaign by invoking the root agent directly.
    This bypasses the Flask app creation and goes straight to the ADK console.
    """
    import asyncio    

    try:
        # Initialize the root agent with the new campaign
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        agent_response = loop.run_until_complete(main_async())
        loop.close()
        
        return jsonify({
            "status": "success", 
            "agent_response": agent_response
        })
    except Exception as e:
        print(f"Error starting new campaign: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/campaign/<string:campaign_id>/characters', methods=['GET'])
def get_campaign_characters(campaign_id):
    """
    API endpoint to get all characters for a specific campaign.
    """
    try:
        characters = list_characters_in_campaign(campaign_id)
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
        from ..data.tools.equipment import get_equipment_details
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
        from ..data.tools.spells import get_spell_details
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
        from ..data.tools.character_data import get_skill_details
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
        from ..data.tools.character_data import get_proficiency_details
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
        from ..data.tools.character_data import get_all_skills
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
        from ..data.tools.character_data import get_all_proficiencies
        profs_data = get_all_proficiencies()
        # profs_data is a dict with 'results' key containing the list
        profs = profs_data.get('results', [])
        mapping = {p['name']: p['index'] for p in profs}
        return jsonify({"status": "success", "mapping": mapping})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/load-campaign/<string:campaign_id>', methods=['GET'])
def load_campaign(campaign_id):
    """
    API endpoint to handle loading an existing campaign.
    Loads campaign data and initializes the GM agent with full context.
    """
    try:
        # For now, just return success - this would typically load campaign data
        return jsonify({
            "status": "success",
            "campaign_id": campaign_id,
            "message": "Campaign loaded successfully"
        })
    except Exception as e:
        print(f"Error loading campaign {campaign_id}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/chat', methods=['POST'])
def chat():
    """
    API endpoint to handle chat messages with the agent.
    Player input is automatically routed to the Root Agent for processing.
    """
    from flask import request
    
    data = request.get_json()
    campaign_id = data.get('campaign_id')
    message = data.get('message')
    
    if not campaign_id or not message:
        return jsonify({"status": "error", "message": "Campaign ID and message are required"}), 400
    
    try:
        # For now, return a simple response since the full agent integration is not set up
        return jsonify({
            "status": "success",
            "agent_response": f"The Dungeon Master received your message: '{message}'. This is a placeholder response while the agent system is being set up."
        })
        
    except Exception as e:
        print(f"Error in chat: {e}")
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

