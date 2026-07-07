"""Gunicorn entry point for hookrelay."""

from hookrelay.app import create_app

app = create_app()
