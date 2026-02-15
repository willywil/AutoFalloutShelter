"""
Data Models

Defines data structures for game entities.
"""

from dataclasses import dataclass
from typing import Optional, List
from enum import Enum


class ResourceType(Enum):
    """Types of resources in the game."""
    POWER = "power"
    FOOD = "food"
    WATER = "water"
    CAPS = "caps"
    STIMPAKS = "stimpaks"
    RADAWAY = "radaway"


class RoomType(Enum):
    """Types of rooms in the shelter."""
    POWER_GENERATOR = "power_generator"
    DINER = "diner"
    WATER_TREATMENT = "water_treatment"
    LIVING_QUARTERS = "living_quarters"
    STORAGE = "storage"
    MEDBAY = "medbay"
    SCIENCE_LAB = "science_lab"
    # Add more room types as needed


@dataclass
class SPECIAL:
    """Dweller SPECIAL stats."""
    strength: int
    perception: int
    endurance: int
    charisma: int
    intelligence: int
    agility: int
    luck: int


@dataclass
class Dweller:
    """Represents a dweller in the shelter."""
    id: str
    name: str
    level: int
    health: int
    special: SPECIAL
    current_room: Optional[str] = None
    is_training: bool = False
    is_exploring: bool = False


@dataclass
class Room:
    """Represents a room in the shelter."""
    id: str
    room_type: RoomType
    level: int
    position: tuple  # (x, y) coordinates
    assigned_dwellers: List[str]  # List of dweller IDs
    is_producing: bool = False
    production_progress: float = 0.0


@dataclass
class GameState:
    """Current state of the game."""
    resources: Dict[ResourceType, float]
    dwellers: List[Dweller]
    rooms: List[Room]
    timestamp: float
