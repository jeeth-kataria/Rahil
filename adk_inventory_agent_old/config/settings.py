"""
Configuration settings for the ADK Inventory Agent.
"""

import os
from typing import Dict, Any

# Default configuration values
DEFAULT_CONFIG = {
    "agent": {
        "name": "ADKInventoryAgent",
        "model": "gemini-2.0-flash-exp",
        "log_level": "INFO"
    },
    "analytics": {
        "default_forecast_periods": 30,
        "default_service_level": 0.95,
        "enable_mock_data": True
    },
    "google_cloud": {
        "project": os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id"),
        "location": os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
        "use_vertex_ai": os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "True").lower() == "true"
    }
}


def get_config() -> Dict[str, Any]:
    """Get the current configuration."""
    return DEFAULT_CONFIG.copy()


def update_config(new_config: Dict[str, Any]) -> None:
    """Update configuration with new values."""
    DEFAULT_CONFIG.update(new_config)