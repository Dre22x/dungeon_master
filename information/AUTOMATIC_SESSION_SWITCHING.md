# Automatic Session Switching

## Overview

The Dungeon Master application now includes automatic session switching functionality that allows the UI to automatically switch to the appropriate agent session when agents transfer control to each other. This enables users to communicate directly with sub-agents in their dedicated sessions through the main UI interface.

## How It Works

### 1. Agent Transfer Detection

The system detects agent transfers in two ways:

#### A. Escalation Events
When an agent escalates to another agent (using the `escalate` action), the system:
- Detects the escalation event in the `log_agent_event` function
- Extracts the source and target agent names
- Creates a new session ID for the target agent
- Sends a session switch notification to all connected clients

#### B. Routing Tool Calls
When the root agent routes to a sub-agent using routing tools (e.g., `route_to_character_creation_agent`), the system:
- Detects routing tool calls in the `log_agent_event` function
- Extracts the target agent name from the tool name
- Creates a new session ID for the sub-agent
- Sends a session switch notification to all connected clients

### 2. Session ID Generation

New session IDs are generated using the following format:
- **Escalation events**: `sub_agent_{agent_name}_{campaign_id}_{timestamp}`
- **Routing calls**: `sub_agent_{agent_name}_{campaign_id}_{timestamp}`

Example session IDs:
- `sub_agent_character_creation_abc123_1703123456`
- `sub_agent_narrative_abc123_1703123457`

### 3. UI Integration

The frontend automatically handles session switch notifications:

#### A. WebSocket Notifications
- Session switch notifications are sent via WebSocket to all connected clients
- The UI receives these notifications and updates the session display
- Users see a system message indicating the session switch

#### B. Session Switcher Component
- A session switcher component shows the current active session
- Users can manually switch sessions using the "Switch Session" button
- All interactions happen through the main UI interface

## API Endpoints

### 1. Manual Session Switch
```
POST /switch-session/{campaign_id}
```
**Body:**
```json
{
  "session_id": "session_id_here",
  "agent_name": "Agent Name"
}
```

### 2. Get Current Session
```
GET /get-current-session/{campaign_id}
```

## Frontend Features

### 1. Session Switcher Component
- Shows current active session and agent
- Provides buttons to switch sessions
- Automatically appears when a session is active

### 2. Manual Session Switching
- Modal dialog for entering session ID and agent name
- Validates input and performs session switch
- Shows success/error messages

### 3. Automatic Notifications
- System messages when sessions switch automatically
- Debug console entries for session switch events
- WebSocket notifications for real-time updates

## Usage Examples

### Automatic Session Switching

1. **User starts character creation**:
   - Root agent routes to Character Creation Agent
   - UI automatically switches to Character Creation Agent session
   - User can communicate directly with Character Creation Agent

2. **User asks for combat mechanics**:
   - Root agent routes to Rules Lawyer Agent
   - UI automatically switches to Rules Lawyer Agent session
   - User can communicate directly with Rules Lawyer Agent

### Manual Session Switching

1. **User wants to switch to a specific session**:
   - Click "Switch Session" button
   - Select session from dropdown
   - Confirm the switch
   - UI updates to show new session

2. **User wants to see available sessions**:
   - Session switcher shows all available sessions
   - Each session shows agent name and description
   - User can select any available session

## Implementation Details

### Pre-Invocation Session Switching

The system includes a pre-invocation session switching mechanism that ensures the UI switches to the new session before any agent activity begins:

```python
def trigger_pre_invocation_session_switch(campaign_id, agent_name, session_id):
    """Trigger session switching before agent invocation to ensure no text is missed."""
    # Send session switch notification immediately
    # UI switches to new session before agent starts
```

### Session Switch Notifications

Session switch notifications include:

- **Session ID**: The new session identifier
- **Agent Name**: The target agent's name
- **Switch Type**: Whether it's automatic or manual
- **Timestamp**: When the switch occurred
- **Details**: Additional information about the switch

### Debug Console Integration

The debug console shows session switch events with:

- **Session switch notifications**: Real-time updates
- **Agent transfer events**: When agents transfer control
- **Session creation/deletion**: Session lifecycle events
- **Error handling**: Failed session switches

## Troubleshooting

### Session Switch Not Working

1. **Check WebSocket connection**:
   - Ensure debug WebSocket is connected
   - Check browser console for connection errors

2. **Verify session exists**:
   - Check that the target session was created
   - Verify session ID format is correct

3. **Check agent routing**:
   - Ensure the routing tool was called correctly
   - Verify agent names match expected format

### Debug Console Not Showing Switches

1. **Check debug filters**:
   - Ensure "session_switch" filter is enabled
   - Check that debug console is visible

2. **Verify WebSocket connection**:
   - Check that debug stream is connected
   - Look for connection error messages

3. **Check server logs**:
   - Look for session switch trigger messages
   - Verify no errors in session management

### Manual Session Switch Failing

1. **Check session ID format**:
   - Root sessions: `session_{campaign_id}`
   - Sub-agent sessions: `sub_agent_{agent_name}_{campaign_id}_{timestamp}`

2. **Verify session exists**:
   - Use session manager to list active sessions
   - Check that the session ID is correct

3. **Check API endpoint**:
   - Verify the switch-session endpoint is working
   - Check for server error messages

## Best Practices

### 1. Session Management
- Monitor active sessions regularly
- Clean up old sessions when no longer needed
- Use session manager for administration

### 2. Debug Console Usage
- Keep debug console open during development
- Monitor session switch events in real-time
- Use filters to focus on relevant events

### 3. User Experience
- Provide clear feedback when sessions switch
- Show current session information prominently
- Allow manual session switching when needed

This automatic session switching system provides seamless agent interaction through the main UI interface, ensuring users can communicate directly with the appropriate agent for their current needs. 