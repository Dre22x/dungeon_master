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

## 🏗️ Architecture

### Agent Hierarchy

The system uses a hierarchical agent architecture:

```
Root Agent (Orchestrator)
├── Character Creation Agent
├── Campaing Outline Generation Agent
├── Narrative Agent
├── Rules Lawyer Agent
```

### Key Components

- **Root Agent**: Master coordinator that routes actions to specialist agents
- **Character Creation Agent**: Guides players through character creation
- **Campaing Outline Generation Agent**: Generates campaign outlines and story structure
- **Narrative Agent**: Handles story elements and environmental descriptions
- **Rules Lawyer Agent**: Manages combat mechanics and rules questions


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