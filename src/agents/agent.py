from google.adk.agents import LlmAgent
from .sub_agents import narrative_agent, npc_agent, rules_lawyer_agent, character_creation_agent, campaign_outline_generation_agent
from .config_loader import get_model_for_agent
from google.adk.models.lite_llm import LiteLlm
import os
import sys
from data.tools.misc_tools import set_state, save_campaign, get_state

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
  sub_agents=[narrative_agent, npc_agent, rules_lawyer_agent, character_creation_agent, campaign_outline_generation_agent],
  tools=[set_state, save_campaign, get_state]
)

