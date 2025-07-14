# AI Dungeon Master

An AI-powered Dungeons & Dragons game master that uses Google's Agent Development Kit (ADK) to create immersive tabletop RPG experiences.

## Features

- **Multi-Agent System**: Specialized agents for different aspects of D&D gameplay
- **Web Interface**: Flask-based web UI for campaign management
- **ADK Integration**: Visual development interface for agent interaction
- **Firestore Database**: Persistent campaign and character storage
- **Character Creation**: Automated character creation with proper D&D rules
- **Multiple Character Support**: Create multiple characters for a single campaign
- **Campaign Outline Generation**: Unique story outlines for each campaign
- **Dynamic Model Configuration**: Agent models configured via YAML file
- **Combat System**: Rules-based combat mechanics
- **NPC Interactions**: Dynamic NPC roleplaying
- **Story Generation**: AI-driven narrative progression

## Setup

### Prerequisites

1. **Python 3.8+** installed
2. **Google ADK** installed: `pip install google-adk`
3. **Google API Key** configured (already set in the code)
4. **Firestore** database configured
5. **PyYAML** installed: `pip install pyyaml`

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd dungeon_master
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python init_database.py
   ```

## Running the Application

### Automated Startup (Recommended)

Use the startup script to launch both services automatically:
```bash
python start_app.py
```

This will:
- Start the Flask web server on `http://localhost:5001`
- Start the ADK web interface on `http://localhost:8000`
- Check for port conflicts and ADK installation
- Provide graceful shutdown with Ctrl+C

### Manual Setup (Alternative)

If you prefer to run services separately:

**Terminal 1 - Flask Web Server:**
```bash
cd UI
python app.py
```

**Terminal 2 - ADK Development UI:**
```bash
adk web .
```

## Usage

1. **Start both services** (Flask + ADK dev UI)
2. **Open the web interface** at `http://localhost:5001`
3. **Create a new campaign** or **load an existing one**
4. **Use the ADK dev UI** at `http://localhost:8000` for agent interaction
5. **Interact with your AI Dungeon Master** through the ADK interface

### Multiple Character Creation

The system now supports creating multiple characters for a single campaign:

- **Automatic Prompting**: After creating your first character, the AI will ask if you want to create another
- **Party Balance**: The AI will suggest complementary character types for balanced party compositions
- **Flexible Creation**: You can create as many characters as you want for your campaign
- **Character Management**: All characters are saved to the campaign and can be viewed in the web interface

**Example Party Compositions:**
- **Balanced Party**: Tank (Fighter/Paladin) + Healer (Cleric) + Damage (Wizard/Rogue) + Support (Bard/Ranger)
- **Combat Focused**: Multiple fighters, paladins, or barbarians
- **Magic Heavy**: Multiple spellcasters (Wizard, Cleric, Bard, Sorcerer)
- **Stealth Focused**: Rogues, rangers, and monks
- **Support Heavy**: Bards, clerics, and druids

### Campaign Outline Generation

Each new campaign automatically generates a unique story outline:

- **Unique Story Elements**: Every campaign gets a distinct title, theme, and main quest
- **Structured Narrative**: Three-act story structure with clear plot progression
- **Key NPCs and Monsters**: Pre-defined characters and creatures for the story
- **Consistent Storytelling**: The AI uses the outline as a guide for all narrative decisions
- **Theme Variety**: Supports classic fantasy, horror, political intrigue, and other themes

**Campaign Outline Structure:**
```json
{
  "title": "Unique Campaign Title",
  "theme": "Story Theme",
  "summary": "Brief overview of the campaign",
  "main_quest": "Clear primary objective",
  "plot_acts": {
    "act_1": { "title": "Act Title", "summary": "What happens", "key_location": "Location", "primary_conflict": "Challenge" },
    "act_2": { "title": "Act Title", "summary": "What happens", "key_location": "Location", "primary_conflict": "Challenge" },
    "act_3": { "title": "Act Title", "summary": "What happens", "key_location": "Location", "primary_conflict": "Challenge" }
  },
  "key_npcs": [{"name": "NPC Name", "location": "Where found", "role": "Story role"}],
  "key_monsters": [{"name": "Monster Name", "location": "Where found", "role": "Story role"}]
}
```

### Agent Model Configuration

The system now supports dynamic model configuration through the YAML file:

- **Centralized Configuration**: All agent models are configured in `adk.yaml`
- **Easy Model Switching**: Change models by updating the YAML file
- **Per-Agent Models**: Different agents can use different models
- **Fallback Support**: Default model used if configuration is missing

**Example YAML Configuration:**
```yaml
agents:
  - name: root_agent
    model: gemini-2.5-flash-lite-preview-06-17
    description: "Master orchestrator and Game Master"
  - name: narrative_agent
    model: gemini-2.5-flash-lite-preview-06-17
    description: "Provides environmental descriptions"
    # ... other agents
```

## Agent System

The application uses a multi-agent architecture:

- **Root Agent**: Master orchestrator and game flow manager
- **Character Creation Agent**: Handles character creation and customization
- **Narrative Agent**: Provides environmental descriptions and story progression
- **NPC Agent**: Roleplays NPCs during dialogue interactions
- **Rules Lawyer Agent**: Handles combat, skill checks, and game mechanics
- **Player Interface Agent**: Manages direct player communication

## File Structure

```
dungeon_master/
├── agents/                 # Agent definitions and instructions
│   ├── config_loader.py   # Configuration loading utilities
│   ├── agent.py           # Main root agent
│   └── sub_agents.py      # Sub-agent definitions
├── tools/                  # D&D game mechanics and tools
│   └── campaign_outline.py # Campaign outline generation tools
├── UI/                     # Flask web interface
├── firestore/              # Database management
├── config/                 # Configuration files
├── adk.yaml               # ADK configuration with agent models
├── main.py                # Direct execution mode
├── start_app.py           # Startup script
├── test_multiple_character_creation.py  # Test for multiple character creation
├── test_campaign_outline_generation.py  # Test for campaign outline generation
└── test_config_loading.py # Test for configuration loading
```

## Testing

### Configuration Loading Test
Test the new agent configuration loading functionality:
```bash
python test_config_loading.py
```

This test will:
- Verify that agent models can be loaded from the YAML file
- Test individual agent model retrieval
- Verify agent creation with loaded configurations
- Test YAML parsing functionality

### Campaign Outline Generation Test
Test the campaign outline generation functionality:
```bash
python test_campaign_outline_generation.py
```

This test will:
- Create a new campaign
- Verify that a unique campaign outline is generated
- Test multiple campaigns to ensure outline uniqueness
- Verify that campaign loading references the outline

### Multiple Character Creation Test
Test the multiple character creation functionality:
```bash
python test_multiple_character_creation.py
```

This test will:
- Create a new campaign
- Create multiple characters (Fighter and Wizard)
- Verify that the AI asks about creating additional characters
- Check that all characters are properly saved
- Test campaign loading with multiple characters

### Other Tests
Run the complete test suite:
```bash
python -m pytest test_*.py
```

## Configuration

### Agent Model Configuration

To change the model used by an agent, edit the `adk.yaml` file:

```yaml
agents:
  - name: root_agent
    model: gemini-2.5-flash-lite-preview-06-17  # Change this line
    description: "Master orchestrator and Game Master"
    instruction_file: agents/instructions/root_agent.txt
    # ... other configuration
```

Available models include:
- `gemini-2.5-flash-lite-preview-06-17` (current default)
- `gemini-2.0-flash`
- `gemini-1.5-pro`
- Other Gemini models as available

### Adding New Agents

1. Add agent configuration to `adk.yaml`:
   ```yaml
   - name: new_agent
     model: gemini-2.5-flash-lite-preview-06-17
     description: "Description of the new agent"
     instruction_file: agents/instructions/new_agent.txt
   ```

2. Create agent definition in `agents/sub_agents.py`
3. Add instruction file in `agents/instructions/`
4. Register agent in `agents/agent.py` if needed

## Troubleshooting

### "No agents found" in ADK dev UI
- Ensure `adk.yaml` exists in the project root
- Verify all agent instruction files are present
- Check that `adk web .` is running from the project root

### Campaign loading issues
- Verify Firestore database is properly configured
- Check that `config/service-account-key.json` exists
- Ensure database initialization was successful

### Flask server issues
- Check that port 5001 is available
- Verify all Python dependencies are installed
- Check the console for error messages

### Multiple character creation not working
- Ensure you're using the latest agent instructions
- Check that the Character Creation Agent is properly configured
- Verify that the campaign is being saved correctly

### Campaign outline generation not working
- Ensure the Narrative Agent has access to the campaign outline tools
- Check that the database is properly configured for outline storage
- Verify that the agent instructions include outline generation workflow

### Configuration loading issues
- Ensure `adk.yaml` file exists and is properly formatted
- Check that PyYAML is installed: `pip install pyyaml`
- Verify that agent names in YAML match agent names in code
- Check console for configuration loading error messages

## Development

### Testing
Run the test suite:
```bash
python -m pytest test_*.py
```

### Adding New Agents
1. Create agent definition in `agents/sub_agents.py`
2. Add instruction file in `agents/instructions/`
3. Update `adk.yaml` configuration with model name
4. Register agent in `agents/agent.py`

### Adding New Tools
1. Create tool function in `tools/` directory
2. Add tool to agent configuration in `adk.yaml`
3. Update agent instructions to use the tool

## License

This project is licensed under the MIT License - see the LICENSE file for details.
