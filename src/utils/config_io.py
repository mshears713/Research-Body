"""
MISSION CONFIG IMPORT/EXPORT
=============================

TEACHING PURPOSE:
-----------------
Demonstrates how to serialize and deserialize mission configurations
for sharing, versioning, and reuse.

Supports multiple formats:
  • YAML (human-readable, git-friendly)
  • JSON (programmatic, web-compatible)
  • Python dict (runtime configuration)
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class MissionConfigIO:
    """
    Import/Export utility for mission configurations.

    Enables:
      • Saving mission configs for reuse
      • Sharing configs across teams
      • Version control of research templates
      • Programmatic config generation
    """

    @staticmethod
    def export_to_yaml(config: Dict[str, Any], file_path: Path) -> bool:
        """
        Export mission config to YAML file.

        Args:
            config: Mission configuration dict
            file_path: Path to save YAML file

        Returns:
            True if successful

        Example:
            >>> config = {
            ...     'topic': 'AI wildfire detection',
            ...     'max_sources': 10,
            ...     'summary_style': 'technical'
            ... }
            >>> MissionConfigIO.export_to_yaml(config, Path('my_mission.yaml'))
        """
        try:
            # Add metadata
            export_config = {
                'exported_at': datetime.now().isoformat(),
                'version': '1.0',
                **config
            }

            with open(file_path, 'w') as f:
                yaml.dump(export_config, f, default_flow_style=False, sort_keys=False)

            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False

    @staticmethod
    def import_from_yaml(file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Import mission config from YAML file.

        Args:
            file_path: Path to YAML file

        Returns:
            Mission configuration dict or None if failed

        Example:
            >>> config = MissionConfigIO.import_from_yaml(Path('my_mission.yaml'))
            >>> print(config['topic'])
        """
        try:
            with open(file_path, 'r') as f:
                config = yaml.safe_load(f)

            # Remove metadata fields
            config.pop('exported_at', None)
            config.pop('version', None)

            return config
        except Exception as e:
            print(f"Import failed: {e}")
            return None

    @staticmethod
    def export_to_json(config: Dict[str, Any], file_path: Path) -> bool:
        """Export mission config to JSON file."""
        try:
            export_config = {
                'exported_at': datetime.now().isoformat(),
                'version': '1.0',
                **config
            }

            with open(file_path, 'w') as f:
                json.dump(export_config, f, indent=2)

            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False

    @staticmethod
    def import_from_json(file_path: Path) -> Optional[Dict[str, Any]]:
        """Import mission config from JSON file."""
        try:
            with open(file_path, 'r') as f:
                config = json.load(f)

            # Remove metadata fields
            config.pop('exported_at', None)
            config.pop('version', None)

            return config
        except Exception as e:
            print(f"Import failed: {e}")
            return None

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate mission configuration.

        Args:
            config: Mission configuration dict

        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = ['topic']

        for field in required_fields:
            if field not in config:
                return (False, f"Missing required field: {field}")

        return (True, None)


# Convenience functions
def save_mission_config(config: Dict, path: Path, format: str = 'yaml'):
    """
    Save mission config to file.

    Args:
        config: Mission configuration
        path: File path
        format: 'yaml' or 'json'
    """
    io = MissionConfigIO()

    if format == 'yaml':
        return io.export_to_yaml(config, path)
    elif format == 'json':
        return io.export_to_json(config, path)
    else:
        raise ValueError(f"Unknown format: {format}")


def load_mission_config(path: Path):
    """
    Load mission config from file.

    Auto-detects format from extension.
    """
    io = MissionConfigIO()

    if path.suffix in ['.yaml', '.yml']:
        return io.import_from_yaml(path)
    elif path.suffix == '.json':
        return io.import_from_json(path)
    else:
        raise ValueError(f"Unknown file extension: {path.suffix}")
