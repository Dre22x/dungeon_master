# Session Management Guide

This guide explains how session management works in the Dungeon Master application and how sessions are handled in the main UI interface.

## Session Types

### Root Agent Sessions
- **Format**: `session_{campaign_id}`
- **Purpose**: Main campaign coordinator and orchestrator
- **Visibility**: Visible in main UI interface
- **Persistence**: Long-running throughout campaign lifecycle

### Sub-Agent Sessions
- **Format**: `sub_agent_{agent_name}_{campaign_id}_{timestamp}`
- **Purpose**: Temporary sessions for specific agent tasks
- **Visibility**: Not visible in main UI (by design)
- **Persistence**: Created and terminated for each specific task

### Character Creation Sessions
- **Format**: `sub_agent_character_creation_{campaign_id}_{timestamp}`
- **Purpose**: Direct player interaction during character creation
- **Visibility**: Sessions are visible in main UI interface
- **Persistence**: Temporary, terminated after character creation

## Main UI Integration

When you create or load a campaign, the application manages sessions through the main UI interface:

```python
# Example session management in main UI
session_id = f"session_{campaign_id}"
# All interactions happen through the main UI at http://localhost:5001
```

## Session Management Commands

### List All Sessions
```bash
python session_manager.py list
```

### Delete a Session
```bash
python session_manager.py delete <session_id>
```

### Open Main UI
```bash
python session_manager.py web
```

## Session Lifecycle

### 1. Campaign Creation
- **Root session created**: `session_{campaign_id}`
- **Session visible in main UI**
- **Session URL provided in response**

### 2. Agent Transfers
- **Sub-agent session created**: `sub_agent_{agent_name}_{campaign_id}_{timestamp}`
- **Session visible in main UI**
- **Session URL provided in response**

### 3. Character Creation
- **Character creation session created**: `sub_agent_character_creation_{campaign_id}_{timestamp}`
- **Main UI can access the session**
- **Direct player interaction enabled**

### 4. Session Termination
- **Sub-agent sessions automatically terminated**
- **Not visible in main UI**
- **Root session persists throughout campaign**

### Session Not Visible in Main UI

If a session is not visible in the main UI:

1. **Check if main UI is running**
   ```bash
   python UI/app.py
   ```

2. **Verify session exists**
   ```bash
   python session_manager.py list
   ```

3. **Check session ID format**
   - Root sessions: `session_{campaign_id}`
   - Sub-agent sessions: `sub_agent_{agent_name}_{campaign_id}_{timestamp}`

## Configuration

### Application Configuration

The `adk.yaml` file defines the application name as `dungeon_master`, which is used in:

- Session ID generation
- Main UI URLs
- Session management

### Session Service Configuration

The application uses `InMemorySessionService` for session management:

```python
from google.adk.sessions import InMemorySessionService
session_service = InMemorySessionService()
```

## Usage Examples

### 1. Create New Campaign
```bash
# Start the application
python start_app.py

# Open main UI
# Navigate to http://localhost:5001
# Click "New Campaign"
```

### 2. Load Existing Campaign
```bash
# In main UI, enter campaign ID
# Click "Load Campaign"
# Note the session ID in the response
```

### 3. Open Main UI
```bash
# Open main UI for a specific campaign
python session_manager.py web
```

## Troubleshooting

### Session Not Found
- Check if the session exists using `python session_manager.py list`
- Verify the campaign ID is correct
- Ensure the main UI is running

### Session Management Issues
- Check that the session service is properly initialized
- Verify session IDs are being generated correctly
- Ensure proper session cleanup is happening

### Main UI Connection Issues
- Ensure the Flask app is running on port 5001
- Check for port conflicts
- Verify all dependencies are installed

This setup provides full visibility into your agent sessions and seamless integration with the main UI interface. 