"""
Automation Module

Handles mouse and keyboard input automation to interact with the game.
"""

import pyautogui
import time


class InputController:
    """Controls mouse and keyboard inputs."""
    
    def __init__(self):
        # Safety feature: move mouse to corner to abort
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
    
    def click(self, x, y, clicks=1, interval=0.0):
        """Click at specified coordinates."""
        pyautogui.click(x, y, clicks=clicks, interval=interval)
    
    def drag(self, x1, y1, x2, y2, duration=0.5):
        """Drag from one point to another."""
        pyautogui.moveTo(x1, y1)
        pyautogui.dragTo(x2, y2, duration=duration)
    
    def collect_resource(self, x, y):
        """Click to collect a resource at specified location."""
        self.click(x, y)
        time.sleep(0.5)


class GameActions:
    """High-level game actions."""
    
    def __init__(self, input_controller):
        self.input = input_controller
    
    def assign_dweller(self, dweller_pos, room_pos):
        """Assign a dweller to a room by dragging."""
        # TODO: Implement dweller assignment
        pass
    
    def rush_room(self, room_pos):
        """Rush production in a room."""
        # TODO: Implement room rushing
        pass
