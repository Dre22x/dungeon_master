"""
Database Layer and Data Persistence

This package handles all data storage and retrieval:
- Firebase Firestore integration
- Database utilities and helpers
- Data initialization and management
"""

from . import firestore
from .firestore import (
    db_utils,
    init_database
)

__all__ = ["firestore", "db_utils", "init_database"]
