"""
AI Agent System for Dungeon Master

This package contains the multi-agent system that powers the AI Dungeon Master:
- Root Agent: Master coordinator and orchestrator
- Narrative Agent: Storytelling and environmental descriptions
- Rules Lawyer Agent: Game mechanics and rules enforcement
- Character Creation Agent: Player character development
- Campaign Outline Generation Agent: Story structure and campaign planning
"""

from .agent import root_agent
from .sub_agents import (
    narrative_agent,
    rules_lawyer_agent,
    character_creation_agent,
    campaign_outline_generation_agent
)

__all__ = [
    "root_agent",
    "narrative_agent",
    "rules_lawyer_agent",
    "character_creation_agent",
    "campaign_outline_generation_agent"
]