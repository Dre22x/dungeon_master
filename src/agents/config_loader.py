"""
Configuration loader for agent model names from YAML file.
"""

import yaml
import os
from typing import Dict, Optional

def load_agent_config() -> Dict[str, str]:
    """
    Load agent configuration from adk.yaml file.
    
    Returns:
        Dict[str, str]: Dictionary mapping agent names to model names
    """
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    yaml_path = os.path.join(project_root, 'config', 'adk.yaml')
    
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        agent_configs = {}
        if 'agents' in config:
            for agent in config['agents']:
                agent_name = agent.get('name')
                model_name = agent.get('model')
                if agent_name and model_name:
                    agent_configs[agent_name] = model_name
        
        print(f"[ConfigLoader] Loaded {len(agent_configs)} agent configurations from {yaml_path}")
        return agent_configs
        
    except FileNotFoundError:
        print(f"ERROR: adk.yaml file not found at {yaml_path}")
        print("Using default model configuration.")
        return {}
    except yaml.YAMLError as e:
        print(f"ERROR: Failed to parse adk.yaml file: {e}")
        print("Using default model configuration.")
        return {}
    except Exception as e:
        print(f"ERROR: Failed to load agent configuration: {e}")
        print("Using default model configuration.")
        return {}

def get_model_for_agent(agent_name: str, default_model: str = "gemini-2.5-flash") -> str:
    """
    Get the model name for a specific agent.
    
    Args:
        agent_name: str - The name of the agent
        default_model: str - Default model to use if not found in config
    
    Returns:
        str - The model name for the agent
    """
    agent_configs = load_agent_config()
    return agent_configs.get(agent_name, default_model)

def get_all_agent_models() -> Dict[str, str]:
    """
    Get all agent model configurations.
    
    Returns:
        Dict[str, str] - Dictionary of all agent names and their models
    """
    return load_agent_config() 