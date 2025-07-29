# AI Dungeon Master

An AI-powered Dungeons & Dragons game master that uses Google's Agent Development Kit (ADK) to create immersive tabletop RPG experiences.

## Features

- **Multi-Agent System**: Specialized agents for different aspects of D&D gameplay
- **Character Creation**: Guided character creation with all D&D 5e options
- **Campaign Management**: Persistent campaign storage and loading
- **Combat Mechanics**: Automated combat resolution and dice rolling
- **NPC Interactions**: Dynamic NPC dialogue and roleplay
- **Story Generation**: AI-driven narrative and environmental descriptions
- **Custom UI**: Web-based interface for seamless gameplay experience

## Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Google ADK** installed: `pip install google-adk`
3. **Firebase/Firestore** project set up with service account key
4. **Google Cloud** credentials configured

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd dungeon_master
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up configuration**:
   - Place your Firebase service account key in `config/service-account-key.json`
   - Ensure `adk.yaml` is in the project root

4. **Initialize the database**:
   ```bash
   python init_database.py
   ```

### Running the Application

**Option 1: Start both services with one command**
```bash
python start_app.py
```

**Option 2: Start services separately**

**Terminal 1 - Flask Web Server:**
```bash
python UI/app.py
```
- Web interface available at `http://localhost:5001`
- Check for port conflicts and ADK installation

**Terminal 2 - Development:**
```bash
# Optional: For development and debugging
adk web .
```

### Usage

1. **Start both services** (Flask + ADK dev UI)
2. **Open your browser** to `http://localhost:5001`
3. **Click "New Campaign"** to start a new adventure
4. **Interact with your AI Dungeon Master** through the web interface
5. **Create characters, explore, and battle** in your custom D&D world

## Architecture

### Agent Hierarchy

The system uses a hierarchical agent architecture:

```
Root Agent (Orchestrator)
├── Character Creation Agent
├── Campaign Creation Agent
├── Narrative Agent
├── Rules Lawyer Agent
├── NPC Agent
└── Player Interface Agent
```

### Key Components

- **Root Agent**: Master coordinator that routes actions to specialist agents
- **Character Creation Agent**: Guides players through character creation
- **Campaign Creation Agent**: Generates campaign outlines and story structure
- **Narrative Agent**: Handles story elements and environmental descriptions
- **Rules Lawyer Agent**: Manages combat mechanics and rules questions
- **NPC Agent**: Handles NPC dialogue and roleplay
- **Player Interface Agent**: Manages direct player communication

### Data Flow

1. **Player Input** → Player Interface Agent
2. **Action Routing** → Root Agent determines appropriate specialist
3. **Specialist Processing** → Specialist agent handles the specific task
4. **Response Coordination** → Root Agent coordinates multiple responses if needed
5. **Player Output** → Final response delivered to player

## Configuration

### Model Configuration

All agents use models defined in `adk.yaml`. To change the model used by an agent, edit the `adk.yaml` file:

```yaml
agents:
  root_agent:
    model: gemini-1.5-flash
  character_creation_agent:
    model: gemini-1.5-flash
  # ... other agents
```

### Database Configuration

The application uses Firebase Firestore for persistent storage:

- **Campaigns**: Campaign data, context, and state
- **Characters**: Player character sheets and data
- **NPCs**: Non-player character information
- **Monsters**: Monster statistics and data
- **Locations**: World locations and descriptions
- **Quests**: Active quests and objectives

## Development

### Adding New Tools

1. **Create the tool function** in the appropriate module under `tools/`
2. **Add the tool to the agent** in `agents/agent.py` or `agents/sub_agents.py`
3. **Update agent instructions** to include the new tool
4. **Test the integration** with the agent system

### Adding New Agents

1. **Create agent configuration** in `adk.yaml`:
   ```yaml
   agents:
     new_agent:
       model: gemini-1.5-flash
       description: "Description of the new agent"
   ```

2. **Create agent instance** in `agents/sub_agents.py`:
   ```python
   new_agent = LlmAgent(
       name="new_agent",
       model=get_model_for_agent("new_agent"),
       description="Description of the new agent",
       instruction=load_instructions("new_agent.txt"),
       tools=[tool1, tool2, tool3]
   )
   ```

3. **Add routing tool** in `tools/misc_tools.py`:
   ```python
   def route_to_new_agent(action_data: Dict[str, Any]) -> str:
       return run_sub_agent_sync(new_agent, action_data)
   ```

4. **Update root agent** to include the new agent and routing tool

## Troubleshooting

### Common Issues

1. **"No agents found" in ADK dev UI**
   - Ensure `adk.yaml` exists in the project root
   - Check that the agent configurations are correct
   - Verify that `adk web .` is running from the project root

2. **Database connection errors**
   - Verify `config/service-account-key.json` exists and is valid
   - Check Firebase project configuration
   - Ensure Firestore is enabled in your Firebase project

3. **Model not found errors**
   - Ensure `adk.yaml` file exists and is properly formatted
   - Check that the model names are correct
   - Verify Google Cloud credentials are set up

4. **Tool not found errors**
   - Check that the tool is properly imported
   - Verify the tool is added to the agent's tools list
   - Update `adk.yaml` configuration with model name

5. **Session management issues**
   - Check that the session service is properly initialized
   - Verify session IDs are being generated correctly
   - Ensure proper session cleanup is happening

### Debug Mode

Enable debug logging by setting the `DEBUG` environment variable:

```bash
export DEBUG=1
python UI/app.py
```

This will provide detailed logging of agent interactions, tool calls, and session management.

## Project Structure

```
dungeon_master/
├── agents/                    # Agent definitions and instructions
│   ├── agent.py              # Root agent configuration
│   ├── sub_agents.py         # Specialist agent definitions
│   ├── config_loader.py      # Model configuration loading
│   └── instructions/         # Agent instruction files
├── tools/                    # Tool implementations
│   ├── character_data.py     # Character creation tools
│   ├── campaign_outline.py   # Campaign management tools
│   ├── game_mechanics.py     # Combat and rules tools
│   ├── misc_tools.py         # Routing and utility tools
│   └── ...                   # Other specialized tools
├── firestore/                # Database utilities
│   ├── database_manager.py   # Database operations
│   └── db_utils.py          # Database utility functions
├── UI/                       # Web interface
│   ├── app.py               # Flask application
│   ├── index.html           # Main page
│   └── campaign.html        # Campaign interface
├── config/                   # Configuration files
│   └── service-account-key.json
├── tests/                    # Test files
├── adk.yaml                 # ADK configuration with agent models
├── start_app.py             # Application startup script
└── README.md                # This file
```

## Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests** for new functionality
5. **Submit a pull request**

## License

This project is licensed under the MIT License - see the LICENSE file for details.
