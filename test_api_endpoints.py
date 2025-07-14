#!/usr/bin/env python3
"""
Test script for the API endpoints
"""

import requests
import json

def test_api_endpoints():
    """Test the API endpoints"""
    
    base_url = "http://localhost:5001"
    
    # Test skills index endpoint
    print("Testing skills index endpoint...")
    try:
        response = requests.get(f"{base_url}/api/skills_index")
        print(f"Skills index status: {response.status_code}")
        print(f"Skills index response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Server not running. Please start the server first.")
        return
    except Exception as e:
        print(f"Skills index error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test proficiencies index endpoint
    print("Testing proficiencies index endpoint...")
    try:
        response = requests.get(f"{base_url}/api/proficiencies_index")
        print(f"Proficiencies index status: {response.status_code}")
        print(f"Proficiencies index response: {response.json()}")
    except Exception as e:
        print(f"Proficiencies index error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test equipment endpoint
    print("Testing equipment endpoint...")
    try:
        response = requests.get(f"{base_url}/api/equipment/longsword")
        print(f"Equipment status: {response.status_code}")
        print(f"Equipment response: {response.json()}")
    except Exception as e:
        print(f"Equipment error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test skill endpoint
    print("Testing skill endpoint...")
    try:
        response = requests.get(f"{base_url}/api/skills/athletics")
        print(f"Skill status: {response.status_code}")
        print(f"Skill response: {response.json()}")
    except Exception as e:
        print(f"Skill error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test proficiency endpoint
    print("Testing proficiency endpoint...")
    try:
        response = requests.get(f"{base_url}/api/proficiencies/longswords")
        print(f"Proficiency status: {response.status_code}")
        print(f"Proficiency response: {response.json()}")
    except Exception as e:
        print(f"Proficiency error: {e}")

if __name__ == "__main__":
    test_api_endpoints() 