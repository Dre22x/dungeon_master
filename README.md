# AI Dungeon Master

An AI-powered Dungeons & Dragons game master that uses Google's Agent Development Kit (ADK) to create immersive tabletop RPG experiences.

## 🎯 Project Overview

This project demonstrates advanced AI agent orchestration, multi-agent systems, and real-time game mechanics. Built with modern Python technologies including Google ADK, Firebase Firestore, and Flask, it showcases:

- **Multi-Agent Architecture**: Hierarchical agent system with specialized roles
- **Real-time Game Mechanics**: Combat resolution, character creation, and story generation
- **Persistent State Management**: Firebase integration for campaign persistence
- **Modern Web Interface**: Responsive Flask-based UI
- **Comprehensive Testing**: Extensive test suite covering all major functionality

## 🚀 Features

- **Multi-Agent System**: Specialized agents for different aspects of D&D gameplay
- **Character Creation**: Guided character creation with all D&D 5e options
- **Campaign Management**: Persistent campaign storage and loading
- **Combat Mechanics**: Automated combat resolution and dice rolling
- **NPC Interactions**: Dynamic NPC dialogue and roleplay
- **Story Generation**: AI-driven narrative and environmental descriptions
- **Custom UI**: Web-based interface for seamless gameplay experience

## 🛠️ Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Google ADK** installed: `pip install google-adk`
3. **Firebase/Firestore** project set up
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

3. **Set up Firebase credentials**:
   - Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
   - Generate a service account key in Project Settings > Service Accounts
   - Replace the template in `config/service-account-key.json` with your actual credentials
   - **⚠️ Never commit real credentials to version control**
4. **Configure environment variables**:
   - Copy `.env.template` to `.env`
   - Fill in your actual API keys and configuration values
   - **⚠️ Never commit the .env file to version control**

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

## 🏗️ Architecture

### Agent Hierarchy

The system uses a hierarchical agent architecture:

```
Root Agent (Orchestrator)
├── Character Creation Agent
├── Campaing Outline Generation Agent
├── Narrative Agent
├── Rules Lawyer Agent
└── NPC Agent
```

### Key Components

- **Root Agent**: Master coordinator that routes actions to specialist agents
- **Character Creation Agent**: Guides players through character creation
- **Campaing Outline Generation Agent**: Generates campaign outlines and story structure
- **Narrative Agent**: Handles story elements and environmental descriptions
- **Rules Lawyer Agent**: Manages combat mechanics and rules questions
- **NPC Agent**: Handles NPC dialogue and roleplay


### Data Flow

1. **Player Input** → Root Agent receives and processes input
2. **Action Routing** → Root Agent determines appropriate specialist
3. **Specialist Processing** → Specialist agent handles the specific task
4. **Response Coordination** → Root Agent coordinates multiple responses if needed
5. **Player Output** → Final response delivered to player

## ⚙️ Configuration

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

- **State**: All global state variables are stored to maintain campign continuity

## 🧪 Development

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_character_creation.py

# Run with coverage
pytest --cov=.
```

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
   
## 🔧 Troubleshooting

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

## 📁 Project Structure

```
dungeon_master/
├── src/                        # Main source code
│   ├── agents/                 # AI agent system
│   │   ├── agent.py           # Root agent implementation
│   │   ├── sub_agents.py      # Specialized agent definitions
│   │   ├── config_loader.py   # Agent configuration management
│   │   └── instructions/      # Agent instruction files
│   ├── core/                   # Core game logic
│   │   ├── session_manager.py # Session state management
│   │   └── utils.py           # Utility functions
│   ├── data/                   # Game data and rules engine
│   │   └── tools/             # Game mechanics and data
│   │       ├── character_data.py # Character management
│   │       ├── game_mechanics.py # Combat and game rules
│   │       ├── campaign_outline.py # Story generation
│   │       ├── races.py       # Race definitions
│   │       ├── classes.py     # Class definitions
│   │       ├── spells.py      # Spell system
│   │       ├── equipment.py   # Equipment and items
│   │       ├── monsters.py    # Monster data
│   │       ├── magic_items.py # Magical items
│   │       ├── weapons.py     # Weapon definitions
│   │       ├── traits.py      # Character traits
│   │       ├── subraces.py    # Subrace options
│   │       ├── subclasses.py  # Subclass options
│   │       └── rules.py       # Game rules engine
│   ├── database/               # Database layer
│   │   └── firestore/         # Firebase integration
│   │       ├── database_manager.py # Database operations
│   │       └── db_utils.py    # Database utility functions
│   ├── web/                    # Web interface
│   │   ├── app.py             # Flask application
│   │   ├── index.html         # Main page template
│   │   └── campaign.html      # Campaign interface template
│   ├── main.py                 # Console application entry point
│   └── start_app.py           # Web application startup
├── config/                      # Configuration files
│   ├── adk.yaml               # Agent configuration
│   └── .env.template          # Environment variables template
├── scripts/                     # Utility scripts
│   └── quick_start.py         # Automated setup script
├── tests/                       # Test suite
├── docs/                        # Documentation
├── examples/                    # Usage examples
├── requirements.txt             # Python dependencies
├── setup.py                     # Package configuration
├── .gitignore                   # Git ignore rules
├── .gitattributes              # Git attributes
├── LICENSE                      # Project license
└── README.md                    # This file
```

**🏗️ Professional Architecture**: This clean structure demonstrates industry-standard Python packaging, clear separation of concerns, and maintainable code organization that recruiters will appreciate.
## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔒 Security Notes

- **Never commit real Firebase credentials** to version control
- The `config/service-account-key.json` file contains a template - replace with your actual credentials
- **Never commit the .env file** to version control
- Use `.env.template` as a starting point for your configuration
- Ensure your `.gitignore` properly excludes sensitive files
- Use environment variables for production deployments
