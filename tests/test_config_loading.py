#!/usr/bin/env python3
"""
Test script to verify that agent model configuration loading works properly.
This test will check that agents can load their model names from the YAML file.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agents.config_loader import load_agent_config, get_model_for_agent, get_all_agent_models

def test_config_loading():
    """Test the configuration loading functionality."""
    print("🧪 Agent Configuration Loading Test")
    print("=" * 50)
    
    # Test 1: Load all agent configurations
    print("\n1. Loading all agent configurations...")
    agent_configs = load_agent_config()
    
    if agent_configs:
        print(f"✅ Successfully loaded {len(agent_configs)} agent configurations")
        print("📋 Agent configurations:")
        for agent_name, model_name in agent_configs.items():
            print(f"   {agent_name}: {model_name}")
    else:
        print("❌ Failed to load agent configurations")
        return False
    
    # Test 2: Get model for specific agents
    print("\n2. Testing individual agent model retrieval...")
    test_agents = ["root_agent", "narrative_agent", "npc_agent", "rules_lawyer_agent", "character_creation_agent", "player_interface_agent"]
    
    for agent_name in test_agents:
        model_name = get_model_for_agent(agent_name)
        print(f"   {agent_name}: {model_name}")
        
        if model_name:
            print(f"   ✅ {agent_name} model retrieved successfully")
        else:
            print(f"   ❌ Failed to get model for {agent_name}")
    
    # Test 3: Test with non-existent agent
    print("\n3. Testing with non-existent agent...")
    non_existent_model = get_model_for_agent("non_existent_agent")
    print(f"   Non-existent agent model: {non_existent_model}")
    
    if non_existent_model == "gemini-2.5-flash-lite-preview-06-17":
        print("   ✅ Default model returned for non-existent agent")
    else:
        print("   ⚠️  Unexpected default model returned")
    
    # Test 4: Get all agent models
    print("\n4. Testing get_all_agent_models...")
    all_models = get_all_agent_models()
    
    if all_models:
        print(f"✅ Successfully retrieved {len(all_models)} agent models")
        print("📋 All agent models:")
        for agent_name, model_name in all_models.items():
            print(f"   {agent_name}: {model_name}")
    else:
        print("❌ Failed to retrieve all agent models")
        return False
    
    print(f"\n✅ Configuration loading test completed successfully!")
    return True

def test_agent_creation():
    """Test that agents can be created with the loaded configurations."""
    print("\n🧪 Agent Creation Test")
    print("=" * 50)
    
    try:
        # Import agents to test creation
        from agents.sub_agents import narrative_agent, npc_agent, rules_lawyer_agent, character_creation_agent, player_interface_agent
        from agents.agent import root_agent
        
        print("✅ All agents imported successfully")
        
        # Check that agents have the correct model names
        agents_to_check = [
            ("root_agent", root_agent),
            ("narrative_agent", narrative_agent),
            ("npc_agent", npc_agent),
            ("rules_lawyer_agent", rules_lawyer_agent),
            ("character_creation_agent", character_creation_agent),
            ("player_interface_agent", player_interface_agent)
        ]
        
        print("\n📋 Agent model verification:")
        for agent_name, agent in agents_to_check:
            expected_model = get_model_for_agent(agent_name)
            actual_model = agent.model
            
            print(f"   {agent_name}:")
            print(f"     Expected: {expected_model}")
            print(f"     Actual:   {actual_model}")
            
            if expected_model == actual_model:
                print(f"     ✅ Model matches")
            else:
                print(f"     ❌ Model mismatch!")
                return False
        
        print(f"\n✅ Agent creation test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import agents: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during agent creation test: {e}")
        return False

def test_yaml_parsing():
    """Test that the YAML file can be parsed correctly."""
    print("\n🧪 YAML Parsing Test")
    print("=" * 50)
    
    try:
        import yaml
        
        # Get the path to the adk.yaml file
        yaml_path = os.path.join(os.path.dirname(__file__), 'adk.yaml')
        
        print(f"📁 Loading YAML file: {yaml_path}")
        
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print("✅ YAML file parsed successfully")
        
        # Check for required sections
        if 'agents' in config:
            print(f"✅ Found {len(config['agents'])} agents in configuration")
            
            for i, agent in enumerate(config['agents'], 1):
                agent_name = agent.get('name', 'Unknown')
                model_name = agent.get('model', 'Unknown')
                print(f"   Agent {i}: {agent_name} -> {model_name}")
        else:
            print("❌ No 'agents' section found in YAML")
            return False
        
        if 'app_name' in config:
            print(f"✅ App name: {config['app_name']}")
        else:
            print("❌ No 'app_name' found in YAML")
            return False
        
        print(f"\n✅ YAML parsing test completed successfully!")
        return True
        
    except FileNotFoundError:
        print(f"❌ YAML file not found at {yaml_path}")
        return False
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during YAML parsing test: {e}")
        return False

if __name__ == "__main__":
    print("🎲 Testing Agent Configuration Loading")
    print("=" * 60)
    
    # Run all tests
    tests = [
        ("Configuration Loading", test_config_loading),
        ("YAML Parsing", test_yaml_parsing),
        ("Agent Creation", test_agent_creation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("📋 Test Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Agent configuration loading is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the configuration.") 