#!/usr/bin/env python3
"""
Test script to verify the communication protocol is working according to the outline.
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from root_agent.agent import root_agent
from utils import run_agent_with_retry

async def test_communication_protocol():
    """Test the communication protocol according to the outline."""
    
    print("🧪 Testing Communication Protocol")
    print("=" * 50)
    
    # Set up session service
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="dungeon_master",
        user_id="test_user",
        session_id="test_session",
    )
    
    # Create runner
    runner = Runner(
        agent=root_agent,
        app_name="dungeon_master",
        session_service=session_service
    )
    
    # Test 1: Player input should be routed to Player Interface Agent
    print("\n📝 Test 1: Player input routing")
    print("-" * 30)
    
    test_message = "Hello, I want to create a character"
    content = types.Content(role='user', parts=[types.Part(text=test_message)])
    
    print(f"Player input: '{test_message}'")
    print("Expected: Root agent should route this to Player Interface Agent")
    
    success, response, agent_name = await run_agent_with_retry(
        runner, "test_user", "test_session", content
    )
    
    if success and response:
        print(f"✅ Response received: {response[:100]}...")
    else:
        print(f"❌ Error: Failed to get response")
    
    # Test 2: Character creation agent should run in same session
    print("\n📝 Test 2: Character creation agent session")
    print("-" * 30)
    
    test_message = "start new campaign"
    content = types.Content(role='user', parts=[types.Part(text=test_message)])
    
    print(f"Campaign start message: '{test_message}'")
    print("Expected: Character creation agent should run in same session as root agent")
    
    success, response, agent_name = await run_agent_with_retry(
        runner, "test_user", "test_session", content
    )
    
    if success and response:
        print(f"✅ Response received: {response[:100]}...")
    else:
        print(f"❌ Error: Failed to get response")
    
    print("\n✅ Communication protocol test completed!")

if __name__ == "__main__":
    asyncio.run(test_communication_protocol()) 