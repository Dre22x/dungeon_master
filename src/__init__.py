"""
AI Dungeon Master - An AI-powered Dungeons & Dragons game master using Google's Agent Development Kit

This package provides a complete D&D game management system with:
- Multi-agent AI coordination
- Real-time game mechanics
- Web-based user interface
- Persistent data storage
"""

__version__ = "1.0.0"
__author__ = "Andre Gonzaga"
__description__ = "AI-powered Dungeons & Dragons game master"

from . import agents
from . import core
from . import data
from . import database
from . import web
