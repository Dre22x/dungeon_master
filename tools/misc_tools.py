import random
import json
from typing import Dict, Any, Optional
import asyncio
import concurrent.futures
from google.adk.sessions import FirestoreSessionService
from google.adk.runners import Runner
from google.genai import types

# NPC Memory Storage
_npc_memory: Dict[str, dict] = {}

# Global session service for agent communication
_session_service = None

def get_session_service():
    """Get or create the global session service."""
    global _session_service
    if _session_service is None:
        _session_service = FirestoreSessionService()
    return _session_service

async def run_sub_agent(agent, action_data: Dict[str, Any], campaign_id: str = None) -> str:
    """
    Run a sub-agent with the given action data and return the response.
    Creates a unique session for this interaction and terminates it after completion.
    
    Args:
        agent: The LlmAgent instance to run
        action_data: Dictionary containing action information
        campaign_id: Optional campaign ID for session management
    
    Returns:
        The agent's response as a string
    """
    session_service = get_session_service()
    
    # Create a unique session ID for this agent interaction
    # Include timestamp to ensure uniqueness even for same agent/campaign combinations
    import time
    timestamp = int(time.time())
    session_id = f"sub_agent_{agent.name}_{campaign_id or 'default'}_{timestamp}"
    
    try:
        # Create session
        session = await session_service.create_session(
            app_name="dungeon_master",
            user_id="root_agent",
            session_id=session_id,
        )

        # Create runner for the sub-agent
        runner = Runner(
            agent=agent,
            app_name="dungeon_master",
            session_service=session_service
        )

        # Format the action data as a message for the sub-agent
        action_message = f"""
ACTION FROM ROOT AGENT:
Action Type: {action_data.get('action_type', 'unknown')}
Player Input: {action_data.get('player_input', '')}
Target: {action_data.get('target', '')}
Context: {action_data.get('context', '')}
Campaign ID: {action_data.get('campaign_id', campaign_id or 'unknown')}
Game State: {action_data.get('game_state', 'unknown')}

Please process this action according to your role and respond appropriately.
"""

        content = types.Content(
            role='user', 
            parts=[types.Part(text=action_message)]
        )

        # Run the sub-agent
        response = ""
        async for event in runner.run_async(
            user_id="root_agent", 
            session_id=session_id, 
            new_message=content
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    response = event.content.parts[0].text
                break
        
        if not response:
            response = "Sub-agent did not produce a response."
            
        return response
        
    except Exception as e:
        return f"Error running sub-agent {agent.name}: {str(e)}"
    finally:
        # CRITICAL: Always terminate the sub-agent session after completion
        try:
            await session_service.delete_session(
                app_name="dungeon_master",
                user_id="root_agent",
                session_id=session_id
            )
        except Exception as e:
            # Log the error but don't fail the main operation
            print(f"Warning: Failed to delete sub-agent session {session_id}: {str(e)}")

def run_sub_agent_sync(agent, action_data: Dict[str, Any], campaign_id: str = None) -> str:
    """
    Synchronous wrapper for run_sub_agent.
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're already in an async context, we need to create a new task
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, run_sub_agent(agent, action_data, campaign_id))
                return future.result()
        else:
            return asyncio.run(run_sub_agent(agent, action_data, campaign_id))
    except RuntimeError:
        # If no event loop is running, create one
        return asyncio.run(run_sub_agent(agent, action_data, campaign_id))


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

def store_npc_in_memory(campaign_id: str, npc_name: str, npc_data: dict) -> str:
    """
    Store an NPC's data in memory for quick access during conversations.
    
    Args:
        campaign_id: str - The campaign ID
        npc_name: str - The NPC's name
        npc_data: dict - The NPC's complete data
    
    Returns:
        str - Success or error message
    """
    try:
        memory_key = f"{campaign_id}:{npc_name.lower()}"
        _npc_memory[memory_key] = npc_data
        print(f"[NPCMemory] Stored NPC '{npc_name}' in memory for campaign '{campaign_id}'")
        return f"NPC '{npc_name}' has been stored in memory for quick access."
    except Exception as e:
        return f"Error storing NPC '{npc_name}' in memory: {e}"

def get_npc_from_memory(campaign_id: str, npc_name: str) -> Optional[dict]:
    """
    Retrieve an NPC's data from memory.
    
    Args:
        campaign_id: str - The campaign ID
        npc_name: str - The NPC's name
    
    Returns:
        dict or None - The NPC data if found in memory, None otherwise
    """
    memory_key = f"{campaign_id}:{npc_name.lower()}"
    npc_data = _npc_memory.get(memory_key)
    if npc_data:
        print(f"[NPCMemory] Retrieved NPC '{npc_name}' from memory for campaign '{campaign_id}'")
    return npc_data

def clear_npc_memory(campaign_id: str = None, npc_name: str = None) -> str:
    """
    Clear NPC memory, optionally for a specific campaign or NPC.
    
    Args:
        campaign_id: str - Optional campaign ID to clear specific campaign's NPCs
        npc_name: str - Optional NPC name to clear specific NPC
    
    Returns:
        str - Success message
    """
    global _npc_memory
    
    if campaign_id and npc_name:
        # Clear specific NPC
        memory_key = f"{campaign_id}:{npc_name.lower()}"
        if memory_key in _npc_memory:
            del _npc_memory[memory_key]
            return f"Cleared NPC '{npc_name}' from memory for campaign '{campaign_id}'"
        else:
            return f"NPC '{npc_name}' not found in memory for campaign '{campaign_id}'"
    elif campaign_id:
        # Clear all NPCs for specific campaign
        keys_to_remove = [key for key in _npc_memory.keys() if key.startswith(f"{campaign_id}:")]
        for key in keys_to_remove:
            del _npc_memory[key]
        return f"Cleared {len(keys_to_remove)} NPCs from memory for campaign '{campaign_id}'"
    else:
        # Clear all NPC memory
        count = len(_npc_memory)
        _npc_memory.clear()
        return f"Cleared all {count} NPCs from memory"

def list_npcs_in_memory(campaign_id: str = None) -> dict:
    """
    List all NPCs currently stored in memory.
    
    Args:
        campaign_id: str - Optional campaign ID to list only that campaign's NPCs
    
    Returns:
        dict - List of NPCs in memory
    """
    if campaign_id:
        campaign_npcs = {key: value for key, value in _npc_memory.items() 
                        if key.startswith(f"{campaign_id}:")}
        return {
            "npcs": list(campaign_npcs.keys()),
            "count": len(campaign_npcs),
            "campaign_id": campaign_id
        }
    else:
        return {
            "npcs": list(_npc_memory.keys()),
            "count": len(_npc_memory),
            "all_campaigns": True
        }


def route_action_to_root_agent(action_data: Dict[str, Any]) -> str:
    """
    Route a structured action from the Player Interface Agent to the Root Agent.
    
    Args:
        action_data: Dictionary containing action information
            - action_type: Type of action (dialogue, combat, exploration, etc.)
            - player_input: Original player message
            - target: Target of the action (NPC name, monster, location, etc.)
            - context: Additional context about the situation
            - game_state: Current game state if known
    
    Returns:
        Confirmation message that action was routed
    """
    # This function will be called by the Player Interface Agent
    # The actual routing logic will be handled by the system
    action_type = action_data.get("action_type", "unknown")
    player_input = action_data.get("player_input", "")
    target = action_data.get("target", "")
    
    return f"Action routed to Root Agent: {action_type} action targeting {target}"


def route_to_narrative_agent(action_data: Dict[str, Any]) -> str:
    """
    Route an action from the Root Agent to the Narrative Agent.
    
    Args:
        action_data: Dictionary containing action information
            - action_type: Type of action (exploration, combat_description, etc.)
            - player_input: Original player message
            - target: Target of the action
            - context: Additional context about the situation
            - game_state: Current game state
            - campaign_id: Campaign identifier
    
    Returns:
        Response from the Narrative Agent
    """
    try:
        from agents.sub_agents import narrative_agent
        campaign_id = action_data.get('campaign_id', 'default')
        response = run_sub_agent_sync(narrative_agent, action_data, campaign_id)
        return response
    except Exception as e:
        return f"Error routing to Narrative Agent: {str(e)}"


def route_to_rules_lawyer_agent(action_data: Dict[str, Any]) -> str:
    """
    Route an action from the Root Agent to the Rules Lawyer Agent.
    
    Args:
        action_data: Dictionary containing action information
            - action_type: Type of action (combat, skill_check, rules_question, etc.)
            - player_input: Original player message
            - target: Target of the action
            - context: Additional context about the situation
            - game_state: Current game state
            - campaign_id: Campaign identifier
    
    Returns:
        Response from the Rules Lawyer Agent
    """
    try:
        from agents.sub_agents import rules_lawyer_agent
        campaign_id = action_data.get('campaign_id', 'default')
        response = run_sub_agent_sync(rules_lawyer_agent, action_data, campaign_id)
        return response
    except Exception as e:
        return f"Error routing to Rules Lawyer Agent: {str(e)}"


def route_to_npc_agent(action_data: Dict[str, Any]) -> str:
    """
    Route an action from the Root Agent to the NPC Agent.
    
    Args:
        action_data: Dictionary containing action information
            - action_type: Type of action (dialogue, question, interaction, etc.)
            - player_input: Original player message
            - target: NPC name or identifier
            - context: Additional context about the situation
            - game_state: Current game state
            - campaign_id: Campaign identifier
    
    Returns:
        Response from the NPC Agent
    """
    try:
        from agents.sub_agents import npc_agent
        campaign_id = action_data.get('campaign_id', 'default')
        response = run_sub_agent_sync(npc_agent, action_data, campaign_id)
        return response
    except Exception as e:
        return f"Error routing to NPC Agent: {str(e)}"


def route_to_character_creation_agent(action_data: Dict[str, Any]) -> str:
    """
    Route an action from the Root Agent to the Character Creation Agent.
    
    Args:
        action_data: Dictionary containing action information
            - action_type: Type of action (character_creation, etc.)
            - player_input: Original player message
            - context: Additional context about the situation
            - campaign_id: Campaign identifier
    
    Returns:
        Response from the Character Creation Agent
    """
    try:
        from agents.sub_agents import character_creation_agent
        campaign_id = action_data.get('campaign_id', 'default')
        response = run_sub_agent_sync(character_creation_agent, action_data, campaign_id)
        return response
    except Exception as e:
        return f"Error routing to Character Creation Agent: {str(e)}"


def route_to_campaign_creation_agent(action_data: Dict[str, Any]) -> str:
    """
    Route an action from the Root Agent to the Campaign Creation Agent.
    
    Args:
        action_data: Dictionary containing action information
            - action_type: Type of action (campaign_outline, etc.)
            - player_input: Original player message
            - context: Additional context about the situation
            - campaign_id: Campaign identifier
    
    Returns:
        Response from the Campaign Creation Agent
    """
    try:
        from agents.sub_agents import campaign_creation_agent
        campaign_id = action_data.get('campaign_id', 'default')
        response = run_sub_agent_sync(campaign_creation_agent, action_data, campaign_id)
        return response
    except Exception as e:
        return f"Error routing to Campaign Creation Agent: {str(e)}"


def route_to_player_interface_agent(action_data: Dict[str, Any]) -> str:
    """
    Route an action from the Root Agent to the Player Interface Agent.
    
    Args:
        action_data: Dictionary containing action information
            - action_type: Type of action (player_communication, etc.)
            - player_input: Original player message
            - context: Additional context about the situation
            - campaign_id: Campaign identifier
    
    Returns:
        Response from the Player Interface Agent
    """
    try:
        from agents.sub_agents import player_interface_agent
        campaign_id = action_data.get('campaign_id', 'default')
        response = run_sub_agent_sync(player_interface_agent, action_data, campaign_id)
        return response
    except Exception as e:
        return f"Error routing to Player Interface Agent: {str(e)}"





def send_response_to_root_agent(response_data: Dict[str, Any]) -> str:
    """
    Send a response from a sub-agent back to the Root Agent.
    
    Args:
        response_data: Dictionary containing response information
            - agent_type: Type of agent sending the response (narrative, rules_lawyer, npc)
            - response_content: The actual response content
            - action_type: Type of action this is responding to
            - context: Additional context about the response
            - campaign_id: Campaign identifier
    
    Returns:
        Confirmation message that response was sent
    """
    # This function will be called by sub-agents
    # The actual routing logic will be handled by the system
    agent_type = response_data.get("agent_type", "unknown")
    action_type = response_data.get("action_type", "unknown")
    
    return f"Response sent from {agent_type} agent to Root Agent for {action_type} action"


if __name__ == "__main__":
  print(roll_dice("d20", 3))