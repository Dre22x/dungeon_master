# Project Structure

## Overview
This document describes the clean, professional structure of the AI Dungeon Master project.

## Directory Structure

```
dungeon_master/
├── src/                           # Main source code
│   ├── agents/                   # AI Agent System
│   ├── core/                     # Core Game Logic
│   ├── data/                     # Game Data & Rules Engine
│   ├── database/                 # Data Persistence Layer
│   ├── web/                      # Web Interface
│   ├── main.py                   # Console application entry point
│   └── start_app.py             # Web application startup
├── config/                        # Configuration Files
├── scripts/                       # Utility Scripts
├── tests/                         # Test Suite
├── docs/                          # Documentation
├── examples/                      # Usage Examples
└── [project files]                # Setup and configuration
```

## Package Organization

- **src/agents/**: AI agent system and coordination
- **src/core/**: Core game logic and utilities
- **src/data/**: Game data, rules, and mechanics
- **src/database/**: Data persistence and storage
- **src/web/**: Web interface and user experience
