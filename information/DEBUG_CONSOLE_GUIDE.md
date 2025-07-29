# Enhanced Debug Console Guide

The Dungeon Master application now features a comprehensive debug console that provides detailed visibility into agent interactions, tool calls, and data transfers. This guide explains how to use the enhanced debugging features.

## 🎯 Overview

The enhanced debug console tracks and displays:
- **Agent Activations**: Which agents are responding to calls
- **Agent Transfers**: Which agent is transferring to another agent and why
- **Tool Calls**: What tools agents are calling with their arguments
- **Tool Results**: Success/failure status and results of tool calls
- **Final Responses**: Agent responses with character counts
- **Errors**: Detailed error information with stack traces
- **API Calls**: Backend API interactions
- **Console Output**: General backend logging

## 🚀 Getting Started

### 1. Access the Debug Console
1. Start the Flask application: `python UI/app.py`
2. Open your browser to `http://localhost:5001`
3. Create or load a campaign
4. Click on the **"Debug"** tab in the campaign interface

### 2. Understanding the Interface

The debug console features:
- **Filter Controls**: Checkboxes to show/hide specific event types
- **Auto-scroll Toggle**: Automatically scroll to new messages
- **Clear Button**: Clear all debug messages
- **Show Summary Button**: Display a summary of all events
- **Expandable Details**: Click "Show Details" to see full event data

## 📊 Event Types and Icons

| Icon | Event Type | Description | Color |
|------|------------|-------------|-------|
| 🤖 | `agent_activated` | Agent is activated and responding | Purple |
| 🔄 | `agent_transfer` | Agent transfers to another agent | Cyan |
| 🔧 | `tool_call` | Agent calls a tool with arguments | Orange |
| ✅ | `tool_result` | Tool execution result (success/error) | Green |
| 📤 | `final_response` | Agent's final response to user | Blue |
| 💥 | `agent_error` | Error occurred during agent execution | Red |
| 🌐 | `api` | API calls and responses | Blue |
| 📝 | `console` | General console output | Green |
| ❌ | `error` | General error messages | Red |
| ⚠️ | `warning` | Warning messages | Yellow |

## 🔍 Using Filters

The debug console includes filter controls to focus on specific event types:

### Available Filters:
- **🤖 Agents**: Show agent activation events
- **🔄 Transfers**: Show agent transfer events
- **🔧 Tools**: Show tool call events
- **✅ Results**: Show tool result events
- **📤 Responses**: Show final response events
- **💥 Errors**: Show error events
- **🌐 API**: Show API call events
- **📝 Console**: Show console output events

### How to Use Filters:
1. Check/uncheck the filter checkboxes to show/hide specific event types
2. Filters are applied in real-time
3. All filters are enabled by default
4. Use the "Show Summary" button to see event statistics

## 📋 Event Details

Each debug event can be expanded to show detailed information:

### Agent Activation Details:
```json
{
  "agent_name": "narrative_agent",
  "agent_description": "You are the world's greatest storyteller...",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### Agent Transfer Details:
```json
{
  "from_agent": "player_interface_agent",
  "to_agent": "rules_lawyer_agent",
  "reason": "Combat action detected",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### Tool Call Details:
```json
{
  "agent_name": "rules_lawyer_agent",
  "tool_name": "get_monster_details",
  "tool_args": {
    "monster_name": "goblin"
  },
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### Tool Result Details:
```json
{
  "tool_name": "get_monster_details",
  "result": {
    "name": "Goblin",
    "hp": 7,
    "ac": 15,
    "actions": [...]
  },
  "error": null,
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

## 📊 Summary Feature

The "Show Summary" button provides a comprehensive overview of all debug events:

### Summary Information:
- **Total Events**: Count of all debug events
- **Errors**: Number of error events
- **Agents Used**: List of all agents that were activated
- **Tools Called**: List of all tools that were called
- **Event Breakdown**: Count of each event type

### Example Summary Output:
```
📊 DEBUG SUMMARY:
Total Events: 15
Errors: 0
Agents Used: root_agent, player_interface_agent, rules_lawyer_agent
Tools Called: get_monster_details, roll_dice, load_character_from_campaign

Event Breakdown:
  agent_activated: 3
  agent_transfer: 2
  tool_call: 5
  tool_result: 5
  final_response: 1
```

## 🛠️ Troubleshooting

### Common Issues:

1. **No Debug Messages Appearing**
   - Ensure the WebSocket connection is established
   - Check that you're on the Debug tab
   - Verify the campaign is properly initialized

2. **Missing Event Types**
   - Check that the corresponding filter is enabled
   - Ensure the agent is actually calling tools or transferring

3. **WebSocket Connection Issues**
   - Refresh the page to reconnect
   - Check browser console for WebSocket errors
   - Verify the Flask app is running

### Debug Console Not Working:
1. Check browser console for JavaScript errors
2. Verify all filter checkboxes are checked
3. Try clearing the console and sending a new message
4. Restart the Flask application

## 🔧 Advanced Usage

### Real-time Monitoring:
- Keep the debug console open while playing
- Monitor agent behavior patterns
- Identify performance bottlenecks
- Track tool usage frequency

### Debugging Agent Issues:
- Look for error events when agents fail
- Check tool call arguments for invalid data
- Monitor agent transfer patterns
- Verify tool results match expectations

### Performance Analysis:
- Use the summary feature to analyze event patterns
- Identify which agents are most active
- Track tool call frequency and success rates
- Monitor response times and character counts

## 🎮 Example Debug Session

Here's what a typical debug session might look like:

1. **Campaign Initialization**:
   ```
   🤖 [10:30:00] AGENT ACTIVATED: root_agent
   🔧 [10:30:01] TOOL CALL: load_campaign by root_agent
   ✅ [10:30:01] TOOL RESULT: load_campaign
   📤 [10:30:02] FINAL RESPONSE: root_agent (245 chars)
   ```

2. **Player Message Processing**:
   ```
   🤖 [10:30:05] AGENT ACTIVATED: player_interface_agent
   🔄 [10:30:06] AGENT TRANSFER: player_interface_agent → rules_lawyer_agent
   🤖 [10:30:06] AGENT ACTIVATED: rules_lawyer_agent
   🔧 [10:30:07] TOOL CALL: get_monster_details by rules_lawyer_agent
   ✅ [10:30:07] TOOL RESULT: get_monster_details
   🔧 [10:30:08] TOOL CALL: roll_dice by rules_lawyer_agent
   ✅ [10:30:08] TOOL RESULT: roll_dice
   📤 [10:30:09] FINAL RESPONSE: rules_lawyer_agent (156 chars)
   ```

## 🚀 Future Enhancements

Planned improvements for the debug console:
- **Timeline View**: Visual timeline of agent interactions
- **Performance Metrics**: Response time tracking
- **Agent Communication Graph**: Visual representation of agent transfers
- **Export Functionality**: Save debug logs to file
- **Search and Filter**: Advanced search within debug messages
- **Real-time Statistics**: Live counters and metrics

---

## 📝 Technical Notes

The enhanced debug console is built using:
- **WebSocket Communication**: Real-time message streaming
- **JSON Data Format**: Structured event data
- **CSS Filtering**: Client-side event filtering
- **JavaScript Event Handling**: Dynamic UI updates

The debug system integrates with the Google ADK framework to capture agent events and tool calls in real-time, providing unprecedented visibility into the multi-agent system's operation. 