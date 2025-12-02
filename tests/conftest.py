"""Conftest for tests."""
import sys
import os

# Add the parent directory to the path so we can import fastapi_study_buddy
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
