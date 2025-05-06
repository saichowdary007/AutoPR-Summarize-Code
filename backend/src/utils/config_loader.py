import os
import yaml
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def load_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from a YAML file or environment variables.

    Args:
        config_file: Path to config file (optional)

    Returns:
        Dictionary with configuration values
    """
    # Default config path
    if config_file is None:
        config_file = os.environ.get(
            "CONFIG_FILE",
            os.path.join(
                os.path.dirname(__file__), "..", "config", "default_config.yaml"
            ),
        )

    config = {}

    # Try to load from file
    try:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f) or {}
            logger.info(f"Loaded configuration from {config_file}")
    except FileNotFoundError:
        logger.warning(f"Config file {config_file} not found, using default settings")
    except yaml.YAMLError as e:
        logger.error(f"Error parsing config file: {e}")

    # Override with environment variables
    env_prefix = "PR_ASSISTANT_"
    env_config = {
        key[len(env_prefix) :].lower(): _parse_env_value(value)
        for key, value in os.environ.items()
        if key.startswith(env_prefix)
    }

    # Apply environment overrides
    _deep_update(config, env_config)

    return config


def _parse_env_value(value: str) -> Any:
    """
    Parse environment variable values into appropriate types.

    Args:
        value: String value from environment variable

    Returns:
        Parsed value (bool, int, float, or original string)
    """
    # Check for boolean values
    if value.lower() in ["true", "yes", "1"]:
        return True
    if value.lower() in ["false", "no", "0"]:
        return False

    # Check for integer
    try:
        return int(value)
    except ValueError:
        pass

    # Check for float
    try:
        return float(value)
    except ValueError:
        pass

    # Return as string if it doesn't match other types
    return value


def _deep_update(target: Dict[str, Any], source: Dict[str, Any]) -> None:
    """
    Deep update a nested dictionary.

    Args:
        target: Target dictionary to update
        source: Source dictionary with new values
    """
    for key, value in source.items():
        if key in target and isinstance(target[key], dict) and isinstance(value, dict):
            # Recursively update nested dictionaries
            _deep_update(target[key], value)
        else:
            # Set or override the value
            target[key] = value
