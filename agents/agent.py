from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts
from agents.sub_agents import narrative_agent, npc_agent, rules_lawyer_agent, character_creation_agent, campaign_creation_agent, player_interface_agent
from agents.config_loader import get_model_for_agent
import os
import sys
from firestore.db_utils import *
from tools.campaign_outline import load_campaign_outline
from tools.misc_tools import route_to_narrative_agent, route_to_rules_lawyer_agent, route_to_npc_agent, route_to_character_creation_agent, route_to_campaign_creation_agent, route_to_player_interface_agent

# Set up environment
os.environ["GOOGLE_API_KEY"] = "AIzaSyAMEgPT8FjJ2ToGvTsn2o0GoodN_wV4Qy8"

def load_instructions(filename: str) -> str:
    """
    Load instructions from a text file in the instructions directory.
    """
    instructions_path = os.path.join(os.path.dirname(__file__), 'instructions', filename)
    try:
        with open(instructions_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"ERROR: Instructions file {filename} not found at {instructions_path}")
        print("Please ensure the instructions file exists in the agents/instructions/ directory.")
        sys.exit(1)

# --- Create Root Agent ---
root_agent = LlmAgent(
  name="root_agent",
  model=get_model_for_agent("root_agent"),
  description="You are the master orchestrator and Game Master for a Dungeons & Dragons campaign. Your primary function is to manage the flow of the game and delegate tasks to your specialist agents. You do not interact with the player directly. ",
  instruction=load_instructions("root_agent.txt"),
  sub_agents=[narrative_agent, npc_agent, rules_lawyer_agent, character_creation_agent, campaign_creation_agent, player_interface_agent],
  tools=[route_to_narrative_agent, route_to_rules_lawyer_agent, route_to_npc_agent, route_to_character_creation_agent, route_to_campaign_creation_agent, route_to_player_interface_agent, create_campaign, save_character_to_campaign, change_game_state, get_game_state, save_campaign, load_campaign, load_campaign_outline]
)

