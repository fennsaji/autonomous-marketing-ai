"""
API package for all API versions.
"""
from .v1 import api_router as api_v1_router

__all__ = ["api_v1_router"]