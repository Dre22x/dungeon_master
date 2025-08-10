"""
Web Interface and User Experience

This package provides the web-based user interface:
- Flask web application
- HTML templates and static assets
- API endpoints and routing
"""

from . import app
from .app import app as flask_app

__all__ = ["app", "flask_app"]
