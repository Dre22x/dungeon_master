#!/usr/bin/env python3
"""
Test script to reproduce and fix the combat state error.
This test ensures that combat is properly initialized before calling advance_turn.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.game_mechanics import start_combat, get_combat_state, advance_turn, end_combat
from firestore.db_utils import save_campaign, load_campaign
import json

def test_combat_error_reproduction():
    """Test to reproduce the combat state error."""
    
    print("=== Testing Combat State Error Reproduction ===\n")
    
    # Setup test campaign
    campaign_id = "test_combat_error"
    campaign_data = {
        "campaign_id": campaign_id,
        "characters": [
            {
                "name": "Test Fighter",
                "class": "Fighter",
                "level": 1,
                "hp": 12,
                "max_hp": 12,
                "strength": 16,
                "dexterity": 14,
                "constitution": 14,
                "intelligence": 10,
                "wisdom": 12,
                "charisma": 8,
                "equipment": ["longsword", "chain mail"],
                "proficiency_bonus": 2
            }
        ],
        "current_location": "A dark forest clearing",
        "game_state": "exploration",
        "notes": "Testing combat error"
    }
    
    # Save test campaign
    save_campaign(campaign_id, campaign_data)
    print("✓ Test campaign created and saved")
    
    # Test 1: Try to advance turn without starting combat (should fail)
    print("\n--- Test 1: Advance Turn Without Combat (Expected Error) ---")
    try:
        result = advance_turn(campaign_id)
        print(f"Result: {result}")
        if "Error: No active combat" in result:
            print("✓ Correctly caught error - no active combat")
        else:
            print("✗ Should have caught error - no active combat")
    except Exception as e:
        print(f"Exception: {e}")
    
    # Test 2: Start combat properly
    print("\n--- Test 2: Start Combat Properly ---")
    combat_result = start_combat(campaign_id, ["Test Fighter"], ["Goblin"])
    print(f"Combat Result: {combat_result}")
    
    # Test 3: Check combat state
    print("\n--- Test 3: Check Combat State ---")
    combat_state = get_combat_state(campaign_id)
    print(f"Combat State: {json.dumps(combat_state, indent=2)}")
    
    if combat_state and not combat_state.get("error"):
        print("✓ Combat state is active")
    else:
        print("✗ Combat state should be active")
    
    # Test 4: Now try to advance turn (should work)
    print("\n--- Test 4: Advance Turn With Active Combat ---")
    try:
        result = advance_turn(campaign_id)
        print(f"Result: {result}")
        if "Error: No active combat" not in result:
            print("✓ Successfully advanced turn")
        else:
            print("✗ Should have advanced turn successfully")
    except Exception as e:
        print(f"Exception: {e}")
    
    # Test 5: End combat
    print("\n--- Test 5: End Combat ---")
    end_result = end_combat(campaign_id)
    print(f"End Result: {end_result}")
    
    # Test 6: Try to advance turn after ending combat (should fail)
    print("\n--- Test 6: Advance Turn After Ending Combat (Expected Error) ---")
    try:
        result = advance_turn(campaign_id)
        print(f"Result: {result}")
        if "Error: No active combat" in result:
            print("✓ Correctly caught error - combat ended")
        else:
            print("✗ Should have caught error - combat ended")
    except Exception as e:
        print(f"Exception: {e}")
    
    print("\n=== Combat Error Test Complete ===")
    print("\nSummary:")
    print("- advance_turn should fail when no combat is active")
    print("- start_combat should properly initialize combat state")
    print("- advance_turn should work when combat is active")
    print("- end_combat should clear combat state")
    print("- advance_turn should fail again after combat ends")

def test_combat_workflow_fix():
    """Test the proper combat workflow to prevent the error."""
    
    print("\n=== Testing Proper Combat Workflow ===\n")
    
    campaign_id = "test_combat_workflow"
    
    # Setup test campaign
    campaign_data = {
        "campaign_id": campaign_id,
        "characters": [
            {
                "name": "Test Fighter",
                "class": "Fighter",
                "level": 1,
                "hp": 12,
                "max_hp": 12,
                "strength": 16,
                "dexterity": 14,
                "constitution": 14,
                "intelligence": 10,
                "wisdom": 12,
                "charisma": 8,
                "equipment": ["longsword", "chain mail"],
                "proficiency_bonus": 2
            }
        ],
        "current_location": "A dark forest clearing",
        "game_state": "exploration",
        "notes": "Testing combat workflow"
    }
    
    save_campaign(campaign_id, campaign_data)
    print("✓ Test campaign created")
    
    # Simulate proper combat workflow
    print("\n--- Simulating Proper Combat Workflow ---")
    
    # Step 1: Check if combat is active
    combat_state = get_combat_state(campaign_id)
    print(f"1. Initial combat state: {combat_state.get('error', 'Active')}")
    
    # Step 2: Start combat when player declares attack
    print("2. Player declares attack - starting combat...")
    start_result = start_combat(campaign_id, ["Test Fighter"], ["Goblin"])
    print(f"   Start result: {start_result}")
    
    # Step 3: Verify combat is active
    combat_state = get_combat_state(campaign_id)
    print(f"3. Combat state after start: {combat_state.get('status', 'Error')}")
    
    # Step 4: Resolve attack and advance turn
    print("4. Resolving attack and advancing turn...")
    advance_result = advance_turn(campaign_id)
    print(f"   Advance result: {advance_result}")
    
    # Step 5: End combat
    print("5. Ending combat...")
    end_result = end_combat(campaign_id)
    print(f"   End result: {end_result}")
    
    # Step 6: Verify combat is ended
    combat_state = get_combat_state(campaign_id)
    print(f"6. Combat state after end: {combat_state.get('error', 'Still Active')}")
    
    print("\n✓ Proper combat workflow completed successfully")

if __name__ == "__main__":
    test_combat_error_reproduction()
    test_combat_workflow_fix() 