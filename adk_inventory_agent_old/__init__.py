"""
ADK Inventory Management Agent Package

A comprehensive inventory management agent built with Google's Agent Development Kit (ADK).
Provides 4-tier analytics: Descriptive, Diagnostic, Predictive, and Prescriptive.
"""

from .agent import inventory_agent

__version__ = "1.0.0"
__author__ = "ADK Inventory Agent"

# Export the main agent for easy access
__all__ = ["inventory_agent"]
