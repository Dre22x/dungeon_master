"""
Game Data and Rules Engine

This package contains all the D&D game data and mechanics:
- Character data and creation tools
- Game mechanics and combat system
- Equipment, spells, and rules
- Monster and NPC data
- Campaign outline generation
"""

from . import tools
from .tools import (
    character_data,
    game_mechanics,
    campaign_outline,
    races,
    classes,
    spells,
    equipment,
    monsters,
    magic_items,
    weapons,
    traits,
    subraces,
    subclasses,
    rules
)

__all__ = [
    "tools",
    "character_data",
    "game_mechanics", 
    "campaign_outline",
    "races",
    "classes",
    "spells",
    "equipment",
    "monsters",
    "magic_items",
    "weapons",
    "traits",
    "subraces",
    "subclasses",
    "rules"
]
