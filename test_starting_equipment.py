#!/usr/bin/env python3
"""
Quick test to verify get_starting_equipment function is accessible
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.tools import get_starting_equipment

def test_starting_equipment():
    """Test the get_starting_equipment function"""
    
    print("=== Testing get_starting_equipment function ===")
    
    # Test with a valid class
    result = get_starting_equipment("fighter")
    print(f"Fighter starting equipment result: {result}")
    
    # Test with another class
    result2 = get_starting_equipment("wizard")
    print(f"Wizard starting equipment result: {result2}")
    
    print("✅ get_starting_equipment function is accessible!")

if __name__ == "__main__":
    test_starting_equipment() 