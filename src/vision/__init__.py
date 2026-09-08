"""Vision package — screen capture stubs + verified dweller tracking."""

from src.vision.dweller_detect import (
    detect_dwellers,
    detect_vault_suit_blobs,
    annotate_detections,
)
from src.vision.dweller_tracker import DwellerTracker, TrackerConfig

__all__ = [
    "detect_dwellers",
    "detect_vault_suit_blobs",
    "annotate_detections",
    "DwellerTracker",
    "TrackerConfig",
    "ScreenCapture",
    "ImageRecognition",
]


class ScreenCapture:
    """Captures screenshots of the game window."""

    def __init__(self):
        self.game_window = None

    def capture(self):
        """Capture the current game screen."""
        raise NotImplementedError(
            "Live capture requires a running Fallout Shelter window. "
            "Steam login is currently blocked in this environment — use "
            "assets/screenshots or src.sim.vault_sim instead."
        )


class ImageRecognition:
    """Recognizes game elements in screenshots."""

    def __init__(self):
        self.templates = {}

    def load_templates(self, template_dir):
        raise NotImplementedError("Template matching not yet verified")

    def detect_resources(self, image):
        raise NotImplementedError("Resource OCR not yet verified")

    def detect_dwellers(self, image):
        return detect_dwellers(image)
