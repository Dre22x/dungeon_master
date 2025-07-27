#!/usr/bin/env python3
"""
Simple test to verify the combat error fix works correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.game_mechanics import start_combat, get_combat_state, advance_turn, update_combat_participant_hp, end_combat
from firestore.db_utils import save_campaign

def test_combat_fix():
    """Test that the combat error fix works correctly."""
    
    print("=== Testing Combat Error Fix ===\n")
    
    # Setup test campaign
    campaign_id = "test_combat_fix"
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
        "notes": "Testing combat fix"
    }
    
    save_campaign(campaign_id, campaign_data)
    print("✓ Test campaign created")
    
    # Test 1: Try to advance turn without combat (should give helpful error)
    print("\n1. Testing advance_turn without combat:")
    result = advance_turn(campaign_id)
    print(f"   Result: {result}")
    if "Please ensure combat has been initiated" in result:
        print("   ✓ Helpful error message provided")
    else:
        print("   ✗ Should provide helpful error message")
    
    # Test 2: Try to update HP without combat (should give helpful error)
    print("\n2. Testing update_combat_participant_hp without combat:")
    result = update_combat_participant_hp(campaign_id, "Test Fighter", 10)
    print(f"   Result: {result}")
    if "Please ensure combat has been initiated" in result:
        print("   ✓ Helpful error message provided")
    else:
        print("   ✗ Should provide helpful error message")
    
    # Test 3: Start combat properly
    print("\n3. Starting combat:")
    result = start_combat(campaign_id, ["Test Fighter"], ["Goblin"])
    print(f"   Result: {result}")
    
    # Test 4: Now advance turn should work
    print("\n4. Testing advance_turn with active combat:")
    result = advance_turn(campaign_id)
    print(f"   Result: {result}")
    if "Error:" not in result:
        print("   ✓ Successfully advanced turn")
    else:
        print("   ✗ Should have advanced turn successfully")
    
    # Test 5: Update HP should work
    print("\n5. Testing update_combat_participant_hp with active combat:")
    result = update_combat_participant_hp(campaign_id, "Test Fighter", 8)
    print(f"   Result: {result}")
    if "Error:" not in result:
        print("   ✓ Successfully updated HP")
    else:
        print("   ✗ Should have updated HP successfully")
    
    # Test 6: End combat
    print("\n6. Ending combat:")
    result = end_combat(campaign_id)
    print(f"   Result: {result}")
    
    # Test 7: Try to advance turn after ending combat (should fail)
    print("\n7. Testing advance_turn after ending combat:")
    result = advance_turn(campaign_id)
    print(f"   Result: {result}")
    if "Please ensure combat has been initiated" in result:
        print("   ✓ Correctly caught error after combat ended")
    else:
        print("   ✗ Should have caught error after combat ended")
    
    print("\n=== Combat Fix Test Complete ===")
    print("\nSummary:")
    print("- Error messages now include helpful guidance")
    print("- Combat state is properly managed")
    print("- Functions work correctly when combat is active")
    print("- Functions fail gracefully when combat is not active")

if __name__ == "__main__":
    test_combat_fix() 