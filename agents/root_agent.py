import os
import asyncio
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts
from sub_agents import narrative_agent, npc_agent, rules_lawyer_agent
# Globals
MODEL_NAME = "gemini-2.0-flash"

# --- Create Root Agent ---
root_agent = LlmAgent(
  name="root_agent",
  model=MODEL_NAME,
  description="You are the master orchestrator and Game Master for a Dungeons & Dragons campaign. Your primary function is to manage the flow of the game and delegate tasks to your specialist agents. You do not interact with the player directly. ",
  instruction="""Your workflow is as follows:
    1.  Receive a structured command from the Player Interface Agent.
    2.  Analyze the command and the current game state ('exploration', 'combat', 'dialogue').
    3.  Based on this analysis, determine which specialist agent is best suited for the task.
    4.  Formulate a clear, concise, and direct instruction for that specialist agent.

    Your output is ALWAYS a command directed at another agent.

    Example Interactions:
    -   If the input is `{"intent": "attack", "actor": "player1", "target": "goblin_2"}`, and the game state is 'combat', your output should be a command to the Rules Lawyer: "Resolve attack: Player1 attacks Goblin_2."
    -   If the input is `{"intent": "look_around", "actor": "player1"}`, and the game state is 'exploration', your output should be a command to the Narrative Agent: "Describe the current location for Player1 in detail."
    -   If the input is `{"intent": "talk", "actor": "player1", "target": "blacksmith_gloria"}`, you must first change the state to 'dialogue' and then command the NPC Agent: "Initiate dialogue for Player1 with NPC: blacksmith_gloria."

    You are the central hub. Be logical, efficient, and precise in your commands.""",
  sub_agents=[narrative_agent, npc_agent, rules_lawyer_agent],
  tools=[change_game_state, start_combat, end_combat, get_player_location]
)

