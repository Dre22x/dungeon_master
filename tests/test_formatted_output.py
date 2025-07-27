#!/usr/bin/env python3
"""
Test script to demonstrate the new formatted combat output.
"""

def show_formatted_examples():
    """Show examples of the new formatted output."""
    
    print("=== Formatted Combat Output Examples ===\n")
    
    # Example 1: Successful attack
    print("Example 1: Successful Attack")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    COMBAT RESOLUTION                         ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║ Character: Elara Meadowlight                                ║")
    print("║ ───────────────────────────────────────────────────────────── ║")
    print("║ Attack Roll: 17 + 5 = 22 vs AC 12                          ║")
    print("║ Result: HIT                                                 ║")
    print("║ ───────────────────────────────────────────────────────────── ║")
    print("║ Damage: 4 + 2 = 6 fire damage                              ║")
    print("║ Target HP: 0                                                ║")
    print("║ Status: unconscious/dead                                    ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    # Example 2: Missed attack
    print("Example 2: Missed Attack")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    COMBAT RESOLUTION                         ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║ Character: Thorne Ironfist                                  ║")
    print("║ ───────────────────────────────────────────────────────────── ║")
    print("║ Attack Roll: 8 + 6 = 14 vs AC 16                          ║")
    print("║ Result: MISS                                                ║")
    print("║ ───────────────────────────────────────────────────────────── ║")
    print("║ Damage: 0 (miss)                                           ║")
    print("║ Target HP: 12 (unchanged)                                  ║")
    print("║ Status: alive                                               ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    # Example 3: Critical hit
    print("Example 3: Critical Hit")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    COMBAT RESOLUTION                         ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║ Character: Zara Swiftwind                                   ║")
    print("║ ───────────────────────────────────────────────────────────── ║")
    print("║ Attack Roll: 20 + 4 = 24 vs AC 15                          ║")
    print("║ Result: CRITICAL HIT!                                       ║")
    print("║ ───────────────────────────────────────────────────────────── ║")
    print("║ Damage: (6 + 3) × 2 = 18 slashing damage                   ║")
    print("║ Target HP: 4                                                ║")
    print("║ Status: alive                                               ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    # Example 4: Skill check
    print("Example 4: Skill Check")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                   SKILL CHECK RESULT                         ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║ Character: Elara Meadowlight                                ║")
    print("║ Skill: Stealth                                              ║")
    print("║ Roll: 15 + 7 = 22 vs DC 18                                 ║")
    print("║ Result: SUCCESS                                             ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    # Example 5: Information request
    print("Example 5: Information Request")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    MONSTER: GOBLIN                          ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║ Armor Class: 15                                             ║")
    print("║ Hit Points: 7 (2d6)                                         ║")
    print("║ Speed: 30 ft.                                               ║")
    print("║ ───────────────────────────────────────────────────────────── ║")
    print("║ Small humanoid, typically armed with scimitars and shortbows ║")
    print("║ Actions include Scimitar (+4 to hit, 5 slashing) and        ║")
    print("║ Shortbow (+4 to hit, 5 piercing, range 80/320 ft.)          ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    print("=== Formatting Benefits ===")
    print("✓ Clear visual separation between different types of information")
    print("✓ Easy to scan and read quickly")
    print("✓ Professional appearance")
    print("✓ Consistent formatting across all rule lawyer responses")
    print("✓ Better readability in chat interfaces")

if __name__ == "__main__":
    show_formatted_examples() 