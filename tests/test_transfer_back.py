#!/usr/bin/env python3
"""
Test to verify that character creation agent transfers back to root agent after completion.
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from root_agent.agent import root_agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

async def test_transfer_back():
    """Test that character creation agent transfers back to root agent after completion."""
    
    print("🧪 Testing Transfer Back After Character Creation")
    print("=" * 60)
    
    # Set up session and runner
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="dungeon_master",
        user_id="test_user",
        session_id="test_transfer_session",
    )

    runner = Runner(
        agent=root_agent,
        app_name="dungeon_master",
        session_service=session_service
    )

    # Test message that should trigger character creation
    test_message = "NEW CAMPAIGN STARTUP: A new campaign has been created with campaign_id: test_transfer"
    
    content = types.Content(
        role='user', 
        parts=[types.Part(text=test_message)]
    )

    print(f"Sending test message: {test_message}")
    print()

    # Run the agent
    async for event in runner.run_async(
        user_id="test_user", 
        session_id="test_transfer_session", 
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
                print(f"📤 Final response: {response}")
            break

    print("\n✅ Test completed!")

if __name__ == "__main__":
    asyncio.run(test_transfer_back()) 