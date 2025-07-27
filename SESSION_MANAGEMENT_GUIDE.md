# Session Management and ADK Web Integration Guide

## Overview

This guide explains how session management works in the Dungeon Master application and how to use ADK web interface with your sessions.

## Session Architecture

### Session Types

1. **Root Agent Sessions (Persistent)**
   - Created when campaigns are initialized
   - Session ID format: `session_{campaign_id}`
   - Stored in Firestore for persistence
   - Visible in ADK web interface

2. **Sub-Agent Sessions (Temporary)**
   - Created for each sub-agent task
   - Session ID format: `sub_agent_{agent_name}_{campaign_id}_{timestamp}`
   - Automatically terminated after task completion
   - Not visible in ADK web (by design)

### Session Service

The application now uses `FirestoreSessionService` instead of `InMemorySessionService` to ensure:
- Sessions persist across application restarts
- Sessions are visible in ADK web interface
- Proper session isolation and management

## ADK Web Integration

### Automatic Session Switching

When you create or load a campaign, the application generates ADK web URLs that automatically switch to the correct session:

```
http://localhost:8000/dev-ui/?app=dungeon_master&session=session_{campaign_id}
```

### Manual Session Management

Use the session manager script to manage sessions:

```bash
# List all active sessions
python session_manager.py list

# Open ADK web for a specific campaign
python session_manager.py open {campaign_id}

# Open ADK web without a specific session
python session_manager.py web

# Delete a session
python session_manager.py delete {session_id}
```

### API Endpoints

The application provides REST API endpoints for session management:

- `GET /sessions` - List all active sessions
- `DELETE /sessions/{session_id}` - Delete a specific session

## Expected Behavior

### ✅ What You Should See

1. **New Campaign Creation**
   - Session created with ID `session_{campaign_id}`
   - Session visible in ADK web interface
   - ADK web URL provided in response

2. **Campaign Loading**
   - Existing session loaded from Firestore
   - Session visible in ADK web interface
   - ADK web URL provided in response

3. **Ongoing Conversations**
   - Same session used for all interactions
   - Session persists across application restarts
   - ADK web can access the session

### ❌ What You Won't See

1. **Sub-Agent Sessions**
   - These are temporary and terminated immediately
   - Not visible in ADK web (by design)
   - Used only for specific tasks

2. **In-Memory Sessions**
   - Previous implementation used in-memory storage
   - Sessions were not persistent
   - Not visible in ADK web

## Troubleshooting

### Session Not Visible in ADK Web

1. **Check if ADK web is running**
   ```bash
   adk web .
   ```

2. **Verify session exists**
   ```bash
   python session_manager.py list
   ```

3. **Check Firestore connection**
   - Ensure `config/service-account-key.json` exists
   - Verify Firestore permissions

4. **Manual session access**
   - Navigate to: `http://localhost:8000/dev-ui/?app=dungeon_master`
   - Select the session from the dropdown

### Session Management Issues

1. **Clear all sessions**
   ```bash
   python session_manager.py list
   # Then delete each session individually
   python session_manager.py delete {session_id}
   ```

2. **Restart application**
   ```bash
   python start_app.py
   ```

3. **Check application logs**
   - Look for session creation/deletion messages
   - Check for Firestore errors

## Configuration

### Firestore Setup

Ensure your Firestore configuration is correct:

1. **Service Account Key**
   - File: `config/service-account-key.json`
   - Must have Firestore read/write permissions

2. **Environment Variables**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="config/service-account-key.json"
   ```

### ADK Configuration

The `adk.yaml` file defines the application name as `dungeon_master`, which is used in:
- Session creation
- ADK web URLs
- Session management

## Best Practices

1. **Session Cleanup**
   - Regularly clean up old sessions
   - Use the session manager to monitor active sessions

2. **ADK Web Usage**
   - Use ADK web for debugging and monitoring
   - Switch between sessions as needed
   - Monitor agent interactions in real-time

3. **Development Workflow**
   - Create test campaigns for development
   - Use session manager to switch between campaigns
   - Monitor sessions during development

## Migration from In-Memory Sessions

If you were previously using in-memory sessions:

1. **Existing sessions will not be migrated**
   - In-memory sessions are lost on restart
   - New sessions will be persistent

2. **ADK web will now show sessions**
   - Previously invisible sessions will now be visible
   - You can monitor sessions in real-time

3. **Session management is now available**
   - Use session manager for administration
   - API endpoints for programmatic access

## Example Workflow

1. **Start the application**
   ```bash
   python start_app.py
   ```

2. **Create a new campaign**
   - Use the web interface at `http://localhost:5001`
   - Note the ADK web URL in the response

3. **Open ADK web**
   ```bash
   python session_manager.py open {campaign_id}
   ```

4. **Monitor the session**
   - Watch agent interactions in real-time
   - Debug issues as they occur

5. **Manage sessions**
   ```bash
   python session_manager.py list
   ```

This setup provides full visibility into your agent sessions and seamless integration with ADK web interface. 