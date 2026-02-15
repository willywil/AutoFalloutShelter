"""
Main entry point for AutoFalloutShelter
"""

import logging
from src.utils import setup_logging
from src.vision import ScreenCapture, ImageRecognition
from src.automation import InputController, GameActions
from src.strategy import ResourceManager, DwellerManager, IncidentHandler


def main():
    """Main execution loop."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting AutoFalloutShelter...")
    
    # Initialize components
    screen_capture = ScreenCapture()
    image_recognition = ImageRecognition()
    input_controller = InputController()
    game_actions = GameActions(input_controller)
    
    # Initialize strategy managers
    resource_manager = ResourceManager()
    dweller_manager = DwellerManager()
    incident_handler = IncidentHandler()
    
    logger.info("Components initialized successfully")
    
    # TODO: Implement main game loop
    # 1. Capture screen
    # 2. Recognize game state
    # 3. Make decisions
    # 4. Execute actions
    # 5. Repeat
    
    logger.info("AutoFalloutShelter stopped")


if __name__ == "__main__":
    main()
