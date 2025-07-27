#!/usr/bin/env python3
"""
Test script to verify the new agent routing system works correctly.
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(__file__))

from agents.agent import root_agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from tools.misc_tools import route_to_character_creation_agent

async def test_new_routing():
    """Test that the new routing system properly invokes sub-agents."""
    
    print("🧪 Testing New Agent Routing System")
    print("=" * 50)
    
    # Test direct routing function
    print("Testing direct routing to Character Creation Agent...")
    
    action_data = {
        "action_type": "character_creation",
        "player_input": "I want to create a new character",
        "context": "New campaign startup",
        "campaign_id": "test_routing"
    }
    
    try:
        response = route_to_character_creation_agent(action_data)
        print(f"✅ Character Creation Agent Response: {response[:200]}...")
    except Exception as e:
        print(f"❌ Error in direct routing: {e}")
    
    print("\n" + "=" * 50)
    
    # Test through root agent
    print("Testing routing through Root Agent...")
    
    # Set up session and runner
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="dungeon_master",
        user_id="test_user",
        session_id="test_routing_session",
    )

    runner = Runner(
        agent=root_agent,
        app_name="dungeon_master",
        session_service=session_service
    )

    # Test message that should trigger character creation
    test_message = """
NEW CAMPAIGN STARTUP: A new campaign has been created with campaign_id: test_routing

Please begin the character creation process by routing to the Character Creation Agent.
"""
    
    content = types.Content(
        role='user', 
        parts=[types.Part(text=test_message)]
    )

    print(f"Sending test message to Root Agent...")
    print()

    # Run the agent
    async for event in runner.run_async(
        user_id="test_user", 
        session_id="test_routing_session", 
        new_message=content
    ):
        if hasattr(event, 'agent') and event.agent:
            print(f"🤖 Agent activated: {event.agent.name}")
        
        if hasattr(event, 'actions') and event.actions:
            if hasattr(event.actions, 'escalate') and event.actions.escalate:
                print(f"🔄 Agent transfer: {event.actions.escalate.agent_name}")
        
        if event.is_final_response():
            if event.content and event.content.parts:
                response = event.content.parts[0].text
                print(f"📤 Final response: {response[:200]}...")
            break

    print("\n✅ Test completed!")

if __name__ == "__main__":
    asyncio.run(test_new_routing()) 