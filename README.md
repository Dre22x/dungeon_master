# AI Dungeon Master

An AI-powered Dungeons & Dragons game master that uses Google's Agent Development Kit (ADK) to create immersive tabletop RPG experiences.

## Features

- **Multi-Agent System**: Specialized agents for different aspects of D&D gameplay
- **Web Interface**: Flask-based web UI for campaign management
- **ADK Integration**: Visual development interface for agent interaction
- **Firestore Database**: Persistent campaign and character storage
- **Character Creation**: Automated character creation with proper D&D rules
- **Combat System**: Rules-based combat mechanics
- **NPC Interactions**: Dynamic NPC roleplaying
- **Story Generation**: AI-driven narrative progression

## Setup

### Prerequisites

1. **Python 3.8+** installed
2. **Google ADK** installed: `pip install google-adk`
3. **Google API Key** configured (already set in the code)
4. **Firestore** database configured

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

## Agent System

The application uses a multi-agent architecture:

- **Root Agent**: Master orchestrator and game flow manager
- **Character Creation Agent**: Handles character creation and customization
- **Narrative Agent**: Provides environmental descriptions and story progression
- **NPC Agent**: Roleplays non-player characters during interactions
- **Rules Lawyer Agent**: Handles combat, skill checks, and game mechanics
- **Player Interface Agent**: Manages direct player communication

## File Structure

```
dungeon_master/
├── agents/                 # Agent definitions and instructions
├── tools/                  # D&D game mechanics and tools
├── UI/                     # Flask web interface
├── firestore/              # Database management
├── config/                 # Configuration files
├── adk.yaml               # ADK configuration
├── main.py                # Direct execution mode
└── start_app.py           # Startup script
```

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

## Development

### Testing
Run the test suite:
```bash
python -m pytest test_*.py
```

### Adding New Agents
1. Create agent definition in `agents/sub_agents.py`
2. Add instruction file in `agents/instructions/`
3. Update `adk.yaml` configuration
4. Register agent in `agents/agent.py`

### Adding New Tools
1. Create tool function in `tools/` directory
2. Add tool to agent configuration
3. Update agent instructions to use the tool

## License

This project is licensed under the MIT License - see the LICENSE file for details.
