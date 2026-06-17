# flake8: noqa
"""
Staging Django settings.
Mirrors live settings for now but exists as a separate module so staging-specific
overrides can be added without changing production settings.
"""
from .live import *