"""
Utility Functions

Helper functions and utilities used across the project.
"""

import logging
import json
from pathlib import Path


def setup_logging(log_level=logging.INFO):
    """Configure logging for the application."""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('autofallout.log'),
            logging.StreamHandler()
        ]
    )


def load_config(config_path='config.json'):
    """Load configuration from JSON file."""
    path = Path(config_path)
    if path.exists():
        with open(path, 'r') as f:
            return json.load(f)
    return {}


def save_config(config, config_path='config.json'):
    """Save configuration to JSON file."""
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


class Timer:
    """Simple timer utility for tracking execution time."""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """Start the timer."""
        import time
        self.start_time = time.time()
    
    def stop(self):
        """Stop the timer and return elapsed time."""
        import time
        self.end_time = time.time()
        return self.elapsed()
    
    def elapsed(self):
        """Get elapsed time."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None
