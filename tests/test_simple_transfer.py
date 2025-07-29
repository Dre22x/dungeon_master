#!/usr/bin/env python3
"""
Simple test to verify the transfer_to_agent function works correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def test_transfer_to_agent_function():
    """Test the transfer_to_agent function directly."""
    
    print("🧪 Testing Transfer to Agent Function (Simple)")
    print("=" * 50)
    
    try:
        # Import the function
        from tools.misc_tools import transfer_to_agent
        
        # Test data
        action_data = {
            "action_type": "character_creation",
            "player_input": "create a character",
            "target": "",
            "context": "starting a new campaign",
            "campaign_id": "test_simple",
            "game_state": "character_creation"
        }
        
        print("Testing transfer_to_agent function...")
        print(f"Action data: {action_data}")
        
        # Test the function
        result = transfer_to_agent("character_creation_agent", action_data, "test_simple")
        
        print(f"✅ Function executed successfully!")
        print(f"Result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing function: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_transfer_to_agent_function()
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!") 