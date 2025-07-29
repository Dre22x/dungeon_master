# Agent Hierarchy and Tool Calling Strategy

## Overview

This document outlines the strict agent hierarchy implemented in the Dungeon Master system, where all agent-to-agent communication is handled through tool calling rather than direct communication.

## Agent Hierarchy

### 1. Player Interface Agent
- **Role**: Single point of contact for all player interactions
- **Communication**: 
  - Receives all player input directly
  - Translates player input into structured action dictionaries
  - Uses `route_action_to_root_agent` to send actions to Root Agent
  - Delivers final responses back to player
- **Tools**: `route_action_to_root_agent`, game state management tools

### 2. Root Agent
- **Role**: Master coordinator and orchestrator
- **Communication**:
  - Receives structured actions from Player Interface Agent
  - Routes actions to appropriate sub-agents using tool calling
  - Coordinates responses from multiple sub-agents when needed
  - Returns final coordinated responses to Player Interface Agent
- **Tools**: Routing tools (`route_to_narrative_agent`, `route_to_rules_lawyer_agent`, etc.), campaign management tools

### 3. Sub-Agents
- **Narrative Agent**: Handles environmental descriptions, story progression, campaign outlines
- **Rules Lawyer Agent**: Handles combat mechanics, skill checks, rules questions
- **NPC Agent**: Handles NPC dialogue and roleplay
- **Character Creation Agent**: Handles character creation (standalone with direct player communication)

## Tool Calling Strategy

### Action Flow
1. **Player Input** → Player Interface Agent
2. **Player Interface Agent** → `route_action_to_root_agent` → Root Agent
3. **Root Agent** → `route_to_[sub_agent]` → Sub-Agent (actually invokes the sub-agent)
4. **Sub-Agent** → `send_response_to_root_agent` → Root Agent
5. **Root Agent** → Player Interface Agent
6. **Player Interface Agent** → Player

### Key Improvement
The new routing system **actually invokes** the sub-agents using the ADK framework instead of just returning confirmation messages. Each `route_to_[sub_agent]` function:
- Creates a unique session for the sub-agent
- Runs the sub-agent with the provided action data
- Returns the actual response from the sub-agent
- Handles both synchronous and asynchronous execution contexts

### Action Dictionary Structure
```json
{
  "action_type": "dialogue|combat|exploration|question|character_creation|meta",
  "player_input": "exact player message",
  "target": "npc_name|monster_name|location|etc",
  "context": "additional context about the situation",
  "game_state": "current game state if known",
  "campaign_id": "campaign identifier"
}
```

### Response Dictionary Structure
```json
{
  "agent_type": "narrative|rules_lawyer|npc|character_creation",
  "response_content": "the actual response content",
  "action_type": "type of action this is responding to",
  "context": "additional context about the response",
  "campaign_id": "campaign identifier"
}
```

## Special Cases

### Character Creation Agent
- **Standalone Status**: Can communicate directly with players during character creation
- **Direct Player Interaction**: No need to route through Player Interface Agent
- **Agent Communication**: Uses `send_response_to_root_agent` when needing to communicate with other agents
- **Unique Privilege**: Only agent besides Player Interface Agent that can talk directly to players

### Complex Interactions
When multiple agents are needed (e.g., combat):
1. **Root Agent** routes combat action to **Rules Lawyer Agent**
2. **Rules Lawyer Agent** processes mechanics and creates combat result
3. **Rules Lawyer Agent** sends response to **Root Agent**
4. **Root Agent** routes combat result to **Narrative Agent** for description
5. **Narrative Agent** creates narrative description and sends to **Root Agent**
6. **Root Agent** coordinates final response and sends to **Player Interface Agent**

## Tool Functions

### Routing Tools (Player Interface Agent → Root Agent)
- `route_action_to_root_agent(action_data)`: Send structured actions to Root Agent

### Routing Tools (Root Agent → Sub-Agents)
- `route_to_narrative_agent(action_data)`: Route to Narrative Agent (actually invokes the agent)
- `route_to_rules_lawyer_agent(action_data)`: Route to Rules Lawyer Agent (actually invokes the agent)
- `route_to_npc_agent(action_data)`: Route to NPC Agent (actually invokes the agent)
- `route_to_character_creation_agent(action_data)`: Route to Character Creation Agent (actually invokes the agent)
- `route_to_campaign_creation_agent(action_data)`: Route to Campaign Creation Agent (actually invokes the agent)
- `route_to_player_interface_agent(action_data)`: Route to Player Interface Agent (actually invokes the agent)

### Response Tools (Sub-Agents → Root Agent)
- `send_response_to_root_agent(response_data)`: Send responses back to Root Agent

## Session Management Strategy

### Root Agent Session:
- **Only long-running session** in the entire system
- **Persists throughout the campaign lifecycle**
- **Maintains game state and context** across all interactions
- **Coordinates all sub-agent activities**

### Sub-Agent Sessions:
- **Temporary sessions** created for each specific task
- **Unique session IDs** with timestamps to prevent conflicts
- **Automatically terminated** after task completion
- **No lingering sessions** or memory leaks
- **Isolated execution** for each interaction

### Session Lifecycle:
1. **Root Agent** receives action from Player Interface Agent
2. **Root Agent** creates unique session for sub-agent
3. **Sub-Agent** executes task in temporary session
4. **Sub-Agent** sends response back to Root Agent
5. **Sub-Agent session is terminated** automatically
6. **Root Agent** continues with persistent session

## Benefits of This Structure

1. **Clear Hierarchy**: Every agent has a defined role and communication path
2. **Tool-Based Communication**: All agent interactions are explicit and traceable
3. **Coordination**: Root Agent can coordinate complex multi-agent scenarios
4. **Isolation**: Sub-agents are isolated and focused on their specific tasks
5. **Scalability**: Easy to add new agents or modify communication patterns
6. **Debugging**: Tool calls provide clear audit trail of agent interactions
7. **Resource Management**: No lingering sessions or memory leaks
8. **Session Isolation**: Each sub-agent task runs in a clean, isolated environment

## Implementation Notes

- All agent instructions have been updated to reflect this hierarchy
- Tool calling functions are implemented in `tools/misc_tools.py`
- Agent configurations updated in `agents/sub_agents.py` and `agents/agent.py`
- Character Creation Agent maintains its standalone nature while following the hierarchy for agent communication
- The system maintains backward compatibility while enforcing the new structure

## Example Workflows

### Simple Dialogue
1. Player: "Hello blacksmith"
2. Player Interface Agent: `route_action_to_root_agent({"action_type": "dialogue", "target": "blacksmith", ...})`
3. Root Agent: `route_to_npc_agent({"action_type": "dialogue", "target": "blacksmith", ...})`
4. NPC Agent: `send_response_to_root_agent({"agent_type": "npc", "response_content": "[Blacksmith] Greetings!", ...})`
5. Root Agent → Player Interface Agent
6. Player Interface Agent: "The blacksmith looks up and smiles. 'Greetings, traveler!'"

### Combat Action
1. Player: "I attack the goblin"
2. Player Interface Agent: `route_action_to_root_agent({"action_type": "combat", "target": "goblin", ...})`
3. Root Agent: `route_to_rules_lawyer_agent({"action_type": "combat", "target": "goblin", ...})`
4. Rules Lawyer Agent: Processes combat, creates result, `send_response_to_root_agent(...)`
5. Root Agent: `route_to_narrative_agent({"action_type": "combat_description", ...})`
6. Narrative Agent: Describes combat, `send_response_to_root_agent(...)`
7. Root Agent → Player Interface Agent
8. Player Interface Agent: "Your sword strikes true, cutting deep into the goblin's flesh..."

This structure ensures that all agent communication is explicit, traceable, and follows a clear hierarchy while maintaining the immersive experience for players. 